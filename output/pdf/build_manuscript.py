"""Build the proof manuscript, with embedded fonts and vector mathematics.

Requires reportlab, matplotlib, Pillow and pypdf.  Run from any directory.
The temporary dependency path is a workspace-local fallback, not a global install.
"""
from pathlib import Path
import sys, os, re, hashlib, json, math, html, warnings

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TMP = ROOT / "tmp" / "pdfs"
TMP.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(TMP / "deps"))
os.environ["MPLCONFIGDIR"] = str(TMP / "mplconfig")
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams.update({"mathtext.fontset": "stix", "font.family": "STIXGeneral"})
from matplotlib.mathtext import MathTextParser
from matplotlib.font_manager import FontProperties
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Flowable,
    Table, TableStyle, KeepTogether,
)
import reportlab.platypus.paragraph as paragraph_engine

# ReportLab's word-count estimate omits some spaces around inline image
# fragments.  Count the actual text spaces for justification of vector math.
_original_justify = paragraph_engine._justifyDrawParaLineX
def justify_math_line(tx, offset, line, last=0):
    previous = line.wordCount
    if any(getattr(getattr(w, "cbDefn", None), "kind", None) == "img" for w in line.words):
        line.wordCount = 1 + sum(
            w.text.count(" ") for w in line.words if not hasattr(w, "cbDefn")
        )
    try:
        return _original_justify(tx, offset, line, last)
    finally:
        line.wordCount = previous
paragraph_engine._justifyDrawParaLineX = justify_math_line

