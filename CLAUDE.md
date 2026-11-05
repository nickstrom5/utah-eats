# Beehive Eats (ut-eats) — notes for Claude Code sessions

Built 2026-11-05 by a side session for Nick's "build Utah, Vermont, Virginia, West Virginia and Wyoming", ported from `../md-eats/`
with every fix to that day (the 10-29 all-states QA P0/P1s, Nevada's `name_key()` ids, the narrowed loan rule, the exact-outline county
lookup, the out-of-county truck rule, the web map frame and Back key). Local only: git-ignored data, no repo, no remote, nothing
published. Sources and calibration: `playbook/12-sources.md`. Brand: `playbook/05-naming.md` — **provisional**, every choice waits for
Nick ("Beehive Eats: Utah Restaurants", Home Screen "Beehive Eats"; "Utah Eats" is the Salt Lake Tribune's food beat; fries-and-fry-sauce
icon A on flag navy; the 2024 state flag palette from `state-prompts/UTAH_PROMPT.md`: navy #071D49, red #AA0200, amber #FFB81D fill only,
sandstone and teal accents; a five-peak Wasatch skyline band ending in a red-rock arch).

## Utah is different
- **No official list a script may read.** DABS publishes no licensee list (the prompt's Looker Studio report is unchecked), the 13 local
  health departments' inspections are search-only, opendata.utah.gov is gone, Salt Lake City publishes no licenses. `official.load()`
  returns an empty table with the usual columns; the pipeline runs on it (0 official places, "Serves alcohol" unknown everywhere, no
  inspection results). The prompt names two public ArcGIS inspection layers with no license stated (Summit County, TriCounty): Nick's
  call, not built.
- **Counties:** Utah's 29 from Overture's land division areas; Antelope Island, Bullfrog and Bear Lake inside; Wendover in, West
  Wendover and Fredonia out (`fetch_overture.py` checks them). **Regions** (8): Salt Lake Valley, Utah Valley, Ogden & Davis, Cache
  Valley & Box Elder, Park City & the Uintas, Southern Utah, Central Utah & West Desert, Moab & Eastern Utah.
- **Merge and matcher fix (2026-11-05):** a listing's own street word ("MAIN" for 501 Main St) no longer counts as a shared name word
  in the duplicate merge (it folded Park City's "501 on Main" into "Riverhorse on Main" 70 m away in the App Store build), and the
  research matcher's statewide fallback needs the researched street (it had renamed South Salt Lake's "Cafe On Main"). Last full run
  2026-11-05: app 6,346 places / 6,168 restaurants, OTA 2026-11-05.1 (rewritten after the ZIP fix; nothing published), 49 unit tests on iPhone 17 Pro Max (iOS 27.0), 13 iPhone + 6
  iPad screens, `qa-site.py --static` OK.
- **Honors:** the MICHELIN Guide Southwest (first selection August 2026: Monte one star; Bib Gourmands Feldman's Deli, One More Noodle
  House, Phở 777; five recommended, Koyote not in our map data) and James Beard 2025-26 nominees and semifinalists. Honors are facts.
- **Guides** (tags in `utah.py` TAGS; bits 1..128): Salt Lake classics (Visit Salt Lake, June 2026), red rock country (Visit Utah),
  pastrami burgers & fry sauce (Tribune 2025, KSL 2025, Gastronomic SLC 2026), Pacific Islander (KSL 2025, Visit Salt Lake), Utah scones
  (empty: waiting for sources, `data/research/app/LEADS.md`), ski towns (Visit Park City, Sept 2026), pie stops (Visit Utah's pie trail),
  oldest (Shooting Star Saloon 1879, Thunderbird 1931, Ruth's Diner 1949 at its canyon address).
- **Adult rule** adds Southern X-Posure (two listings linking its parked domain) to the family-wide rule.
- **Ranking:** "Featured first" (honors, then founding year), as everywhere until Nick decides on the all-factor Ranked score
  (`eats-ranked-score-all-states-proposal-2026-11-05.md` in the shared notes). The export already carries its inputs (hand-checked,
  honors, founding year, chain count); no health-grade wording anywhere.

## Rebuild
```bash
cd pipeline
../.venv/bin/python check_sources.py URL...   # a new host first
../.venv/bin/python fetch_overture.py && ../.venv/bin/python fetch_extras.py && ../.venv/bin/python fetch_official.py
../.venv/bin/python geocode_official.py && ../.venv/bin/python geocode_census.py && ../.venv/bin/python listings.py
../.venv/bin/python calibrate.py && ../.venv/bin/python utah.py && ../.venv/bin/python build_research.py && ../.venv/bin/python utah.py
UT_APP=1 ../.venv/bin/python utah.py && cd .. && cp data/app/places.json data/app/detail-*.json UtahEats/Resources/
.venv/bin/python pipeline/check_websites.py --retry-transient   # link verification; re-export after
.venv/bin/python scripts/make-site.py && .venv/bin/python scripts/publish_app_data.py && .venv/bin/python scripts/publish_app_data.py --check
.venv/bin/python scripts/qa-site.py --static
```
(`listings.py` must run before `calibrate.py`, and `utah.py` once before `build_research.py`, which matches names against
`site/utah.json`.) The `.venv` is on the python.org framework Python 3.12 (Homebrew's python@3.12 is gone), with md-eats' versions.
`data/ucsd/meta-Utah.json.gz` (Google 2021, private, web build only) comes from mcauleylab.ucsd.edu's googlelocal set.

## App, site, screenshots
- App: `UtahEats/` (XcodeGen `project.yml`, bundle `com.utaheats.ios`, display "Beehive Eats"), tests in `UtahEatsTests/` (data guards:
  adult venues, blocklisted and multi-URL websites, bad and legal names, non-restaurants, listed twice, no Google data; MICHELIN; the
  outline with Wendover). Run tests: `DEVELOPER_DIR="/Applications/Xcode 1.app/Contents/Developer" xcodebuild test ...
  CODE_SIGNING_ALLOWED=NO` on a temporary simulator. Archive only with Xcode 1.app (now 27.2, 27B52); Xcode.app is a beta.
  Run `xcodegen generate` after the export whenever the set of `Resources/*.json` files changes (an app built without them still
  compiles but opens on "Couldn't open the list").
- Site: `scripts/make-site.py` writes `docs/` (18 pages; city pages Salt Lake City, Park City, Moab, Torrey) and
  `playbook/site-numbers.json`; `scripts/explore.js` is the web app; `scripts/qa-site.py` the QA. Site URL for now:
  nickstrom5.github.io/utah-eats (no CNAME). Rebuild the site before the unit tests: `ShareLinkTests` reads the web app's ids from `docs/`.
- OTA data: `docs/data/app/` via `scripts/publish_app_data.py` (`../OTA-DATA.md`).
- Screenshots: `scripts/capture-screenshots.sh <sim>` (ScreenshotMode pins downtown Salt Lake City; Torrey for red rock, Park City for
  ski towns, Bryce Canyon City for pies), then `scripts/site-images.sh`, then make-site + qa-site. App Store frames:
  `scripts/appstore-screenshots.py`. Icons: `scripts/icon-concepts.swift` (A fries and fry sauce, B scone, C dirty soda; all pass
  `state-prompts/icon-style/check.swift`; B reads as a small table at 60 px) and `scripts/make-brand.swift`.
- Not ported: the App Store listing writer and the private Google-2021 leaderboard. `site/` holds the leaderboard's data and is
  git-ignored with `data/`.

## Fixes after the first build (2026-11-05)
- **UI test:** the "my location" map check used Baltimore's Inner Harbor (from md-eats); now this state's own downtown.
- **Last full run** 2026-11-05: 49 unit tests, the detail and 6 iPad screens re-captured after the ZIP fix, `qa-site.py
  --static` OK, OTA 2026-11-05.1 (local only).
- **ZIPs:** the export (`pipeline/utah.py`, the place's `z` and the address-strip pattern) still kept only Maryland's 206xx-219xx, carried
  from md-eats, so the app showed addresses without a ZIP and ZIP search found little. Now this state's own range (84xxx); the
  detail screenshot was re-captured.

## Rules
No commits, pushes, public repos, App Store Connect or DNS changes without Nick's yes each time; never submit for review or accept
agreements; never publish Google-derived data. Support email nick@eatsranked.com. Commit author "Nick Soderstrom"
<329204362+nickstrom5@users.noreply.github.com> via `-c user.name -c user.email`.
