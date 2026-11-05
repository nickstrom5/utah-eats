"""Writes data/research/app/*.json (hand-checked Utah guides), data/research/michelin.json, jbf.json and closed.json from the
compact lists below. Ported from md-eats/pipeline/build_research.py.

Each entry cites the 2025-26 page that names it (robots-checked host: check_sources.py), read through Claude's web fetcher on
2026-11-05. Every page below is dated on its face, or is an official tourism listing (Visit Utah, Visit Salt Lake, Visit Park City).
The address comes from the map listing we already hold for that name in that town (site/utah.json), never from memory; a name that
isn't found exactly once in its town (or at the street number given) is left out and listed in data/research/app/LEADS.md. A place the
map data lacks is added only when the dated page prints its street address (ADDR).
Usage: ../.venv/bin/python build_research.py   (then utah.py)"""
import json, os, re
from brands import brand_of
from common import norm_name
ROOT = os.path.join(os.path.dirname(__file__), "..")
R = os.path.join(ROOT, "data", "research")
d = json.load(open(os.path.join(ROOT, "site", "utah.json")))
C, M = d["cols"], d["meta"]
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower().replace("'", "").replace("\u2019", ""))).strip()

# each dated on its face, or an official tourism listing (read 2026-11-05)
VSL_ICONIC = "https://www.visitsaltlake.com/blog/stories/post/where-to-eat-in-salt-lake-city-15-iconic-restaurants-that-define-the-city/"  # 2026-06-09
VSL_PI = "https://www.visitsaltlake.com/plan-your-visit/community-diversity/pacific-islander/"      # Visit Salt Lake, (c) 2026
VU_MIGHTY5 = "https://www.visitutah.com/articles/dining-between-the-mighty-five"                   # Visit Utah, (c) 2026
VU_FOODIE = "https://www.visitutah.com/plan-your-trip/recommended-itineraries/foodie-journey"      # Visit Utah, (c) 2026
VU_PIE = "https://www.visitutah.com/articles/utahs-pie-ala-road"                                   # Visit Utah, (c) 2026
VPC_MAIN = "https://www.visitparkcity.com/blog/stories/post/restaurants-on-historic-main-street-in-park-city-utah/"  # 2026-09-11
TRIB_PASTRAMI = "https://www.sltrib.com/artsliving/food/2025/03/11/crown-astro-apollo-serve-pastrami/"   # 2025-03-11
KSL_CROWN = "https://www.ksl.com/article/51357312/stacked-with-flavor-family-and-pastrami-crown-burgers-has-been-a-utah-staple-for-nearly-50-years"  # 2025-08-07
GSLC_BURGERS = "https://gastronomicslc.com/best-burgers-salt-lake/"                                  # "The Best Burgers in Salt Lake City 2026"
KSL_PACSEAS = "https://www.ksl.com/article/ksltv/pacific-islander-voices-where-food-meets-family/51588010"  # 2025-10-17
TT_OLDBAR = "https://www.tastingtable.com/1786324/oldest-bar-every-state/"                          # 2025-02-17
US_RUTHS = "https://utahstories.com/2025/10/ruths-diner-emigration-canyon-utah-history-100-years/"  # 2025-10-18
MI_UT = "https://guide.michelin.com/us/en/utah/restaurants"                                          # the 2026 Southwest selection (9 in Utah)
JBF26 = "https://www.jamesbeard.org/stories/james-beard-award-semifinalists-2026"                   # 2026-01-21
JBF26N = "https://www.jamesbeard.org/stories/james-beard-awards-restaurant-and-chef-nominees-2026"  # 2026-03-31
JBF25 = "https://www.jamesbeard.org/stories/the-2025-james-beard-award-semifinalists"               # 2025-01-22
JBF25N = "https://www.jamesbeard.org/stories/2025-james-beard-awards-restaurant-and-chef-nominees"   # 2025-04-02