FONTDIR = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
for name, filename in [
    ("TimesBody", "times.ttf"), ("TimesBody-Bold", "timesbd.ttf"),
    ("TimesBody-Italic", "timesi.ttf"), ("TimesBody-BoldItalic", "timesbi.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, str(FONTDIR / filename)))
pdfmetrics.registerFontFamily(
    "TimesBody", normal="TimesBody", bold="TimesBody-Bold",
    italic="TimesBody-Italic", boldItalic="TimesBody-BoldItalic",
)

PAGE_W, PAGE_H = A4
LEFT, RIGHT, TOP, BOTTOM = 69, 69, 63, 61
TEXT_W = PAGE_W - LEFT - RIGHT
BODY_SIZE = 11
PARSER = MathTextParser("path")
MATH_CACHE = {}
INLINE_BY_PATH = {}
FONT_CACHE = {}
MATH_DIR = TMP / "math_placeholders"
MATH_DIR.mkdir(exist_ok=True)
VECTOR_DRAWS = 0


def math_expr(text):
    # MathText is intentionally restricted to the mathematical subset used here.
    text = text.replace(r"\substack{x\neq r\\a\in T(x)}", r"x\neq r,\ a\in T(x)")
    text = text.replace(r"\hbox{for every }", r"\mathrm{for\ every}\ ")
    text = text.replace(r"\bigl(", r"\left(").replace(r"\bigr)", r"\right)")
    return text


def equation(text, size=BODY_SIZE):
    key = (text, size)
    if key not in MATH_CACHE:
        expr = "$" + math_expr(text) + "$"
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            parsed = PARSER.parse(expr, dpi=72, prop=FontProperties(size=size))
        if caught:
            raise RuntimeError(f"Math font warning in {text!r}: {caught}")
        MATH_CACHE[key] = parsed
    return MATH_CACHE[key]


def math_font(ft):
    path = str(ft.fname)
    if path not in FONT_CACHE:
        name = "Math-" + hashlib.sha256(path.encode()).hexdigest()[:12]
        pdfmetrics.registerFont(TTFont(name, path))
        FONT_CACHE[path] = name
    return FONT_CACHE[path]


def draw_math(canvas, parsed, x, y, width=None, height=None):
    """Draw the MathText vector glyph positions; y is the bottom of its box."""
    global VECTOR_DRAWS
    VECTOR_DRAWS += 1
    w, h, depth, glyphs, rects = parsed
    sx, sy = (width / w if width else 1), (height / h if height else 1)
    canvas.saveState()
    canvas.translate(x, y)
    canvas.scale(sx, sy)
    canvas.setFillColor(colors.black)
    for g in glyphs:
        if len(g) == 6:  # matplotlib >= 3.11 also returns a glyph index
            ft, size, codepoint, glyph_index, ox, oy = g
        else:
            ft, size, codepoint, ox, oy = g
        canvas.setFont(math_font(ft), size)
        canvas.drawString(float(ox), float(oy + depth), chr(codepoint))
    for rx, ry, rw, rh in rects:
        canvas.rect(float(rx), float(ry + depth), float(rw), float(rh), fill=1, stroke=0)
    canvas.restoreState()


class MathCanvas(Canvas):
    def drawImage(self, image, x, y, width=None, height=None, **kwargs):
        path = str(getattr(image, "fileName", image))
        if path in INLINE_BY_PATH:
            parsed = INLINE_BY_PATH[path]
            draw_math(self, parsed, x, y, width, height)
            return parsed.width, parsed.height
        return super().drawImage(image, x, y, width, height, **kwargs)


def inline_math(text, size):
    parsed = equation(text, size)
    digest = hashlib.sha256((text + "|" + str(size)).encode()).hexdigest()[:20]
    path = str((MATH_DIR / (digest + ".png")).resolve())
    if not Path(path).exists():
        Image.new("RGB", (1, 1), "white").save(path)
    INLINE_BY_PATH[path] = parsed
    # The placeholder is used only by ReportLab's layout engine.  MathCanvas
    # replaces it with vector glyphs; there are no raster equations in the PDF.
    return (
        f'<img src="{path}" width="{float(parsed.width):.3f}" '
        f'height="{float(parsed.height):.3f}" valign="{-float(parsed.depth):.3f}"/>'
    )


def markup(text, size=BODY_SIZE):
    text = text.replace("–", "-").replace("—", "-").replace("‑", "-")
    tokens = []
    def protect(m):
        # Include trailing punctuation in the same unbreakable vector object.
        fragment = inline_math(m.group(1) + (m.group(2) or ""), size)
        tokens.append(fragment)
        return f"@@MATH{len(tokens)-1}@@"
    text = re.sub(r"\$([^$]+)\$([.,;:?!])?", protect, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = text.replace("&", "&amp;")
    # Keep paragraph text and the font used for the end-of-proof mark compatible.
    text = text.replace("∎", '<font name="TimesBody">■</font>')
    for i, token in enumerate(tokens):
        text = text.replace(f"@@MATH{i}@@", token)
    return text


STYLES = {
    "body": ParagraphStyle(
        "body", fontName="TimesBody", fontSize=BODY_SIZE, leading=14.5,
        alignment=TA_JUSTIFY, spaceAfter=6, allowWidows=0, allowOrphans=0,
        splitLongWords=1, autoLeading="max",
    ),
    "title": ParagraphStyle(
        "title", fontName="TimesBody-Bold", fontSize=19, leading=23,
        alignment=TA_CENTER, spaceBefore=12, spaceAfter=12, keepWithNext=True,
    ),
    "subtitle": ParagraphStyle(
        "subtitle", fontName="TimesBody-Italic", fontSize=11, leading=14,
        alignment=TA_CENTER, spaceAfter=5, keepWithNext=True,
    ),
    "date": ParagraphStyle(
        "date", fontName="TimesBody", fontSize=10, leading=13,
        alignment=TA_CENTER, spaceAfter=18, keepWithNext=True,
    ),
    "abstract": ParagraphStyle(
        "abstract", fontName="TimesBody", fontSize=10, leading=13.2,
        leftIndent=18, rightIndent=18, alignment=TA_JUSTIFY,
        spaceAfter=9, autoLeading="max", allowWidows=0, allowOrphans=0,
    ),
    "keywords": ParagraphStyle(
        "keywords", fontName="TimesBody", fontSize=9, leading=12,
        leftIndent=18, rightIndent=18, spaceAfter=12,
    ),
    "section": ParagraphStyle(
        "section", fontName="TimesBody-Bold", fontSize=13, leading=16,
        spaceBefore=15, spaceAfter=8, keepWithNext=True,
    ),
    "subsection": ParagraphStyle(
        "subsection", fontName="TimesBody-Bold", fontSize=11.5, leading=15,
        spaceBefore=10, spaceAfter=7, keepWithNext=True,
    ),
    "table": ParagraphStyle(
        "table", fontName="TimesBody", fontSize=9, leading=11.5,
        alignment=TA_LEFT, autoLeading="max", splitLongWords=1,
    ),
    "caption": ParagraphStyle(
        "caption", fontName="TimesBody", fontSize=9.5, leading=12,
        alignment=TA_CENTER, spaceAfter=7,
    ),
    "reference": ParagraphStyle(
        "reference", fontName="TimesBody", fontSize=10, leading=13,
        leftIndent=17, firstLineIndent=-17, spaceAfter=8,
        allowWidows=0, allowOrphans=0,
    ),
}


class DisplayMath(Flowable):
    def __init__(self, text):
        super().__init__()
        tag = re.search(r"\\tag\{([^}]+)\}\s*$", text)
        self.tag = tag.group(1) if tag else None
        text = text[:tag.start()].strip() if tag else text.strip()
        self.parsed = equation(text.replace(r"\frac", r"\dfrac"), 11.5)
        self.spaceBefore, self.spaceAfter = 4, 8
        self.keepWithNext = False

    def wrap(self, aw, ah):
        self.width = aw
        self.scale = min(1, (aw - (42 if self.tag else 8)) / self.parsed.width)
        if self.scale < 0.86:
            raise ValueError(f"Display equation would be too small: {self.parsed.width}")
        self.height = self.parsed.height * self.scale + 4
        return self.width, self.height

    def draw(self):
        w, h = self.parsed.width*self.scale, self.parsed.height*self.scale
        draw_math(self.canv, self.parsed, (self.width-w)/2, 2, w, h)
        if self.tag:
            self.canv.setFont("TimesBody", 10.5)
            self.canv.drawRightString(self.width, (self.height-10)/2, f"({self.tag})")


class DoubledCycle(Flowable):
    def __init__(self):
        super().__init__()
        self.width, self.height = TEXT_W, 166

    def draw(self):
        c = self.canv
        cx, cy, radius = self.width/2, 81, 59
        centres, pairs = [], []
        for i in range(5):
            theta = math.pi/2 + 2*math.pi*i/5
            x, y = cx+radius*math.cos(theta), cy+radius*math.sin(theta)
            dx, dy = 6*math.cos(theta+math.pi/2), 6*math.sin(theta+math.pi/2)
            centres.append((x, y, theta))
            pairs.append([(x-dx, y-dy), (x+dx, y+dy)])
        c.setStrokeColor(colors.HexColor("#6a6a6a"))
        c.setLineWidth(0.55)
        for i in range(5):
            for x,y in pairs[i]:
                for a,b in pairs[(i+1)%5]:
                    c.line(x,y,a,b)
        for group in pairs:
            for x,y in group:
                c.setFillColor(colors.white)
                c.setStrokeColor(colors.black)
                c.setLineWidth(0.8)
                c.circle(x,y,2.4,fill=1,stroke=1)
        for i,(x,y,theta) in enumerate(centres):
            m = equation("V_"+str(i), 10)
            px,py = x+16*math.cos(theta), y+16*math.sin(theta)
            draw_math(c,m,px-m.width/2,py-m.height/2)


class ManuscriptDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, "outline_title"):
            key = flowable.outline_key
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(
                flowable.outline_title, key, level=flowable.outline_level, closed=False
            )


def decorate(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont("TimesBody-Italic", 8.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(LEFT, PAGE_H-39, "Induced matchings in prescribed edge sets")
        canvas.setStrokeColor(colors.HexColor("#c0c0c0"))
        canvas.setLineWidth(0.3)
        canvas.line(LEFT, PAGE_H-45, PAGE_W-RIGHT, PAGE_H-45)
    canvas.setFillColor(colors.black)
    canvas.setFont("TimesBody", 9)
    canvas.drawCentredString(PAGE_W/2, 35, str(doc.page))
    canvas.restoreState()


def paragraph(text, style="body"):
    return Paragraph(markup(text, STYLES[style].fontSize), STYLES[style])


def make_table(rows):
    count = len(rows[0])
    if count == 6:
        widths = [TEXT_W*.28]+[TEXT_W*.144]*5
    else:
        widths = [TEXT_W*.40,TEXT_W*.60]
    content = []
    for i,row in enumerate(rows):
        content.append([paragraph(("**"+s+"**") if i == 0 else s,"table") for s in row])
    t = Table(content, colWidths=widths, repeatRows=1, hAlign="CENTER")
    t.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),7),
        ("RIGHTPADDING",(0,0),(-1,-1),7),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LINEABOVE",(0,0),(-1,0),.7,colors.black),
        ("LINEBELOW",(0,0),(-1,0),.4,colors.black),
        ("LINEBELOW",(0,-1),(-1,-1),.7,colors.black),
    ]))
    t.spaceBefore, t.spaceAfter = 5, 10
    return t


