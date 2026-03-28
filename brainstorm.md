# Brainstorm: Using Stage Lat/Long Data

Now that each stage has GPS coordinates, here are ideas for what the app could do with them.

---

## Google Maps Links

Add a "Directions" link on each stage label or act detail that opens Google Maps
with the stage as the destination:

```
https://www.google.com/maps/dir/?api=1&destination=29.95278,-90.06307
```

Low effort, high value — especially for first-time festival-goers who don't
know the Quarter layout.

---

## Distance Between Consecutive Picks

When the user has a sequence of picked acts, show the walking distance (or
straight-line distance) between each venue transition:

> **2:30 PM** Rebirth Brass Band @ Jack Daniel's Stage
> *~350m walk, ~4 min*
> **3:30 PM** Tuba Skinny @ NewOrleans.com Stage

Use the Haversine formula for straight-line distance. The French Quarter
street grid adds roughly 20-30% to straight-line for actual walking, so
multiply by ~1.25 as a rough correction factor.

---

## Proximity Warnings on Pick Selection

When the user picks a new act, if their previous or next pick is far away and
the gap is short, show a warning:

> ⚠ Entergy Songwriter Stage is ~450m from Louisiana Fish Fry Stage.
> You have 10 minutes between sets — that's a tight walk.

Define thresholds: maybe >300m with <15 min gap = yellow warning,
>400m with <10 min gap = red warning. The thresholds could be tunable in
settings.

---

## Interactive Map View

Add a map tab (Leaflet or MapLibre GL with OpenStreetMap tiles) showing:
- Stage pins with the stage name
- Color-coded by "currently playing" vs "upcoming" vs "idle"
- Click a pin to see the current/next act
- Overlay the user's picks as a connected path with timestamps

This would be the most impressive feature but also the most work. Could use
a free tile provider (Stadia Maps, Carto, or self-hosted).

---

## "Nearby Stages" Suggestions

In the act detail modal, show a "Nearby stages" section listing stages
within 200m, along with what's playing there at the same time. This helps
users discover acts they might not have noticed, especially on stages they
haven't explored yet.

---

## Heat Map / Density View

Show a simple heat map overlay indicating which areas of the Quarter have
the most stages clustered together. The French Market / Dutch Alley / Entergy /
Loyola / PanAm cluster is very dense — users heading there can easily hop
between 5-6 stages. The Fish Fry / Abita area is more isolated.

This could just be a static info graphic rather than a dynamic feature.

---

## Walking Route Planner

Given the user's full day of picks, compute an optimized walking route
that minimizes total distance. This is basically the Traveling Salesman Problem
but with time constraints (each act has a fixed time window). The constraint
simplifies it — you can't reorder the acts — but the optimizer could suggest:

- "You could swap your 2:00 pick from Stage A to Stage B (same genre, similar
  act) and save 600m of walking"
- "There's a 45-minute gap here — consider grabbing food near [nearby stage]"

---

## Rough Priority

| Idea | Effort | Value |
|------|--------|-------|
| Google Maps links | Low | High |
| Distance between picks | Low | High |
| Proximity warnings | Medium | High |
| Nearby stages | Medium | Medium |
| Interactive map | High | High |
| Heat map / density | Low | Low |
| Walking route planner | High | Medium |