# (name as the source writes it or as our listing spells it, town as our listing has it, street number to pick the location (or
# None), note, founded, founded_note, [sources])
SLC = "Salt Lake City"
GUIDES = {
 "salt lake classic": [   # Visit Salt Lake's "15 iconic restaurants that define the city" (2026-06-09)
  ("Ruth's Diner", SLC, "4160", "A trolley-car diner up Emigration Canyon, with a patio and big biscuits.", 1949,
   "Ruth Evans opened Ruth's Hamburgers downtown in 1930 and moved the diner up Emigration Canyon in 1949 (Utah Stories, October 2025).", [VSL_ICONIC, US_RUTHS]),
  ("Red Iguana", SLC, "736", "The North Temple original, known for its moles.", None, None, [VSL_ICONIC]),
  ("Takashi", SLC, "18", "Downtown sushi that helped shape the city's dining.", None, None, [VSL_ICONIC]),
  ("Valter's Osteria", SLC, "173", "Upscale Italian for celebration dinners.", None, None, [VSL_ICONIC]),
  ("The Pie Pizzeria", SLC, "1320", "Big, cheesy pies by the University; a late-night standby.", None, None, [VSL_ICONIC]),
  ("Mumbai House Salt Lake City", SLC, "2731", "Rich curries and big portions.", None, None, [VSL_ICONIC]),
  ("Feldman's Deli", SLC, "2005", "An East Coast-style Jewish deli: pastrami and Reubens.", None, None, [VSL_ICONIC]),
  ("La Caille Restaurant", "Sandy", "9565", "A French-inspired estate at the foot of the Wasatch.", None, None, [VSL_ICONIC]),
  ("The Copper Onion", SLC, "111", "Downtown's ingredient-driven kitchen, open since 2010.", None, None, [VSL_ICONIC]),
  ("Chanon Thai Café", SLC, "278", "A small, busy Thai spot known for khao soi.", None, None, [VSL_ICONIC]),
  ("Mazza", SLC, "1515", "Long-running Middle Eastern cooking beside the King's English Bookshop.", None, None, [VSL_ICONIC]),
  ("Mahider Ethiopian Restaurant & Market", SLC, "1465", "Stews, spiced lentils and injera platters.", None, None, [VSL_ICONIC]),
  ("Star Of India", SLC, "1000", "Curries with a loyal following.", None, None, [VSL_ICONIC]),
  ("Oquirrh Restaurant", SLC, "368", "A seasonal menu built on Utah farms.", None, None, [VSL_ICONIC]),
  ("Pretty Bird Hot Chicken", SLC, "146", "The Regent Street original of the Nashville hot chicken shop.", None, None, [VSL_ICONIC]),
 ],
 "red rock country": [   # Visit Utah: "Dining Between the Mighty Five" and the Foodie Journey itinerary
  ("Hell's Backbone Grill & Farm", "Boulder", "20", "Farm-to-table on Scenic Byway 12; almost everything on the menu is grown locally.", None, None, [VU_MIGHTY5, VU_FOODIE]),
  ("Burr Trail Grill", "Boulder", "10", "Local lamb burgers and homemade pies.", None, None, [VU_MIGHTY5, VU_FOODIE]),
  ("Sweetwater Kitchen at BMGR", "Boulder", None, "Ranch-to-table at Boulder Mountain Guest Ranch, with beef raised on site.", None, None, [VU_MIGHTY5, VU_FOODIE]),
  ("Capitol Burger", "Torrey", None, "A food truck known for its mac 'n cheese burger.", None, None, [VU_MIGHTY5, VU_FOODIE]),
  ("Hunt & Gather Restaurant", "Torrey", None, "Slow-cooked meals from local ingredients, wild game and fish.", None, None, [VU_MIGHTY5, VU_FOODIE]),
  ("The Wild Rabbit Cafe", "Torrey", None, "House-baked buttermilk biscuits and coffee roasted in town.", None, None, [VU_FOODIE]),
  ("Color Ridge Creamery", "Torrey", None, "Artisanal ice cream: juniper berry, lavender honey.", None, None, [VU_MIGHTY5, VU_FOODIE]),
  ("Torrey Grill & BBQ", "Torrey", None, "Barbecue at the Capitol Reef end of town.", None, None, [VU_MIGHTY5]),
  ("Milt's Stop & Eat", "Moab", None, "A long-running Moab diner with grass-fed burgers.", None, None, [VU_MIGHTY5, VU_FOODIE]),
  ("Josie Wyatt's Grille", "Moab", None, "Steaks, prime rib and seafood on a patio at Hoodoo Moab.", None, None, [VU_MIGHTY5]),
  ("Sabaku Sushi", "Moab", None, "Sushi in the desert, on Center Street.", None, None, [VU_MIGHTY5, VU_FOODIE]),
  ("Arches Thai", "Moab", None, "Thai food a block off Main Street.", None, None, [VU_MIGHTY5]),
  ("Moab Garage", "Moab", None, "Street tacos on Main Street.", None, None, [VU_MIGHTY5]),
  ("Jailhouse Cafe", "Moab", None, "Breakfast in Moab's old jailhouse.", None, None, [VU_FOODIE]),
  ("Doughbird", "Moab", None, "Fried chicken and doughnuts on Main Street.", None, None, [VU_FOODIE]),
  ("Kiva Koffeehouse", "Escalante", None, "Espresso and a hillside view at milepost 73 on Scenic Byway 12.", None, None, [VU_MIGHTY5, VU_FOODIE]),
  ("North Creek Grill", "Escalante", None, "Local cooking in Escalante.", None, None, [VU_FOODIE]),
  ("Stone Hearth Grille", "Tropic", None, "Casual fine dining at the Stone Canyon Inn, near Bryce Canyon.", None, None, [VU_MIGHTY5, VU_FOODIE]),
  ("Tamarisk Restaurant", "Green River", None, "Breakfast on the Green River.", None, None, [VU_FOODIE]),
  ("Cowboy's Smokehouse Cafe", "Panguitch", None, "Western barbecue on Panguitch's Main Street.", None, None, [VU_FOODIE]),
  ("Peekaboo Canyon Wood Fired Kitchen", "Kanab", None, "Wood-fired pizza in Kanab.", None, None, [VU_FOODIE]),
 ],
 "pastrami burger": [   # the Tribune (March 2025), KSL (August 2025), Gastronomic SLC's burgers of 2026
  ("Crown Burgers", SLC, "377", "The downtown Crown Burgers: a quarter-pound burger under a pile of pastrami. Crown began downtown in 1978.", None, None, [TRIB_PASTRAMI, KSL_CROWN]),
  ("Crown Burgers", "Millcreek", "3190", "Crown's Highland Drive store; the family's Millcreek branch opened in 1983.", None, None, [TRIB_PASTRAMI]),
  ("Apollo Burger", SLC, "379", "Apollo's Main Street store: pastrami burgers and the Utah Burger with gyro meat.", None, None, [TRIB_PASTRAMI]),
  ("Yanni's Greek Express", SLC, "2761", "A family-run Sugar House spot that makes a mean pastrami burger.", None, None, [GSLC_BURGERS]),
  ("Golden Gyros", SLC, "259", "The house burger with gyro meat and a judicious side of fry sauce.", None, None, [GSLC_BURGERS]),
 ],
 "pacific islander": [   # KSL (October 2025) and Visit Salt Lake's Pacific Islander page
  ("Pacific Seas Restaurant", SLC, "1151", "A Tongan family's island home cooking: lu, palusami, lamb and otai.", None, None, [KSL_PACSEAS]),
  ("Moki's Hawaiian Grill", "Taylorsville", None, "Plate lunches, musubi and Dole pineapple whip.", None, None, [VSL_PI]),
  ("Bigeye Poke Grill Draper", "Draper", None, "Hawaiian poke in Draper.", None, None, [VSL_PI]),
  ("The Salty Pineapple", "Herriman", None, "Kalua pork, coconut shrimp and guava cake, from a shop and a food truck.", None, None, [VSL_PI]),
 ],
 "utah scones": [],   # waiting for sources (LEADS.md)
 "ski town": [   # Visit Park City's Historic Main Street restaurants (2026-09-11)
  ("Red Banjo Pizza", "Park City", "322", "Park City's oldest restaurant, on Main Street since 1962.", 1962,
   "Visit Park City (September 2026) calls it Park City's oldest restaurant, established in 1962.", [VPC_MAIN]),
  ("No Name Saloon", "Park City", "447", "The buffalo burger, a rooftop patio and several bars.", None, None, [VPC_MAIN]),
  ("Grappa", "Park City", "151", "Rustic Italian at the top of Main Street.", None, None, [VPC_MAIN]),
  ("Chimayo", "Park City", "368", "Southwestern cooking: queso, margaritas, barbecue spareribs.", None, None, [VPC_MAIN]),
  ("Purple Sage", "Park City", "434", "Rustic Western cooking: meatloaf and Utah trout.", None, None, [VPC_MAIN]),
  ("The Eating Establishment", "Park City", "317", "Breakfast, lunch and dinner on Main Street.", None, None, [VPC_MAIN]),
  ("Butcher's Chop House & Bar", "Park City", "751", "A Main Street steakhouse with game and seafood.", None, None, [VPC_MAIN]),
  ("Le Depot Brasserie", "Park City", "660", "French classics in the old Union Pacific depot.", None, None, [VPC_MAIN]),
  ("Firewood", "Park City", "306", "New American cooking over cedar, cherry and maple fires.", None, None, [VPC_MAIN]),
  ("350 Main Brasserie", "Park City", "350", "A globally minded brasserie with a cocktail bar.", None, None, [VPC_MAIN]),
  ("501 on Main", "Park City", "501", "Seasonal American cooking with local produce.", None, None, [VPC_MAIN]),
  ("Courchevel Bistro", "Park City", "201", "French and European bistro cooking at Main and Heber.", None, None, [VPC_MAIN]),
  ("Yuki Yama Sushi", "Park City", "586", "Sushi and noodles in Old Town.", None, None, [VPC_MAIN]),
  ("Cafe Terigo", "Park City", "424", "Northern Italian and southern French cooking, with a patio.", None, None, [VPC_MAIN]),
  ("Handle", "Park City", "136", "A seasonal menu from local and regional ingredients.", None, None, [VPC_MAIN]),
 ],
 "pie stop": [   # Visit Utah's "Pie-Ala-Road" pie trail
  ("Thunderbird Restaurant", "Mount Carmel", None, "\"Ho-made\" pies at the junction of Route 9 and US 89, on the way to Zion.", 1931,
   "Visit Utah ties the Thunderbird's pies to founder Jack Morrison and 1931.", [VU_PIE]),
  ("Veyo Pies", "Veyo", None, "The state's biggest pie selection, north of St. George: try the Veyo Volcano.", None, None, [VU_PIE]),
  ("Bryce Canyon Pines Restaurant", "Bryce Canyon City", None, "Pie on Scenic Byway 12, just before the Bryce Canyon turnoff.", None, None, [VU_PIE]),
  ("Burr Trail Grill", "Boulder", "10", "Made-from-scratch pies, many with fruit grown nearby.", None, None, [VU_MIGHTY5]),
 ],
 "oldest": [
  ("Shooting Star Saloon", "Huntsville", None, "Burgers, chips and beer under the taxidermy.", 1879,
   "Tasting Table (February 2025) names it Utah's oldest bar, established in 1879 as Hoken's Hole.", [TT_OLDBAR]),
  ("Thunderbird Restaurant", "Mount Carmel", None, "Pies on the road to Zion.", 1931, "Visit Utah ties the Thunderbird to founder Jack Morrison and 1931.", [VU_PIE]),
  ("Ruth's Diner", SLC, "4160", "The trolley-car diner up Emigration Canyon.", 1949,
   "Opened downtown in 1930 as Ruth's Hamburgers; at this Emigration Canyon address since 1949 (Utah Stories, October 2025).", [US_RUTHS, VSL_ICONIC]),
 ],
}
# the dated pages print these street addresses; placed by utah.py when the map data lacks the place
ADDR = {}
CUISINE = {("Pacific Seas Restaurant", SLC): "Hawaiian & Pacific Islander", ("The Salty Pineapple", "Herriman"): "Hawaiian & Pacific Islander",
           ("Thunderbird Restaurant", "Mount Carmel"): "American & Other", ("Burr Trail Grill", "Boulder"): "American & Other",
           ("Ruth's Diner", SLC): "Breakfast & Diner", ("Color Ridge Creamery", "Torrey"): "Bakery & Sweets",
           ("Feldman's Deli", SLC): "Sandwiches & Deli", ("Shooting Star Saloon", "Huntsville"): "Burgers"}