def main():
    text = (HERE/"packing20_manuscript.md").read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n",text.strip())
    story = []
    abstract_next = False
    heading_count = 0
    for block in blocks:
        block = block.strip()
        if block.startswith("# "):
            story.append(paragraph(block[2:],"title"))
        elif block.startswith("@subtitle "):
            for line in block.splitlines():
                if line.startswith("@subtitle "):
                    story.append(paragraph(line[len("@subtitle "):],"subtitle"))
                elif line.startswith("@date "):
                    story.append(paragraph(line[len("@date "):],"date"))
        elif block.startswith("@abstract"):
            rest = block[len("@abstract"):].strip()
            if rest:
                story.append(paragraph("**Abstract.** "+rest,"abstract"))
            else:
                abstract_next = True
        elif abstract_next:
            story.append(paragraph("**Abstract.** "+block,"abstract"))
            abstract_next = False
        elif block.startswith("@keywords "):
            story.append(paragraph("**Keywords.** "+block[len("@keywords "):],"keywords"))
        elif block.startswith("## "):
            heading_count += 1
            p = paragraph(block[3:],"section")
            p.outline_title, p.outline_key, p.outline_level = block[3:], f"h{heading_count}", 0
            story.append(p)
        elif block.startswith("### "):
            heading_count += 1
            p = paragraph(block[4:],"subsection")
            p.outline_title, p.outline_key, p.outline_level = block[4:], f"h{heading_count}", 1
            story.append(p)
        elif block.startswith("$$ "):
            story.append(DisplayMath(block[3:]))
        elif block.startswith("@table "):
            rows = []
            for line in block.splitlines():
                line = re.sub(r"^@(table|row) ","",line)
                rows.append([s.strip() for s in line.split("|")])
            story.append(make_table(rows))
        elif block == "@figure doubled_cycle":
            story.append(KeepTogether([
                DoubledCycle(),
                paragraph("Figure 1. The doubled five-cycle: five independent pairs, "
                          "ten vertices and twenty edges. Each pair of consecutive clusters "
                          "induces a complete bipartite graph.","caption"),
            ]))
        elif block.startswith("@ref "):
            story.append(paragraph(block[5:],"reference"))
        else:
            p = paragraph(block)
            if re.match(r"\*\*(Theorem|Lemma|Proposition) ", block):
                p.keepWithNext = True
            story.append(p)

    out = HERE/"packing20_proof_manuscript.pdf"
    doc = ManuscriptDoc(
        str(out), pagesize=A4, leftMargin=LEFT, rightMargin=RIGHT,
        topMargin=TOP, bottomMargin=BOTTOM,
        title="Induced Matchings in Prescribed Edge Sets of Graphs of Maximum Degree Four",
        author="", subject="A complete proof manuscript for the prescribed-edge packing bound",
        creator="Proof manuscript typesetting", pageCompression=1,
    )
    frame = Frame(LEFT,BOTTOM,TEXT_W,PAGE_H-TOP-BOTTOM,
                  leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="paper",frames=frame,onPage=decorate)])
    doc.build(story, canvasmaker=MathCanvas)
    from pypdf import PdfReader
    pdf = PdfReader(str(out))
    manifest = {
        "output":out.name, "pages":len(pdf.pages),
        "sha256":hashlib.sha256(out.read_bytes()).hexdigest(),
        "source_sha256":hashlib.sha256(text.encode()).hexdigest(),
        "unique_math_expressions":len(MATH_CACHE),
        "vector_math_draws":VECTOR_DRAWS,
        "embedded_math_fonts":len(FONT_CACHE),
        "author":str(pdf.metadata.author or ""),
        "characters_per_page":[len(p.extract_text()) for p in pdf.pages],
        "raster_images":sum(len(p.images) for p in pdf.pages),
        "math_width_diagnostics": [
            {"formula":key[0],"width":float(v.width),"computed_end":float(end)}
            for key,v in MATH_CACHE.items()
            if (end := max((float(g[-2])+pdfmetrics.stringWidth(chr(g[2]),math_font(g[0]),g[1]) for g in v.glyphs),default=0)) > v.width+1
        ],
    }
    (HERE/"manuscript_build.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(json.dumps(manifest,indent=2))


if __name__ == "__main__":
    main()
