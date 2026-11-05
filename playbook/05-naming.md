# Utah brand: provisional (2026-11-05), waiting for Nick's calls

Built while Nick was away, so every choice below is a placeholder in the pattern he picked for the other states. Changing any of
them is cheap: the display name and copy, `scripts/make-brand.swift` (icon, favicons, share image), `Design/Theme.swift`, the site
palette in `scripts/make-site.py`, then the screenshots again.

## Name (Nick decides)
- **Used for now: "Beehive Eats: Utah Restaurants"**, Home Screen **"Beehive Eats"**, tagline **"Pastrami Burgers, Pie & Red Rock"**.
  One of the prompt's three options; a web search (2026-11-05) found no business, app or publication by that name ("Beehive Meals" is
  a meal-delivery company). Not checked in the App Store or for trademarks.
- **Not "Utah Eats":** the Salt Lake Tribune runs a "Utah Eats" food beat with its own reporter (the prompt's first option).
- **The prompt's third option:** "Fry Sauce: Utah Restaurants" (Arctic Circle sells fry sauce; check marks first).
- **Avoid** (from the prompt): "Life Elevated" (state brand), "The Mighty 5®" (state tourism), "The Greatest Snow On Earth®" (Ski Utah),
  "Deseret". The site's copy says "Utah's national parks" rather than the Mighty 5 mark.
- Bundle id `com.utaheats.ios` and repo name `utah-eats` are neutral; they don't need to change with the name.

## Icon (Nick picks one of three; `scripts/icon-concepts.swift`, PNGs in `playbook/brand/`; all three pass `check.swift`)
- **A (used for now)** fries in a red carton with a cup of pink fry sauce beside it, on flag navy. Reads clearly at 60 px.
- **B** a puffy Utah scone with a pat of honey butter and a honey drizzle. Passes, but at 60 px the drips read as table legs.
- **C** a dirty soda: a white cup of cola, a red straw, a lime wedge. Passes; reads as a drink.

## Palette (provisional): the 2024 state flag (the prompt's set)
Flag navy #071D49 (16.4:1 on white) for titles and accents; flag red #AA0200 as the guide-card fill under white text (7.7:1); flag
amber #FFB81D only as a fill under navy text (as text on white it's 1.7:1); snow-white #FAF7F0 page; accents red-rock sandstone #B5451B
and Great Salt Lake teal #1F6E78. Navy and red are balanced so neither reads as a school (Utes red, BYU blue, Utah State). The header
band is the prompt's idea: a five-peak Wasatch skyline (the new flag's peaks) on a red-rock baseline, ending in a sandstone arch.