KINDS = {k: [k] for k in ("salt lake classic", "red rock country", "pastrami burger", "pacific islander", "utah scones", "ski town",
                          "pie stop", "oldest")}

# MICHELIN Guide Southwest, 2026 (Utah's nine; guide.michelin.com, 2026-11-05)
MICHELIN = [("Monte", "South Salt Lake", "1 Star", "Contemporary"),
            ("Feldman's Deli", SLC, "Bib Gourmand", "Deli"), ("One More Noodle House", "South Salt Lake", "Bib Gourmand", "Chinese"),
            ("Phở 777", "West Valley City", "Bib Gourmand", "Vietnamese"),
            ("Handle", "Park City", "Recommended", "Contemporary"), ("Matilda", "Park City", "Recommended", "Pizza"),
            ("The Nelson Cottage by High West", "Park City", "Recommended", "American"), ("Star of India", SLC, "Recommended", "Indian"),
            ("Koyote", SLC, "Recommended", "Ramen")]
MI_MATCH = {"The Nelson Cottage by High West": ["NELSON COTTAGE"], "Phở 777": ["PHO 777"]}
# James Beard (facts with sources): Utah's 2025-26 nominees (finalists) and semifinalists; no Utah winner in 2025 or 2026
JBF = [{"name": "Felt Bar & Eatery", "city": SLC, "honors": ["Best Chef: Mountain finalist 2026 (Travis Herbert)"], "sources": [JBF26N, JBF26]},
       {"name": "Urban Hill", "city": SLC, "honors": ["Best Chef: Mountain finalist 2026 (Nick Zocco)"], "sources": [JBF26N, JBF26, JBF25]},
       {"name": "Oquirrh", "city": SLC, "honors": ["Best Chef: Mountain semifinalist 2026 (Andrew Fuller)"], "sources": [JBF26, JBF25], "match_names": ["OQUIRRH RESTAURANT"]},
       {"name": "Arlo", "city": SLC, "honors": ["Best Chef: Mountain semifinalist 2026 (Milo Carrier)"], "sources": [JBF26], "match_names": ["ARLO RESTAURANT"]},
       {"name": "The Pearl", "city": SLC, "honors": ["Best Chef: Mountain semifinalist 2026 (Tommy Nguyen)"], "sources": [JBF26]},
       {"name": "Post Office Place", "city": SLC, "honors": ["Outstanding Bar semifinalist 2026"], "sources": [JBF26]},
       {"name": "Table X", "city": SLC, "honors": ["Best Chef: Mountain semifinalist 2025 (Mike Blocher and Nick Tramp)"], "sources": [JBF25]},
       {"name": "Manoli's", "city": SLC, "honors": ["Outstanding Hospitality semifinalist 2025"], "sources": [JBF25]},
       {"name": "Water Witch", "city": SLC, "honors": ["Outstanding Bar finalist 2025"], "sources": [JBF25N, JBF25]},
       {"name": "Fillings & Emulsions", "city": SLC, "address": "1475 S Main St", "honors": ["Outstanding Pastry Chef or Baker semifinalist 2025 (Adalberto Diaz)"], "sources": [JBF25]},
       {"name": "Tupelo Park City", "city": "Park City", "honors": ["Best Chef: Mountain semifinalist 2025 (Matthew Harris)"], "sources": [JBF25]}]
