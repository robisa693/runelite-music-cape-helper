#!/usr/bin/env python3
"""Scrape each track's infobox `location` field from the OSRS Wiki into
wiki_locations.json - a human-readable place name shown by the plugin when it
falls back to the wiki (empty coords or unmappable zones)."""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scrape_track_coords import OUTPUT_FILE, get_wikitext  # noqa: E402

OUT = os.path.join(os.path.dirname(OUTPUT_FILE), "wiki_locations.json")


def strip_wikitext(v):
    v = re.sub(r'\[\[[^\]|]*\|([^\]]+)\]\]', r'\1', v)   # [[A|B]] -> B
    v = re.sub(r'\[\[([^\]]+)\]\]', r'\1', v)              # [[A]] -> A
    v = re.sub(r'\{\{[^{}]*\}\}', '', v)                    # drop templates
    v = re.sub(r'<[^>]+>', '', v)                           # drop html
    return v.strip(" \t*")


def main():
    with open(OUTPUT_FILE) as f:
        tracks = list(json.load(f).keys())
    out = {}
    for i, track in enumerate(tracks):
        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(tracks)}... ({len(out)} found)")
        for title in (track, track + " (music track)"):
            wt = get_wikitext(title)
            if wt:
                break
        if not wt:
            continue
        m = re.search(r'\|\s*location\s*=\s*(.+)', wt)
        if m:
            loc = strip_wikitext(m.group(1))
            if loc and loc.lower() not in ("no", "n/a", "unknown", "none"):
                out[track] = loc
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, sort_keys=True)
    print(f"wrote {OUT}: {len(out)} tracks with a location name")


if __name__ == "__main__":
    main()
