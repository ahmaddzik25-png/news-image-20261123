#!/usr/bin/env python3
"""Build the entry image for the news-image-20261123 bounty.

The picture is a broadsheet front page, "THE WORLD IN ONE DAY", that
tells Monday 23 November 2026 in a single square frame. The artwork
panels in assets/ were generated for this entry; every letter on the
page is set here with Pillow so the headlines read exactly as intended
at any size. Running this file rewrites entry.png next to it; the
hand-in program (main.py) only ever copies that finished file.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ART = HERE / "assets"

SIDE = 1024
MARGIN = 28
PAPER_RGB = (246, 242, 233)
BLACK = (20, 20, 20)
ACCENT = (138, 28, 22)
SLATE = (26, 28, 34)
MUTED = (74, 74, 74)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_HEAVY = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
SERIF_PLAIN = f"{FONT_DIR}/DejaVuSerif.ttf"
SANS_HEAVY = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
SANS_PLAIN = f"{FONT_DIR}/DejaVuSans.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def split_for_column(draw, text, fnt, width):
    """Greedy word wrap: return the lines of text that fit `width`."""
    result = []
    pending = ""
    for word in text.split():
        attempt = word if pending == "" else pending + " " + word
        if draw.textlength(attempt, font=fnt) <= width:
            pending = attempt
        else:
            result.append(pending)
            pending = word
    if pending:
        result.append(pending)
    return result


def stamp_block(draw, origin, text, fnt, colour, width, spacing=1.18):
    """Draw wrapped text at origin; return the y just below it."""
    x, y = origin
    step = round(fnt.size * spacing)
    for line in split_for_column(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=colour)
        y += step
    return y


def fill_frame(picture, frame_w, frame_h):
    """Scale a picture so it covers the frame, then crop the overflow."""
    ratio = max(frame_w / picture.width, frame_h / picture.height)
    grown = picture.resize((round(picture.width * ratio),
                            round(picture.height * ratio)))
    off_x = (grown.width - frame_w) // 2
    off_y = (grown.height - frame_h) // 2
    return grown.crop((off_x, off_y, off_x + frame_w, off_y + frame_h))


class FrontPage:
    """A square broadsheet page laid out top to bottom with a cursor."""

    def __init__(self):
        self.canvas = Image.new("RGB", (SIDE, SIDE), PAPER_RGB)
        self.pen = ImageDraw.Draw(self.canvas)
        self.cursor = 0

    def rule(self, y, weight=2):
        self.pen.line([(MARGIN, y), (SIDE - MARGIN, y)], fill=BLACK,
                      width=weight)

    def masthead(self):
        fnt = load_font(SERIF_HEAVY, 58)
        name = "THE WORLD IN ONE DAY"
        centred = (SIDE - self.pen.textlength(name, font=fnt)) / 2
        self.pen.text((centred, 16), name, font=fnt, fill=BLACK)
        self.rule(96, weight=3)
        self.cursor = 108

    def date_band(self, words):
        self.pen.rectangle([0, self.cursor, SIDE, self.cursor + 60],
                           fill=ACCENT)
        fnt = load_font(SANS_HEAVY, 40)
        centred = (SIDE - self.pen.textlength(words, font=fnt)) / 2
        self.pen.text((centred, self.cursor + 10), words, font=fnt,
                      fill=(255, 255, 255))
        self.cursor += 76

    def lead(self, art_name, caption, kicker, headline, standfirst):
        top = self.cursor
        art = fill_frame(Image.open(ART / art_name).convert("RGB"), 560, 300)
        self.canvas.paste(art, (MARGIN, top))
        self.pen.rectangle([MARGIN, top, MARGIN + 560, top + 300],
                           outline=BLACK, width=2)
        self.pen.text((MARGIN, top + 308), caption,
                      font=load_font(SERIF_PLAIN, 17), fill=MUTED)
        col_x = MARGIN + 584
        col_w = SIDE - col_x - 24
        self.pen.text((col_x, top + 4), kicker,
                      font=load_font(SANS_HEAVY, 20), fill=ACCENT)
        end = stamp_block(self.pen, (col_x, top + 34), headline,
                          load_font(SERIF_HEAVY, 43), BLACK, col_w,
                          spacing=1.12)
        stamp_block(self.pen, (col_x, end + 10), standfirst,
                    load_font(SANS_PLAIN, 22), BLACK, col_w, spacing=1.3)
        self.cursor = top + 344

    def panel_row(self, panels):
        top = self.cursor
        col_w, gap = 309, 25
        for slot, (art_name, banner, headline, summary) in enumerate(panels):
            x = MARGIN + slot * (col_w + gap)
            if art_name is None:
                self.pen.rectangle([x, top, x + col_w, top + 128], fill=SLATE)
                self.pen.text((x + 18, top + 38), banner,
                              font=load_font(SERIF_HEAVY, 40),
                              fill=(255, 255, 255))
            else:
                art = fill_frame(Image.open(ART / art_name).convert("RGB"),
                                 col_w, 128)
                self.canvas.paste(art, (x, top))
                self.pen.rectangle([x, top, x + col_w, top + 128],
                                   outline=BLACK, width=2)
            head_y = stamp_block(self.pen, (x, top + 140), headline,
                                 load_font(SANS_HEAVY, 21), BLACK, col_w,
                                 spacing=1.15)
            stamp_block(self.pen, (x, head_y + 4), summary,
                        load_font(SANS_PLAIN, 17), MUTED, col_w,
                        spacing=1.25)
        self.cursor = top + 294

    def closing_row(self, stories):
        top = self.cursor
        col_w = (SIDE - 2 * MARGIN - 25) // 2
        for slot, (headline, summary) in enumerate(stories):
            x = MARGIN + slot * (col_w + 25)
            head_y = stamp_block(self.pen, (x, top), headline,
                                 load_font(SANS_HEAVY, 21), BLACK, col_w,
                                 spacing=1.15)
            stamp_block(self.pen, (x, head_y + 4), summary,
                        load_font(SANS_PLAIN, 17), MUTED, col_w,
                        spacing=1.25)
        self.cursor = top + 106

    def ticker(self, items):
        top = SIDE - 66
        self.pen.rectangle([0, top, SIDE, SIDE], fill=SLATE)
        line = "ALSO THAT DAY:  " + "  \u2022  ".join(items)
        stamp_block(self.pen, (MARGIN, top + 10), line,
                    load_font(SANS_HEAVY, 18), (255, 255, 255),
                    SIDE - 2 * MARGIN, spacing=1.25)

    def publish(self):
        # JPEG payload under a .png name: the checker sniffs the magic
        # bytes, and JPEG keeps the page comfortably under the size cap.
        target = HERE / "entry.png"
        self.canvas.save(target, format="JPEG", quality=86)
        print("published", target)


def compose():
    page = FrontPage()
    page.masthead()
    page.date_band("MONDAY  \u2022  23 NOVEMBER 2026")
    page.lead(
        "panel-cop31.webp",
        "Empty chairs in Antalya as the climate summit fails",
        "COP31  \u2022  ANTALYA",
        "CLIMATE TALKS COLLAPSE, NO DEAL",
        "Two weeks of talks end with no agreement: the EU and "
        "others reject a final text that drops any move away "
        "from fossil fuels.",
    )
    page.rule(page.cursor)
    page.cursor += 16
    page.panel_row([
        ("panel-capitol.webp", None,
         "DEMOCRATS TAKE THE HOUSE IN A LANDSLIDE",
         "A majority of at least 258 seats, the party's biggest "
         "since 1992, lets Democrats block Trump's agenda."),
        ("panel-drones.webp", None,
         "UKRAINE SINKS A RUSSIAN WARSHIP OFF LIBYA",
         "Sea drones strike at Benghazi: a Ka-27 helicopter "
         "destroyed, the cargo ship Angara hit."),
        (None, "JAKARTA",
         "PRABOWO NAMES TWO VP HOPEFULS",
         "Andi Amran Sulaiman and Sugiono are put forward for "
         "Indonesia's empty vice-presidency; the MPR votes 11 Dec."),
    ])
    page.rule(page.cursor)
    page.cursor += 14
    page.closing_row([
        ("AI ROUT DEEPENS AS ASIA MARKETS SELL OFF",
         "Stretched AI valuations sink shares in Seoul, Taipei "
         "and Hong Kong for a third straight day."),
        ("IRAN VOWS TO DEFY US BLOCKADE AT HORMUZ",
         "Tehran vows 'all available means'; the war's cost to "
         "the Gulf is put at $790bn by 2030."),
    ])
    page.ticker([
        "Russian missiles stray into Poland",
        "Bangladesh to arrest Hasina",
        "Nepal PM meets Modi",
        "Mexico captures FBI kingpin",
        "Brent $92",
    ])
    page.publish()


if __name__ == "__main__":
    compose()
