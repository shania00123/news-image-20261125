# Wednesday 25 November 2026 — The World in One Day (Morning Edition)

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/shania00123/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/shania00123/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A front page summing up the world's news of **Wednesday 25 November 2026** in one
1024×1024 image: 38 stories across 3 regions, every one verified against
reporting from that day. This is the morning edition — built from news
verifiable before 09:30 WIB (02:30 UTC); an evening edition with the full
day's news may supersede it.

## What happened that day

- **Jiuquan:** Shenzhou-24 lifts off at 00:18 GMT carrying commander Tang
  Hongbo, flight engineer Wu Yi, and Zeeshan Ali — the first Pakistani in
  orbit, bound for 5–10 days aboard the Tiangong station.
- **Honiara:** Australia and Solomon Islands sign a security pact making
  Canberra the island nation's defence partner of choice, a shift from its
  2022 security deal with China.
- **San Francisco:** the Bay braces for near-record king tides — Wednesday's
  high tide may reach 8.5 ft, near the 1983 record of 8.82 ft — as an
  atmospheric river arrives for Thanksgiving week.
- **Seoul / Tokyo:** the Nvidia rally unwinds — Kospi sinks 4.6% and trips
  its circuit breaker, Nikkei slides 2.4% in early trade.
- **Washington:** the US weighs new duties on 16 trading partners after a
  Section 301 probe; Shein agrees to pay $100m to settle FTC claims; the
  CDC director draws doubts from staff and lawmakers; a soldier admits
  selling military secrets to China; and Trump pardons the Thanksgiving
  turkeys.
- **Brussels:** the European Parliament debates Costa's €1.58tn budget
  compromise ahead of the 26–27 November summit.

## How it is built

`render.py` draws the whole front page with PIL (DejaVu fonts, no network):
masthead, six-number strip, UTC timeline, three hero scenes drawn from
scratch, 19 grid cards, a pinned world map, 16 more stories, a DATE CHECK
box holding Tuesday's stories out of the count, and a markets band.
`main.py` (standard library only) copies the shipped `poster.png` to
`/output/entry.png`, verifying the PNG magic, 1024×1024 size, 1 MiB cap and
every chunk CRC first. Two runs write identical bytes.

## Run it

```sh
python3 render.py            # redraw poster.png (needs Pillow + DejaVu)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=r27sfaxp&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