# closed, each with a source (none verified this pass)
CLOSED = []


def key(s):
    """The name key without a leading "the": "Varsity" is our "The Varsity"."""
    return re.sub(r"^the ", "", norm(s))


def find(name, town, num):
    k = key(name)
    hits = [i for i, n in enumerate(C["name"]) if C["city"][i] is not None and M["cities"][C["city"][i]] == town
            and (key(n) == k or key(n).startswith(k + " ") or k.startswith(key(n) + " ") or key(n).replace(" ", "") == k.replace(" ", "")
                 or (key(n).split()[:2] == k.split()[:2] and len(k.split()) >= 2))]
    if num:
        hits = [i for i in hits if (C["addr"][i] or "").split(" ")[0] == num]
    return hits


leads, n_out = [], {}
for kind, rows in GUIDES.items():
    out = []
    for name, town, num, note, founded, fnote, srcs in rows:
        hits = find(name, town, num)
        if not hits and (name, town) in ADDR:
            out.append({"name": name, "address": ADDR[(name, town)], "city": town, "zip": None, "kinds": KINDS[kind], "dishes": [], "note": note,
                        "founded": founded, "founded_note": fnote, "website": None, "open": True, "evidence_date": "2026-10",
                        "sources": srcs, "match_names": []} | ({"cuisine": CUISINE[(name, town)]} if (name, town) in CUISINE else {}))
            continue
        if len(hits) != 1:
            leads.append(f"- {kind}: {name} ({town}{', ' + num if num else ''}) — {len(hits)} matches in our data; not added"); continue
        i = hits[0]
        out.append({"name": C["name"][i], "address": C["addr"][i], "city": town, "zip": str(C["zip"][i]) if C["zip"][i] else None,
                    "kinds": KINDS[kind], "dishes": [], "note": note, "founded": founded, "founded_note": fnote, "website": None, "open": True,
                    "evidence_date": "2026-10", "sources": srcs, "match_names": [name.upper()] if norm(name) != norm(C["name"][i]) else []})
        if brand_of(norm_name(name)):   # a chain shows under its own spelling at every branch, whatever the listing says
            out[-1]["display"] = name
        if (name, town) in CUISINE:
            out[-1]["cuisine"] = CUISINE[(name, town)]
    fn = re.sub(r"[^a-z]+", "_", kind).strip("_")
    json.dump(out, open(f"{R}/app/{fn}.json", "w"), indent=1, ensure_ascii=False)
    n_out[kind] = len(out)

