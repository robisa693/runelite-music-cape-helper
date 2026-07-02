# Music Track Completer

A RuneLite plugin that shows all music tracks organized by area, with unlock hints for tracks you haven't unlocked yet. Helps you finish the music log.

## Features

- Side panel listing all music tracks
- Track name, unlock status (colored), and unlock hint shown for each track
- "Missing only" toggle to show just what you need
- Search/filter by track name
- Summary counts (total unlocked / total tracks)

## Usage

1. Install and enable the plugin
2. Open the Music tab (keyboard shortcut or click the music icon)
3. The **Music Track Completer** panel populates from the Music tab data
4. Click the music note icon in the RuneLite sidebar to open the panel
5. The "Missing only" checkbox filters to locked tracks
6. Use the search box to find specific tracks

> **Note:** The plugin observes the vanilla Music tab to determine which tracks are unlocked. Open the Music tab with the "All" filter selected at least once so every track gets evaluated. The unlocked state is cached between sessions.

## Configuration

- **Show missing only** – Only display locked tracks
- **Group by area** – Organize tracks by area
