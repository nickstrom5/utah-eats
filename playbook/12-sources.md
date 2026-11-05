# Utah sources (checked 2026-11-05)

Every cited host was robots-checked with `pipeline/check_sources.py` (ClaudeBot, Claude-User and anthropic-ai; RFC 9309 matcher) before
use. User agents: `BeehiveEatsSourceCheck/1.0` and `BeehiveEatsLinkCheck/2.0` (+nick@eatsranked.com).

## Official records: none a script may read
- **Alcohol:** the Department of Alcoholic Beverage Services licenses every on-premises seller. Its 2026 licensing system publishes no
  licensee list we found; `state-prompts/UTAH_PROMPT.md` mentions a Looker Studio "Licensee List" linked from
  abs.utah.gov/licenses-permits/license-information/ (export and terms unchecked). A GRAMA request is Nick's call. Until then "Serves
  alcohol" is unknown ("—") everywhere, never "no".
- **Inspections:** 13 local health departments (Bear River, Central Utah, Davis, Salt Lake County, San Juan, Southeast Utah, Southwest
  Utah, Summit, Tooele, TriCounty, Utah County, Wasatch, Weber-Morgan), linked through the Utah Association of Local Health Departments
  (ualhd.org, 200 on 2026-11-05). Salt Lake County's page says its Inspection Reports are "the only official source" for its inspections:
  1, 3 or 6 points per violation (lower is better) and a 0-100% percentile rank within risk level, no letter grade (read 2026-11-05).
  Search-only; never scraped. The prompt names two public ArcGIS layers with no license stated: Summit County's
  (`Summit_County_Food_Public_2025`, a county TOTAL_SCORE out of 100, about 1,400 inspections since October 2024) and TriCounty's
  Survey123 layer (about 430 inspections since July 2025, addresses but no names). Using them is Nick's call; not built.
- **Lists:** opendata.utah.gov no longer answers as a catalog (400; "Domain not found" in Socrata's catalog); Salt Lake City publishes no
  business licenses we found. UDAF inspects groceries, bakeries and food plants, not restaurants.

## Listings and outlines
- Overture Maps places and addresses, release 2026-10-21.0 (CDLA Permissive 2.0 / Apache 2.0 / CC0 per source; addresses under open
  licenses). 13,035 eating and drinking listings in Utah; 1.48 million Utah address points.
- Overture divisions (ODbL, © OpenStreetMap contributors): the state and Utah's 29 counties, land class (the lakes out, their islands
  and shores in).
- The keep rule is the family's: Meta confidence 0.95, or 0.90 with a website, chain store lists and hand-checked places. With no
  official list to measure against in Utah, `calibrate.py` reports only the share Google's Sep 2021 snapshot still showed open
  (private, web build only): Meta-high 70.5%, Meta-mid with a website 48.4%, Meta-low 4.9%.
- Benchmark: Census CBP 2023, 6,178 NAICS 722 establishments in Utah (the prompt). The app keeps 6,167 restaurants.

## Honors
- **MICHELIN Guide Southwest**, first selection (revealed in Las Vegas in August 2026; Michelin's release 2026-08-31):
  guide.michelin.com/us/en/utah/restaurants lists 9 Utah places. Monte (1 Star, South Salt Lake); Bib Gourmands Feldman's Deli, One
  More Noodle House, Phở 777; Recommended Handle, Matilda, The Nelson Cottage by High West, Star of India, Koyote (not in our map data).
  The prompt's "American Southwest" isn't Michelin's name.
- **James Beard:** 2026 nominees Travis Herbert (Felt Bar & Eatery) and Nick Zocco (Urban Hill), Best Chef: Mountain (2026-03-31); 2026
  semifinalists (2026-01-21) and 2025 semifinalists (2025-01-22) from jamesbeard.org. No Utah winner in 2025 or 2026. Restaurateur
  honors (Saffron Valley) aren't shown on places.

## Hand-checked guides (each place: a dated 2025-26 page or an official tourism listing)
Visit Salt Lake (15 iconic restaurants, 2026-06-09; Pacific Islander page), Visit Utah (dining between the national parks, the foodie
itinerary, the pie trail), Visit Park City (Historic Main Street restaurants, 2026-09-11), the Salt Lake Tribune (pastrami burgers,
2025-03-11), KSL (Crown Burgers 2025-08-07; Pacific Seas 2025-10-17), Gastronomic SLC (best burgers 2026), Utah Stories (Ruth's Diner,
2025-10-18), Tasting Table (oldest bar in every state, 2025-02-17). Unusable: saltlakemagazine.com (bot check), cityweekly.net (403),
utahbusiness.com (robots). Leads waiting for a source: `data/research/app/LEADS.md`.
