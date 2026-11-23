# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ahmaddzik25-png/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ahmaddzik25-png/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

**The world in one day** — a one-page newspaper front page that sums up the world news of **Monday 23 November 2026** in a single 1024×1024 image:

- **Climate talks collapse, no deal** — COP31 ends in Antalya with no agreement after the EU and others reject a final text that drops any move away from fossil fuels
- **Democrats take the House in a landslide** — a majority of at least 258 seats, the party's biggest since 1992
- **Ukraine sinks a Russian warship off Libya** — sea drones strike at Benghazi, destroying a Ka-27 helicopter and hitting the cargo ship Angara
- **Prabowo names two VP hopefuls** — Andi Amran Sulaiman and Sugiono are put forward for Indonesia's empty vice-presidency; the MPR votes on 11 December
- **AI rout deepens as Asia markets sell off** — stretched valuations sink shares in Seoul, Taipei and Hong Kong
- **Iran vows to defy US blockade at Hormuz** — the war's cost to the Gulf put at $790bn by 2030
- Plus a ticker: Russian missiles stray into Poland, Bangladesh to arrest Hasina, Nepal's PM meets Modi, Mexico captures an FBI kingpin, Brent at $92

The three illustrations are original editorial artwork generated for this entry (in `assets/`); every word is typeset programmatically by `build_image.py`, so the headlines are crisp and exactly as written. The finished image is a JPEG of 273,916 bytes under the name `entry.png` — the gate reads the format from the file's first bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies `entry.png` to the output directory — `/output` in the grader's container, `MAKEFUN_OUTPUT_DIR` anywhere else. It runs offline and writes the identical bytes every time. To rebuild the image from its sources instead: `python3 build_image.py` (needs Pillow and the DejaVu fonts).

---

<sub>Entered on [make.fun](https://make.fun/?ref=q1sv169n&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
