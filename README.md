# Sum up 21 November's world news in one image

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/apasi22/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/apasi22/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A code-drawn front page summing up Saturday 21 November 2026: 19 verified
stories, 11 illustrated story cards, a dotted world map with location pins,
a two-column brief list, and a DATE CHECK strip excluding stories from other
days.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13 + Pillow, no network) draws the page with simple flat
vector-style illustrations and writes `entry.png` (1024x1024, deterministic).

## Stories

Lead: drones strike Kyiv overnight; a double-tap strike kills 2 in Kryvyi
Rih; COP31 talks run past deadline with no deal. Plus the capture of
'El Chapo Isidro' in Sinaloa, a M6.7 quake in Junin, GTA VI's $3.79bn first
day, a Mercury orbit arrival, a verified Riemann proof, and eleven more —
all dated 21 November 2026.
