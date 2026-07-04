#!/usr/bin/env python3
"""Scrape music track coordinates from OSRS Wiki.

Extracts polygon/area coordinates from each track page and Map: subpages,
computes centroids, and outputs track_coords.json.
"""

import json
import os
import re
import sys
import time
from urllib.parse import quote

import requests

API = "https://oldschool.runescape.wiki/api.php"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "src", "main", "resources")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "track_coords.json")
MISSING_CATEGORY = "Category:Missing_track_location"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "MusicCapeHelperCoordScraper/1.0"})

def api_call(params):
    params["format"] = "json"
    time.sleep(0.35)
    resp = SESSION.get(API, params=params)
    resp.raise_for_status()
    return resp.json()

def get_category_members(category, limit=500):
    pages = []
    cmcontinue = None
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": category,
            "cmlimit": min(limit, 500),
        }
        if cmcontinue:
            params["cmcontinue"] = cmcontinue

        data = api_call(params)
        for m in data.get("query", {}).get("categorymembers", []):
            pages.append(m["title"])

        cont = data.get("continue", {})
        cmcontinue = cont.get("cmcontinue")
        if not cmcontinue:
            break
    return pages

def get_wikitext(title):
    data = api_call({
        "action": "parse",
        "page": title,
        "prop": "wikitext",
        "redirects": 1,
    })
    parsed = data.get("parse")
    if not parsed:
        return None
    wt = parsed.get("wikitext", {}).get("*")
    return wt

def parse_coord_pair(text):
    text = text.strip()
    m = re.match(r'(\d+\.?\d*)\s*,\s*(\d+\.?\d*)', text)
    if m:
        return [float(m.group(1)), float(m.group(2))]
    return None

def parse_inline_map_template(content):
    content = content.strip()
    parts = [p.strip() for p in content.split("|")]
    coords = []
    params = {}
    for part in parts:
        if "=" in part:
            k, v = part.split("=", 1)
            params[k.strip()] = v.strip()
        else:
            pair = parse_coord_pair(part)
            if pair:
                coords.append(pair)
    plane = int(params.get("plane", "0"))
    map_id = params.get("mapID", "-1")
    mtype = params.get("mtype", "")
    group = params.get("group", "")
    bucket = params.get("bucket", "")
    return {
        "coords": coords,
        "plane": plane,
        "mapID": map_id,
        "type": mtype,
        "group": group,
        "bucket": bucket,
    }

def extract_inline_maps(wikitext):
    maps = []
    pattern = r'\{\{Map\|([^}]+)\}\}'
    for m in re.finditer(pattern, wikitext):
        parsed = parse_inline_map_template(m.group(1))
        if len(parsed["coords"]) >= 2:
            maps.append(parsed)
    return maps

def extract_infobox_map_ref(wikitext):
    m = re.search(r'\|\s*map\s*=\s*\{\{Map:([^}]+)\}\}', wikitext)
    if m:
        subpage = "Map:" + m.group(1).strip()
        return subpage
    return None

def parse_subpage_data(wikitext):
    x_m = re.search(r'\|\s*x\s*=\s*([\d.]+)', wikitext)
    y_m = re.search(r'\|\s*y\s*=\s*([\d.]+)', wikitext)
    if not x_m or not y_m:
        return None
    center = [float(x_m.group(1)), float(y_m.group(1))]

    plane = 0
    plane_m = re.search(r'\|\s*plane\s*=\s*(\d+)', wikitext)
    if plane_m:
        plane = int(plane_m.group(1))

    polygon = []
    pt_pattern = re.compile(r'\[(\d+\.?\d*)\s*,\s*(\d+\.?\d*)\]')
    for match in pt_pattern.finditer(wikitext):
        polygon.append([float(match.group(1)), float(match.group(2))])

    return {
        "center": center,
        "plane": plane,
        "polygon": polygon,
    }

def centroid(coords):
    if not coords:
        return None
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    return [round(sum(xs) / len(xs), 1), round(sum(ys) / len(ys), 1)]

def resolve_inline_map_name(wikitext):
    m = re.search(r'\|\s*link\s*=\s*([^|}]+)', wikitext)
    if m:
        return m.group(1).strip()
    m = re.search(r'\|\s*mapname\s*=\s*([^|}]+)', wikitext)
    if m:
        return m.group(1).strip()
    return None

def main():
    print("Fetching music track pages...")
    all_pages = get_category_members("Category:Music_tracks")
    print(f"  Found {len(all_pages)} pages total")

    print("Fetching missing-track-location pages...")
    missing_pages = set(get_category_members(MISSING_CATEGORY))
    print(f"  {len(missing_pages)} pages have no location data")

    output_data = {}

    skipped_pages = {"7th Realm"}

    for i, page in enumerate(all_pages):
        if page in skipped_pages:
            continue

        if (i + 1) % 50 == 0:
            print(f"  Processing page {i + 1}/{len(all_pages)}...")

        wt = get_wikitext(page)
        if wt is None:
            print(f"  WARNING: Could not fetch wikitext for {page}")
            continue

        track_name = page.replace(" (music track)", "").strip()
        if track_name == page:
            track_name = page

        locations = []

        in_missing = page in missing_pages

        if not in_missing:
            subpage = extract_infobox_map_ref(wt)
            if subpage:
                sub_wt = get_wikitext(subpage)
                if sub_wt:
                    sub_data = parse_subpage_data(sub_wt)
                    if sub_data:
                        loc_name = resolve_inline_map_name(sub_wt) or subpage.replace("Map:", "").replace(" music", "").strip()
                        full_center = sub_data["center"] + [sub_data["plane"]]
                        locations.append({
                            "name": loc_name,
                            "center": full_center,
                            "polygon": sub_data["polygon"],
                        })

            inline_maps = extract_inline_maps(wt)
            current_bucket_regions = {}
            for im in inline_maps:
                if im["bucket"] and im["group"]:
                    key = f"{im['bucket']}_{im['group']}"
                    if key not in current_bucket_regions:
                        current_bucket_regions[key] = []
                    current_bucket_regions[key].append(im)

            multi_group_seen = set()
            for im in inline_maps:
                c = centroid(im["coords"])
                if not c:
                    continue
                full_center = c + [im["plane"]]

                if im["group"] and im["group"] not in multi_group_seen:
                    multi_group_seen.add(im["group"])
                    loc_name = f"Region {im['group']}" if im["group"] else "Location"
                else:
                    loc_name = "Location"

                if im["bucket"]:
                    loc_name = f"{loc_name} ({im['bucket']})"

                if not any(loc["center"] == full_center for loc in locations):
                    locations.append({
                        "name": loc_name,
                        "center": full_center,
                        "polygon": im["coords"],
                    })

        if locations:
            output_data[track_name] = locations
        elif in_missing or extract_infobox_map_ref(wt) is None and not extract_inline_maps(wt):
            output_data[track_name] = []

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print(f"\nDone! Wrote {OUTPUT_FILE}")
    print(f"  Tracks with coords: {sum(1 for v in output_data.values() if v)}")
    print(f"  Tracks without coords: {sum(1 for v in output_data.values() if not v)}")
    print(f"  Total entries: {len(output_data)}")

if __name__ == "__main__":
    main()
