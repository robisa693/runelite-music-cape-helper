#!/usr/bin/env python3
"""Targeted pass: add "mapId" to existing track_coords.json locations.

Only re-fetches pages for tracks that have at least one mid-band location
(4160 <= y < 6400) - those are the self-contained zones (Rat Pits, Keldagrim,
...) whose wiki mapID we need to resolve a surface entrance. Existing entries
are patched in place by matching centers; nothing else is changed.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scrape_track_coords import (  # noqa: E402
    OUTPUT_FILE,
    build_locations_from_inline_maps,
    extract_infobox_map_ref,
    extract_inline_maps,
    get_wikitext,
    parse_subpage_data,
)


def needs_mapid(locs):
    for l in locs:
        c = l.get("center")
        if c and len(c) >= 3 and 4160 <= c[1] < 6400 and "mapId" not in l:
            return True
    return False


def scrape_page_locations(track):
    """Re-derive this track's locations (with mapId) from the wiki."""
    for title in (track, track + " (music track)"):
        wt = get_wikitext(title)
        if wt:
            break
    if not wt:
        return []

    locations = []
    subpage = extract_infobox_map_ref(wt)
    if subpage:
        sub_wt = get_wikitext(subpage)
        if sub_wt:
            sub_data = parse_subpage_data(sub_wt)
            if sub_data:
                entry = {"center": sub_data["center"] + [sub_data["plane"]]}
                if sub_data.get("mapId") is not None:
                    entry["mapId"] = sub_data["mapId"]
                locations.append(entry)
            else:
                locations.extend(build_locations_from_inline_maps(extract_inline_maps(sub_wt), locations))
    locations.extend(build_locations_from_inline_maps(extract_inline_maps(wt), locations))
    return locations


def main():
    with open(OUTPUT_FILE) as f:
        data = json.load(f)

    todo = [t for t, locs in data.items() if needs_mapid(locs)]
    print(f"{len(todo)} tracks need mapId lookup")

    patched = 0
    unmatched = []
    for i, track in enumerate(todo):
        if (i + 1) % 25 == 0:
            print(f"  {i + 1}/{len(todo)}...")
        fresh = scrape_page_locations(track)
        by_center = {}
        for l in fresh:
            c = l.get("center")
            if c and l.get("mapId") is not None:
                by_center[(round(c[0], 1), round(c[1], 1), int(c[2]))] = l["mapId"]
        for l in data[track]:
            c = l.get("center")
            if not c or len(c) < 3 or "mapId" in l:
                continue
            key = (round(c[0], 1), round(c[1], 1), int(c[2]))
            if key in by_center:
                l["mapId"] = by_center[key]
                patched += 1
            elif 4160 <= c[1] < 6400:
                unmatched.append((track, key))

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\npatched {patched} locations with mapId")
    print(f"{len(unmatched)} mid-band locations without a mapId:")
    for t, k in unmatched[:40]:
        print(f"  {t} @ {k}")


if __name__ == "__main__":
    main()
