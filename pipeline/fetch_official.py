"""Utah's open official records -> data/raw/official/ (git-ignored, never public). Nothing to fetch yet.

Checked 2026-11-05 (playbook/12-sources.md): the Department of Alcoholic Beverage Services publishes no licensee list (its 2026 licensing
system has none); Utah's 13 local health departments publish inspections only through search pages (Salt Lake County: "the only
official source"); opendata.utah.gov no longer answers as a Socrata catalog; Salt Lake City publishes no business licenses. When a list
turns up (a GRAMA response, a county dataset), add its loader to official.py and its download here, after check_sources.py clears the
host, one request at a time, with no owner or person names requested.
"""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "official")
os.makedirs(OUT, exist_ok=True)
json.dump({}, open(os.path.join(OUT, "meta.json"), "w"))
print("Utah: no official list to fetch (see the docstring)")