# a name norm_name can't tell apart ("Phở 777" keeps only PHO) is pinned by the street address of our own listing for it
MI_ADDR = {"Phở 777": "3585 S Redwood Rd"}
json.dump({"restaurants": [{"name": n, "address": MI_ADDR.get(n), "city": t, "zip": None, "distinction": dist, "cuisine": cu, "green_star": False,
                             "michelin_url": MI_UT, "sources": [MI_UT], "match_names": [x.upper() for x in MI_MATCH.get(n, [])], "open": True}
                            for n, t, dist, cu in MICHELIN]}, open(f"{R}/michelin.json", "w"), indent=1, ensure_ascii=False)
json.dump([dict({"address": None}, **j, zip=None, open=True) for j in JBF], open(f"{R}/jbf.json", "w"), indent=1, ensure_ascii=False)
json.dump(CLOSED, open(f"{R}/closed.json", "w"), indent=1, ensure_ascii=False)
open(f"{R}/app/LEADS.md", "w").write("# Utah research leads (not yet verified)\n\nWritten by pipeline/build_research.py.\n\n" + "\n".join(leads) + """

## Waiting for a 2025-26 source we may use
- Utah scones and fry bread: Sill's Cafe (335 E Gentile St, Layton; City Weekly's Best of Utah 2025 "Best Fried Scones", but
  cityweekly.net answers 403 to our fetcher), Navajo Hogan (South Salt Lake; Visit Salt Lake's listing calls it "American & Burgers"
  and doesn't mention fry bread), Totally Sconed (American Fork; Fox 13's page has no date). The guide shows once it has three.
- Pastrami burgers: Astro Burgers (the Tribune's March 2025 piece names it without a town), Atlantis Burgers (North Salt Lake),
  Lucky 13 (City Weekly, blocked). Salt Lake Magazine's pastrami-burger field guide sits behind a bot check.
- Pacific Islander: Poke Luau (Midvale; on Visit Salt Lake's Pacific Islander page) isn't in our map data; Sagato Bakery (2024 page only).
- Red rock country: Escalante Outfitters, Magnolia's Kitchen, Mimi's Bakery and Deli, Georgie's Outdoor Mexican Restaurant (Escalante),
  i.d.k. Barbecue (Tropic), Archie's Food to Die For (Orderville), Kenny Rays (Panguitch) and Sunglow Café (Bicknell) are on Visit
  Utah's pages but not in our map data; Gifford House (Capitol Reef, pies in season) sits inside the national park.
- Ski towns: Riverhorse on Main, High West Distillery & Saloon, Loma and Top of Main Brew Pub (Visit Park City, 2026-09-11) aren't in
  our map data under those names.
- Honors: Koyote (MICHELIN recommended, Salt Lake City), Junah (James Beard Best New Restaurant semifinalist 2026) and Alpine
  Distilling Social Aid & Pleasure Club (Park City; Sara Sergent, beverage semifinalist 2026) aren't in our map data.
- Oldest: The Bluebird (Logan, 1914; Tasting Table, September 2025) is closed for renovation since 2020; Idle Isle Café (Brigham City,
  1921) closed in May 2025. Crown Burgers began downtown in 1978, but in the building just east of today's store (KSL, August 2025).
- Blocked or unusable hosts: saltlakemagazine.com (bot check), cityweekly.net (403), utahbusiness.com (robots), opendata.utah.gov
  (no longer a catalog).
""")
print(n_out, "| leads:", len(leads))
for l in leads: print(l)
