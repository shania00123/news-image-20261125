# Wednesday 25 November 2026 — The Day in Full

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/shania00123/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/shania00123/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A front page summing up the world's news of **Wednesday 25 November 2026** in
one 1024x1024 image. This full-day update replaces the morning edition with
38 stories verified to 14:10 UTC: later US market closes and unreleased data
are not invented, and wrong-day items are held out in the DATE CHECK box.

## Lead stories

- **Hormuz:** Iran says two oil tankers struck naval mines and caught fire;
  Tehran warns vessels to coordinate passage.
- **Tiangong:** Shenzhou-24 docked at 03:56 UTC with Tang Hongbo, Wu Yi and
  Muhammad Zeeshan Ali, the first Pakistani in orbit.
- **Ukraine war:** drones over Samara and Syzran; Russian strikes cut power
  in five Ukrainian regions and killed one person in Bila Tserkva.
- **United States:** Q3 GDP was revised to +4.3% while October PCE inflation
  stayed at +3.8% year on year; jobless claims fell to 189,000.
- **Pacific:** Australia and Solomon Islands signed a security treaty naming
  Australia the primary security partner, with no foreign military base.

## How it is built

`render.py` draws the whole front page with PIL and DejaVu fonts: masthead,
six-number strip, region bar, two drawn hero scenes, three illustrated cards,
a UTC timeline, a markets band, a pinned map, 24 further stories and a DATE
CHECK box. `main.py` is standard-library only and copies the shipped
`poster.png` to `/output/entry.png` after checking the PNG signature, size
and dimensions. Two runs write identical bytes.

## Run it

```sh
python3 render.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=r27sfaxp&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
