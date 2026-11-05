"""Download the Overture Maps extracts that utah.py reads -> data/ut/

- overture_ut_bbox.parquet     every place in Utah's bounding box (name, category, address, point)
- overture_ut_sources.parquet  which datasets each Utah eating/drinking listing came from (Meta, Foursquare, ...)
- ut_shapes.json               simplified state and county outlines for the map
- ut_state_detail.geojson      the state outline at full detail, for the in-state test

Reads the public Overture bucket over S3 with DuckDB (no account needed). Ported from md-eats/pipeline/fetch_overture.py.
Utah: land division areas, so the Great Salt Lake, Utah Lake and Lake Powell stay out of the outline while their islands and shores
stay in (Antelope Island's Buffalo Point café, Bullfrog's marina); the "counties" are Utah's 29. Small islands are kept (min area
0.000005 deg2, about 5 ha), and the script checks the islands, the shore towns and the border towns that straddle a state line
(Wendover is in Utah, West Wendover in Nevada).
"""
import os, json, time
import duckdb
from shapely import wkb
from shapely.geometry import mapping, Polygon

RELEASE = "2026-10-21.0"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "ut")
# Utah (37.0°N–42.0°N, 109.04°W–114.05°W) plus a margin for the border towns (Wendover, Kanab's Arizona neighbours, Bear Lake)
BBOX = "bbox.xmin BETWEEN -114.2 AND -108.9 AND bbox.ymin BETWEEN 36.9 AND 42.1"
EAT = "('restaurant','casual_eatery','bar','fast_food_restaurant','coffee_shop','cafe','smoothie_juice_bar','brewery','food_court')"
os.makedirs(OUT, exist_ok=True)

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs; INSTALL spatial; LOAD spatial; SET s3_region='us-west-2';")
places = f"s3://overturemaps-us-west-2/release/{RELEASE}/theme=places/type=place/*.parquet"

t = time.time()
if not os.path.exists(f"{OUT}/overture_ut_bbox.parquet"):
    con.execute(f"""
COPY (
  SELECT id, names.primary AS name, basic_category AS cat, taxonomy.primary AS tax, taxonomy.hierarchy AS hier, confidence,
         operating_status AS status, brand.names.primary AS brand, addresses[1].freeform AS street, addresses[1].locality AS city,
         addresses[1].postcode AS zip, addresses[1].region AS region, ST_Y(geometry) AS lat, ST_X(geometry) AS lon, websites[1] AS web,
         phones[1] AS phone
  FROM read_parquet('{places}', hive_partitioning=1) WHERE {BBOX}
) TO '{OUT}/overture_ut_bbox.parquet' (FORMAT PARQUET)""")
    print("places in bbox", round(time.time() - t), "s", flush=True)
if not os.path.exists(f"{OUT}/overture_ut_sources.parquet"):
    con.execute(f"""
COPY (
  SELECT id, list_transform(sources, lambda x: x.dataset) AS ds, list_transform(sources, lambda x: x.update_time) AS ut,
         list_transform(sources, lambda x: x.record_id) AS rid,
         len(socials) AS n_soc, len(websites) AS n_web, len(phones) AS n_ph
  FROM read_parquet('{places}', hive_partitioning=1)
  WHERE {BBOX} AND basic_category IN {EAT}
) TO '{OUT}/overture_ut_sources.parquet' (FORMAT PARQUET)""")
    print("sources", round(time.time() - t), "s", flush=True)

areas = f"s3://overturemaps-us-west-2/release/{RELEASE}/theme=divisions/type=division_area/*.parquet"
rows = con.execute(f"""
  SELECT subtype, names.primary AS name, ST_AsWKB(geometry) AS g
  FROM read_parquet('{areas}', hive_partitioning=1)
  WHERE country = 'US' AND region = 'US-UT' AND subtype IN ('region', 'county') AND class = 'land'
    AND bbox.xmin > -114.3 AND bbox.xmax < -108.8 AND bbox.ymin > 36.8 AND bbox.ymax < 42.2""").fetchall()


def rings(geom, tol, min_area):
    geom = geom.simplify(tol, preserve_topology=True)
    polys = [p for p in getattr(geom, "geoms", [geom]) if p.geom_type == "Polygon" and p.area >= min_area]
    return [[[round(x, 3), round(y, 3)] for x, y in p.exterior.coords] for p in polys]


out = {"state": None, "counties": []}
for sub, name, g in rows:
    geom = wkb.loads(bytes(g)).buffer(0)
    if sub == "region":
        json.dump(mapping(geom.simplify(0.0005, preserve_topology=True)), open(f"{OUT}/ut_state_detail.geojson", "w"))
        out["state"] = [[r] for r in rings(geom, 0.002, 0.000005)]
    else:
        out["counties"].append({"name": name, "c": rings(geom, 0.004, 0.00002)})
# full-detail county polygons for assigning each place to a county (not shipped)
json.dump({name: mapping(wkb.loads(bytes(g)).buffer(0).simplify(0.0003, preserve_topology=True))
           for sub, name, g in rows if sub == "county"}, open(f"{OUT}/ut_counties_detail.geojson", "w"))
json.dump(out, open(f"{OUT}/ut_shapes.json", "w"), separators=(",", ":"))
print("outlines: state", len(out["state"] or []), "rings +", len(out["counties"]), "counties;", round(time.time() - t), "s total")
# islands, shores and border towns: each must fall on the right side of the detailed state outline
from shapely.geometry import shape, Point
st = shape(json.load(open(f"{OUT}/ut_state_detail.geojson")))
for nm, lon, lat, want in [("Antelope Island (Buffalo Point)", -112.2590, 41.0381, True), ("Bullfrog Marina (Lake Powell)", -110.7290, 37.5150, True),
                           ("Garden City (Bear Lake)", -111.3940, 41.9460, True), ("Wendover, UT", -114.0360, 40.7370, True),
                           ("West Wendover, NV", -114.0730, 40.7390, False), ("Kanab", -112.5260, 37.0475, True),
                           ("Fredonia, AZ", -112.5260, 36.9455, False), ("Bluff", -109.5540, 37.2840, True)]:
    ok = st.contains(Point(lon, lat))
    print(f"  {nm}: {'inside' if ok else 'outside'}{'' if ok == want else '  <-- WRONG'}")
print("counties:", len(out["counties"]), sorted(c["name"] for c in out["counties"]))

# the neighbours' land (Idaho, Wyoming, Colorado, Arizona, Nevada, New Mexico): listings.py widens Utah's outline ~300 m for lake
# shores, but only where no neighbour's land is, so a West Wendover, NV or Fredonia, AZ listing on the far side of the line stays out
nb = con.execute(f"""
  SELECT region, ST_AsWKB(geometry) FROM read_parquet('{areas}', hive_partitioning=1)
  WHERE country = 'US' AND region IN ('US-ID', 'US-WY', 'US-CO', 'US-AZ', 'US-NV', 'US-NM') AND subtype = 'region' AND class = 'land'""").fetchall()
from shapely.ops import unary_union
from shapely.geometry import box
near = box(-114.3, 36.8, -108.8, 42.2)
nbg = unary_union([wkb.loads(bytes(g)).buffer(0).intersection(near) for _, g in nb])
json.dump(mapping(nbg.simplify(0.0002, preserve_topology=True)), open(f"{OUT}/ut_neighbors.geojson", "w"))
print("neighbours:", sorted(r for r, _ in nb))
