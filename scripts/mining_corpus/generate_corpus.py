"""Render the synthetic Ridgeback Concentrator document pack to PDF (HTML/SVG -> headless Chrome).

Usage:  .venv/bin/python scripts/mining_corpus/generate_corpus.py [--out corpora/copper-concentrator/raw]

All values come from plant_model.py. Seeded conflicts are applied only through value_in().
"""

from __future__ import annotations

import argparse
import html
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plant_model as pm

E = html.escape
MB = pm.MB
SITE = pm.SITE
CHROME = shutil.which("google-chrome") or shutil.which("chromium")

BASE_CSS = """
*{box-sizing:border-box} body{margin:0;font:10.5px/1.35 Arial,Helvetica,sans-serif;color:#111}
.page{page-break-after:always;position:relative;padding:0}
.page:last-child{page-break-after:auto}
.banner{border:1.5px solid #b00;color:#b00;font-weight:bold;text-align:center;padding:3px;margin-bottom:6px;font-size:9px;letter-spacing:.3px}
table{border-collapse:collapse;width:100%} td,th{border:1px solid #333;padding:3px 5px;vertical-align:top}
th{background:#e9e9e9;text-align:left} h1{font-size:15px;margin:4px 0 6px} h2{font-size:12.5px;margin:12px 0 4px;border-bottom:1px solid #333}
h3{font-size:11px;margin:9px 0 3px} p{margin:3px 0 6px} .r{text-align:right} .c{text-align:center} .sm{font-size:9px;color:#333}
.hdr td{font-size:10px} .mono{font-family:'Courier New',monospace} ul{margin:2px 0 6px 16px;padding:0} li{margin:1px 0}
"""


def fname(s: str) -> str:
    """File-system safe title: drop parentheticals, no slashes."""
    import re
    return re.sub(r"\s+", " ", re.sub(r"\([^)]*\)", "", s).replace("/", "-")).strip()


def banner() -> str:
    return f"<div class='banner'>{E(SITE['disclaimer'])}</div>"


def chrome_pdf(html_text: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "doc.html"
        src.write_text(html_text, encoding="utf-8")
        cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
               f"--print-to-pdf={out}", f"file://{src}"]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)


def doc(title: str, body: str, size: str = "A4") -> str:
    return (f"<!doctype html><html><head><meta charset='utf-8'><title>{E(title)}</title>"
            f"<style>@page{{size:{size};margin:12mm}}{BASE_CSS}</style></head><body>{body}</body></html>")


# ---------------------------------------------------------------------------
# Data sheets
# ---------------------------------------------------------------------------
def ds_header(doc_no: str, title: str, rev: str, sheet: int, of: int, tag: str) -> str:
    return (f"{banner()}<table class='hdr'><tr><td rowspan=2 style='width:28%'><b>{E(SITE['owner'])}</b><br>{E(SITE['site'])}<br>Project {SITE['project_no']}</td>"
            f"<td rowspan=2 style='width:42%'><h1>{E(title)}</h1>Equipment tag: <b>{E(tag)}</b></td>"
            f"<td>Doc No.<br><b class='mono'>{E(doc_no)}</b></td><td>Rev<br><b>{E(rev)}</b></td></tr>"
            f"<tr><td colspan=2>Sheet <b>{sheet}</b> of <b>{of}</b></td></tr></table>")


def ds_table(rows: list[tuple[str, str]], caption: str) -> str:
    tr = "".join(f"<tr><td style='width:45%'>{E(k)}</td><td><b>{E(v)}</b></td></tr>" for k, v in rows)
    return f"<h2>{E(caption)}</h2><table><tr><th>Parameter</th><th>Value</th></tr>{tr}</table>"


def rev_block(revs: list[tuple[str, str, str]]) -> str:
    tr = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{E(c)}</td></tr>" for a, b, c in revs)
    return f"<h2>Revision history</h2><table><tr><th>Rev</th><th>Date</th><th>Description</th></tr>{tr}</table>"


DS_ID = {  # plant_model doc id -> file doc number
    "CR-2101": "RB-4410-PS-CR2101", "ML-3101": "RB-4410-PS-ML3101", "CR-3102": "RB-4410-PS-CR3102",
    "ML-3201": "RB-4410-PS-ML3201", "PP-3201A": "RB-4410-PS-PP3201", "CY-3201": "RB-4410-PS-CY3201",
    "FC-4101": "RB-4410-PS-FC4101", "ML-4201": "RB-4410-PS-ML4201", "FC-4301": "RB-4410-PS-FC4301",
    "TK-4501": "RB-4410-PS-TK4501", "TK-4511": "RB-4410-PS-TK4511", "TK-4521": "RB-4410-PS-TK4521",
    "TH-5101": "RB-4410-PS-TH5101", "PP-5101A": "RB-4410-PS-PP5101", "FP-5101": "RB-4410-PS-FP5101",
    "TH-6101": "RB-4410-PS-TH6101", "PP-6101A": "RB-4410-PS-PP6101",
}
MODEL_DOC = {  # tag -> plant_model conflict doc id for its data sheet
    "ML-3101": "DS-ML-3101", "PP-3201A": "DS-PP-3201", "TK-4511": "DS-TK-4511", "TH-5101": "DS-TH-5101",
    "CR-2101": "DS-CR-2101", "PP-6101A": "DS-PP-6101", "ML-3201": "DS-ML-3201 (Sheet 1)",
}


def ds_rows(tag: str, doc_id: str) -> list[tuple[str, str]]:
    return [(p, pm.value_in(doc_id, tag, p)) for p in pm.EQ[tag].params]


def build_datasheets(out: Path) -> list[Path]:
    made = []
    for e in pm.EQUIPMENT:
        doc_no = DS_ID[e.tag]
        did = MODEL_DOC.get(e.tag, f"DS-{e.tag}")
        area = pm.AREAS[e.area]
        common = [("Service", e.name), ("Plant area", f"Area {e.area} - {area}"), ("Equipment class", e.cls),
                  ("Function", e.function), ("Connected equipment", ", ".join(e.connections))]
        pages = []
        if e.tag == "PP-5101A":  # revision decoy: two files
            for rev, flow, date, desc in (("A", "180 m3/h", "2025-11-04", "Issued for design"),
                                          ("B", "210 m3/h", "2026-03-18", "Rated flow increased after filter trade-off; supersedes Rev A")):
                rows = [(k, flow if k == "Rated flow" else v) for k, v in ds_rows(e.tag, did)]
                body = ("<div class='page'>" + ds_header(doc_no, f"{e.name} - Process Data Sheet", rev, 1, 1, "PP-5101A/B")
                        + ds_table(common, "General") + ds_table(rows, "Process design data")
                        + rev_block([("A", "2025-11-04", "Issued for design")] + ([("B", date, desc)] if rev == "B" else [])) + "</div>")
                p = out / "data_sheets" / f"{doc_no}_{fname(e.name.upper())} PROCESS DATA SHEET_Rev{rev}.pdf"
                chrome_pdf(doc(doc_no, body), p)
                made.append(p)
            continue
        rows = ds_rows(e.tag, did)
        if e.tag in ("ML-3101", "ML-3201"):
            n = 3
            pages.append(ds_header(doc_no, f"{e.name} - Process Data Sheet", "B", 1, n, e.tag)
                         + ds_table(common, "General (cover sheet)") + ds_table(rows, "Process design data")
                         + rev_block([("A", "2025-09-12", "Issued for review"), ("B", "2026-02-20", "Issued for design")]))
            motor_kw = pm.value_in("DS-ML-3201 (Sheet 3)", "ML-3201", "Installed power") if e.tag == "ML-3201" else pm.value_in(did, e.tag, "Installed power")
            pages.append(ds_header(doc_no, f"{e.name} - Mechanical Data", "B", 2, n, e.tag) + ds_table([
                ("Shell material", "ASTM A516 Gr 70"), ("Shell thickness", "90 mm" if e.tag == "ML-3101" else "80 mm"),
                ("Head/trunnion", "Cast steel, one-piece"), ("Feed chute", "Rubber-lined, replaceable wear plates"),
                ("Discharge", "Trommel to SC-3101" if e.tag == "ML-3101" else "Overflow to PP-3201 hopper"),
                ("Reline method", "Mill relining machine, 2.5 t capacity"), ("Inching drive", "GMD inching mode, 0.1 rpm"),
                ("Charge weight at max filling", "2,450 t" if e.tag == "ML-3101" else "1,980 t")], "Mechanical design"))
            pages.append(ds_header(doc_no, f"{e.name} - Motor & Lubrication Data", "B", 3, n, e.tag) + ds_table([
                ("Motor type", "Ring motor (GMD)"), ("Rated motor power", motor_kw), ("Voltage", "33 kV feed / cycloconverter"),
                ("Lube system", "Combined hydrostatic lift / hydrodynamic lube unit"),
                ("HP lift pump discharge pressure (normal)", "120 bar(g)" if e.tag == "ML-3101" else "110 bar(g)"),
                ("Lube system design pressure", "170 bar(g)"), ("Bearing temperature instruments", "TT-3101 / TT-3102 (RTD, duplex)" if e.tag == "ML-3101" else "TT-3201 / TT-3202"),
                ("Oil grade", "ISO VG 460")], "Drive, motor and lubrication"))
        else:
            pages.append(ds_header(doc_no, f"{e.name} - Process Data Sheet", "B", 1, 1, e.tag)
                         + ds_table(common, "General") + ds_table(rows, "Process design data")
                         + rev_block([("A", "2025-09-12", "Issued for review"), ("B", "2026-02-20", "Issued for design")]))
        body = "".join(f"<div class='page'>{p}</div>" for p in pages)
        p = out / "data_sheets" / f"{doc_no}_{fname(e.name.upper())} PROCESS DATA SHEET_B.pdf"
        chrome_pdf(doc(doc_no, body), p)
        made.append(p)

    # Instrument data sheets
    temp = [i for i in pm.INSTRUMENTS if i[0].startswith("TT")]
    pres = [i for i in pm.INSTRUMENTS if i[0].startswith(("PT", "PSV"))]
    anal = [i for i in pm.INSTRUMENTS if i[0].startswith(("AIC", "DT", "LT"))]
    for no, title, group in (("RB-4410-PS-0034", "Temperature Instrument Process Data Sheet", temp),
                             ("RB-4410-PS-0032", "Pressure Instrument & Relief Valve Process Data Sheet", pres),
                             ("RB-4410-PS-0033", "Analyser, Density & Level Instrument Data Sheet", anal)):
        tr = "".join(f"<tr><td class='mono'><b>{t}</b></td><td>{E(s)}</td><td>{E(r)}</td><td><b>{E(a)}</b></td><td>{E(f)}</td></tr>" for t, s, r, a, f in group)
        body = ("<div class='page'>" + ds_header(no, title, "B", 1, 1, "Various")
                + f"<h2>Instrument schedule</h2><table><tr><th>Tag</th><th>Service</th><th>Range</th><th>Alarm / trip / set point</th><th>SIS function</th></tr>{tr}</table>"
                + "<p class='sm'>Set points on this data sheet are the design basis. The SIS cause &amp; effect matrix (RB-4410-STD-CE-001) must match.</p></div>")
        p = out / "data_sheets" / f"{no}_{fname(title.upper())}_B.pdf"
        chrome_pdf(doc(no, body), p)
        made.append(p)
    return made


# ---------------------------------------------------------------------------
# P&IDs (vector SVG, A3 landscape)
# ---------------------------------------------------------------------------
W, H = 1560, 1040
LINE = "stroke='#000' stroke-width='1.6' fill='none'"


def sym(kind: str, x: int, y: int, tag: str) -> str:
    t = f"<text x='{x}' y='{y+78}' text-anchor='middle' font-size='13' font-weight='bold'>{tag}</text>"
    if kind == "mill":
        return (f"<rect x='{x-90}' y='{y-40}' width='180' height='80' rx='14' {LINE}/><rect x='{x-120}' y='{y-14}' width='30' height='28' {LINE}/>"
                f"<rect x='{x+90}' y='{y-14}' width='30' height='28' {LINE}/><line x1='{x-60}' y1='{y-40}' x2='{x-60}' y2='{y+40}' stroke='#000'/>"
                f"<line x1='{x+60}' y1='{y-40}' x2='{x+60}' y2='{y+40}' stroke='#000'/>{t.replace(str(y+78), str(y+62))}")
    if kind == "crusher":
        return f"<polygon points='{x-50},{y-40} {x+50},{y-40} {x+22},{y+40} {x-22},{y+40}' {LINE}/><polygon points='{x-14},{y-20} {x+14},{y-20} {x+6},{y+30} {x-6},{y+30}' {LINE}/>{t.replace(str(y+78), str(y+58))}"
    if kind == "pump":
        return (f"<circle cx='{x}' cy='{y}' r='22' {LINE}/><line x1='{x}' y1='{y-22}' x2='{x+34}' y2='{y-22}' stroke='#000' stroke-width='1.6'/>"
                f"<polygon points='{x-16},{y+30} {x+16},{y+30} {x},{y+14}' {LINE}/>{t.replace(str(y+78), str(y+50))}")
    if kind == "tank":
        return (f"<rect x='{x-45}' y='{y-50}' width='90' height='100' {LINE}/><line x1='{x}' y1='{y-66}' x2='{x}' y2='{y+20}' stroke='#000' stroke-width='1.6'/>"
                f"<line x1='{x-18}' y1='{y+20}' x2='{x+18}' y2='{y+20}' stroke='#000' stroke-width='3'/>{t.replace(str(y+78), str(y+70))}")
    if kind == "thickener":
        return (f"<polyline points='{x-110},{y-30} {x-110},{y+10} {x},{y+45} {x+110},{y+10} {x+110},{y-30}' {LINE}/><line x1='{x}' y1='{y-50}' x2='{x}' y2='{y+40}' stroke='#000' stroke-width='1.6'/>"
                f"<line x1='{x-90}' y1='{y+14}' x2='{x+90}' y2='{y+14}' stroke='#000' stroke-dasharray='6 4'/>{t.replace(str(y+78), str(y+68))}")
    if kind == "cyclone":
        return (f"<rect x='{x-22}' y='{y-50}' width='44' height='34' {LINE}/><polygon points='{x-22},{y-16} {x+22},{y-16} {x+5},{y+40} {x-5},{y+40}' {LINE}/>"
                f"<line x1='{x}' y1='{y-66}' x2='{x}' y2='{y-50}' stroke='#000' stroke-width='1.6'/>{t.replace(str(y+78), str(y+60))}")
    if kind == "cell":
        return (f"<rect x='{x-40}' y='{y-40}' width='80' height='80' {LINE}/><line x1='{x}' y1='{y-54}' x2='{x}' y2='{y+22}' stroke='#000' stroke-width='1.6'/>"
                f"<polygon points='{x-14},{y+22} {x+14},{y+22} {x},{y+32}' fill='#000'/>{t.replace(str(y+78), str(y+60))}")
    if kind == "column":
        return f"<rect x='{x-28}' y='{y-80}' width='56' height='160' rx='8' {LINE}/>{t.replace(str(y+78), str(y+100))}"
    if kind == "filter":
        bars = "".join(f"<line x1='{x-50+i*12}' y1='{y-30}' x2='{x-50+i*12}' y2='{y+30}' stroke='#000'/>" for i in range(9))
        return f"<rect x='{x-56}' y='{y-30}' width='112' height='60' {LINE}/>{bars}{t.replace(str(y+78), str(y+50))}"
    if kind == "fan":
        return (f"<circle cx='{x}' cy='{y}' r='20' {LINE}/><line x1='{x-14}' y1='{y-14}' x2='{x+14}' y2='{y+14}' stroke='#000'/>"
                f"<line x1='{x-14}' y1='{y+14}' x2='{x+14}' y2='{y-14}' stroke='#000'/>{t.replace(str(y+78), str(y+42))}")
    if kind == "screen":
        return f"<polygon points='{x-50},{y-10} {x+50},{y+10} {x+50},{y+22} {x-50},{y+2}' {LINE}/>{t.replace(str(y+78), str(y+44))}"
    if kind == "conveyor":
        return (f"<line x1='{x-80}' y1='{y}' x2='{x+80}' y2='{y-30}' stroke='#000' stroke-width='2'/><circle cx='{x-80}' cy='{y}' r='7' {LINE}/>"
                f"<circle cx='{x+80}' cy='{y-30}' r='7' {LINE}/>{t.replace(str(y+78), str(y+26))}")
    return ""


def bubble(x: int, y: int, tag: str, to: tuple[int, int] | None = None, shared: bool = True) -> str:
    letters, num = tag.split("-")
    s = ""
    if to:
        s += f"<line x1='{x}' y1='{y+18}' x2='{to[0]}' y2='{to[1]}' stroke='#000' stroke-dasharray='5 3'/>"
    s += f"<circle cx='{x}' cy='{y}' r='18' fill='#fff' stroke='#000' stroke-width='1.4'/>"
    if shared:
        s += f"<line x1='{x-18}' y1='{y}' x2='{x+18}' y2='{y}' stroke='#000'/>"
    s += (f"<text x='{x}' y='{y-3}' text-anchor='middle' font-size='10' font-weight='bold'>{letters}</text>"
          f"<text x='{x}' y='{y+12}' text-anchor='middle' font-size='10'>{num}</text>")
    return s


def psv(x: int, y: int, tag: str, setp: str) -> str:
    return (f"<polygon points='{x-12},{y+12} {x+12},{y+12} {x},{y}' {LINE}/><polygon points='{x-12},{y-12} {x+12},{y-12} {x},{y}' {LINE}/>"
            f"<text x='{x+18}' y='{y-2}' font-size='11' font-weight='bold'>{tag}</text><text x='{x+18}' y='{y+12}' font-size='10'>SET {E(setp)}</text>")


def pipe(points: list[tuple[int, int]], label: str = "") -> str:
    pts = " ".join(f"{a},{b}" for a, b in points)
    (x1, y1), (x2, y2) = points[-2], points[-1]
    ax = "" if (x1, y1) == (x2, y2) else f"<polygon points='{x2},{y2} {x2-(10 if x2>x1 else -10 if x2<x1 else 5)},{y2-(5 if y1==y2 else (10 if y2>y1 else -10))} {x2-(10 if x2>x1 else -10 if x2<x1 else -5)},{y2+(5 if y1==y2 else -(10 if y2>y1 else -10))}' fill='#000'/>"
    lab = f"<text x='{(points[0][0]+points[1][0])//2}' y='{(points[0][1]+points[1][1])//2-6}' font-size='10' text-anchor='middle'>{E(label)}</text>" if label else ""
    return f"<polyline points='{pts}' stroke='#000' stroke-width='2' fill='none'/>{ax}{lab}"


def eq_box(x: int, y: int, lines: list[str], w: int = 250) -> str:
    h = 16 * len(lines) + 10
    txt = "".join(f"<text x='{x+8}' y='{y+18+i*16}' font-size='{12 if i==0 else 11}' font-weight='{'bold' if i==0 else 'normal'}'>{E(t)}</text>" for i, t in enumerate(lines))
    return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='#fff' stroke='#000'/>{txt}"


def title_block(dwg: str, title: str, rev: str = "B") -> str:
    x, y = W - 560, H - 150
    return (f"<rect x='{x}' y='{y}' width='550' height='140' fill='#fff' stroke='#000' stroke-width='2'/>"
            f"<line x1='{x}' y1='{y+40}' x2='{x+550}' y2='{y+40}' stroke='#000'/><line x1='{x}' y1='{y+100}' x2='{x+550}' y2='{y+100}' stroke='#000'/>"
            f"<text x='{x+10}' y='{y+17}' font-size='12' font-weight='bold'>{E(SITE['owner'])}</text>"
            f"<text x='{x+10}' y='{y+33}' font-size='11'>{E(SITE['site'])} - Project {SITE['project_no']}</text>"
            f"<text x='{x+10}' y='{y+62}' font-size='13' font-weight='bold'>PIPING &amp; INSTRUMENTATION DIAGRAM</text>"
            f"<text x='{x+10}' y='{y+84}' font-size='13'>{E(title)}</text>"
            f"<text x='{x+10}' y='{y+124}' font-size='13' font-weight='bold'>DWG No. {dwg}</text>"
            f"<text x='{x+400}' y='{y+124}' font-size='13' font-weight='bold'>REV {rev}</text>"
            f"<text x='{x+300}' y='{y+17}' font-size='10' fill='#b00'>SYNTHETIC DEMO DRAWING</text>")


def notes(lines: list[str]) -> str:
    x, y = 30, H - 150
    t = "".join(f"<text x='{x+10}' y='{y+36+i*15}' font-size='11'>{i+1}. {E(s)}</text>" for i, s in enumerate(lines))
    return f"<rect x='{x}' y='{y}' width='900' height='140' fill='#fff' stroke='#000'/><text x='{x+10}' y='{y+18}' font-size='12' font-weight='bold'>NOTES</text>{t}"


def pid_page(dwg: str, title: str, content: str, note_lines: list[str]) -> str:
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='100%' font-family='Arial'>"
           f"<rect x='8' y='8' width='{W-16}' height='{H-16}' fill='none' stroke='#000' stroke-width='3'/>"
           f"{content}{notes(note_lines)}{title_block(dwg, title)}</svg>")
    return doc(dwg, f"<div class='page'>{svg}</div>", "A3 landscape")


def v(doc_id: str, tag: str, p: str) -> str:
    return pm.value_in(doc_id, tag, p)


def build_pids(out: Path) -> list[Path]:
    made = []
    d = out / "pid"
    P = {}
    # 21-001 Primary crushing
    P[("RB-4410-PID-21-001", "PRIMARY CRUSHING")] = (
        sym("crusher", 360, 360, "CR-2101") + sym("conveyor", 760, 470, "CV-2101") + sym("tank", 1150, 380, "ST-2101")
        + pipe([(360, 400), (360, 470), (680, 470)], "ROM ore 5,500 t/h max") + pipe([(840, 440), (1105, 400)], "Crushed ore S-101")
        + eq_box(200, 110, ["CR-2101 PRIMARY GYRATORY CRUSHER", f"Type: {v('PID-21-001','CR-2101','Type')}", f"Power: {v('PID-21-001','CR-2101','Installed power')}", f"CSS: {v('PID-21-001','CR-2101','Closed side setting')}"])
        + eq_box(1010, 110, ["ST-2101 COARSE ORE STOCKPILE", "Live capacity: 60,000 t", "Reclaim: FE-3101A/B/C"])
        + bubble(470, 270, "WT-2101", (400, 330)) + bubble(560, 560, "WIT-2102", (700, 470)),
        ["Crusher lubrication and hydroset systems on vendor drawing VD-2101.", "Dust suppression sprays not shown.", "Weightometer WIT-2102 is the plant feed reconciliation meter."])
    # 31-001 SAG mill
    P[("RB-4410-PID-31-001", "SAG MILL ML-3101")] = (
        sym("conveyor", 250, 430, "CV-3101") + sym("mill", 640, 420, "ML-3101") + sym("screen", 930, 470, "SC-3101")
        + sym("crusher", 1180, 330, "CR-3102") + sym("pump", 1000, 640, "PP-3201A")
        + pipe([(330, 400), (520, 410)], "SAG feed S-301") + pipe([(760, 430), (880, 460)]) + pipe([(980, 470), (1150, 380)], "Pebbles S-305")
        + pipe([(930, 490), (930, 620), (978, 640)], "Screen U/S to cyclone feed hopper")
        + pipe([(1180, 290), (1180, 200), (250, 200), (250, 395)], "Crushed pebbles return")
        + eq_box(470, 90, ["ML-3101 SAG MILL", f"Size: {v('PID-31-001','ML-3101','Diameter x EGL')}", f"Motor: {v('PID-31-001','ML-3101','Installed power')} GMD", f"Throughput: {v('PID-31-001','ML-3101','Design throughput')}"], 290)
        + bubble(560, 560, "TT-3101", (590, 460)) + bubble(720, 560, "TT-3102", (700, 460)) + bubble(640, 300, "JI-3101", (640, 380))
        + bubble(400, 540, "WIC-3101", (330, 430)) + bubble(860, 330, "FIC-3103", (800, 425)),
        ["Hydrostatic lift and lube system on RB-4410-PID-31-002.", "TT-3101/3102 trip via SIF-3101 - refer RB-4410-STD-CE-001.",
         "Mill feed water ratio control FIC-3103 targets 75 % solids in mill.", "Pebble crusher bypass chute not shown."])
    # 31-002 Lube system
    P[("RB-4410-PID-31-002", "SAG MILL HYDROSTATIC LIFT & LUBE SYSTEM")] = (
        sym("tank", 300, 450, "TK-3105") + sym("pump", 560, 520, "PP-3105A") + sym("pump", 560, 680, "PP-3105B")
        + pipe([(345, 480), (538, 520)]) + pipe([(345, 500), (538, 680)]) + pipe([(594, 498), (900, 498), (900, 380), (1100, 380)], "HP lift oil to trunnion pads")
        + psv(760, 440, "PSV-3105", v("PID-31-002", "PSV-3105", "Set pressure") if ("PID-31-002","PSV-3105","Set pressure") in pm._OVERRIDES else "160 bar(g)")
        + pipe([(760, 452), (760, 498)]) + pipe([(760, 428), (760, 330), (300, 330), (300, 400)], "Relief return to reservoir")
        + bubble(980, 560, "PT-3104", (900, 498)) + bubble(1150, 300, "TT-3101", (1100, 380))
        + eq_box(180, 110, ["TK-3105 LUBE OIL RESERVOIR", "Capacity: 12 m3", "Oil: ISO VG 460"]) + eq_box(620, 110, ["PP-3105A/B HP LIFT PUMPS", "Normal discharge: 120 bar(g)", "System design pressure: 170 bar(g)"], 300),
        ["PSV-3105 protects HP lift pump discharge; set pressure shall not exceed system design pressure.", "PT-3104 PALL inhibits mill start (SIF-3102).", "Coolers, filters and heaters not shown."])
    # 32-001 ball mill & cyclones
    P[("RB-4410-PID-32-001", "BALL MILL ML-3201 & CYCLONE CLUSTER CY-3201")] = (
        sym("mill", 420, 520, "ML-3201") + sym("pump", 800, 650, "PP-3201A") + sym("pump", 920, 650, "PP-3201B") + sym("cyclone", 1100, 330, "CY-3201")
        + pipe([(540, 530), (778, 650)]) + pipe([(834, 628), (1000, 628), (1000, 250), (1100, 250), (1100, 264)], "Cyclone feed S-321")
        + pipe([(1100, 370), (1100, 440), (300, 440), (300, 505)], "Cyclone U/F S-323") + pipe([(1122, 300), (1400, 300)], "Cyclone O/F S-324 to TK-4101")
        + eq_box(250, 110, ["ML-3201 BALL MILL", f"Size: {v('PID-32-001','ML-3201','Diameter x EGL')}", f"Motor: {v('PID-32-001','ML-3201','Installed power')} GMD"], 290)
        + eq_box(700, 110, ["PP-3201A/B/C CYCLONE FEED PUMPS", "2 duty + 1 standby (C not shown)", f"Rated: {MB['S-322']['slurry_m3h']:,} m3/h each @ SG {MB['S-322']['slurry_sg']}"], 320)
        + eq_box(1150, 110, ["CY-3201 CYCLONE CLUSTER", "16 x 660 mm", f"Feed density: {MB['S-321']['solids_w_pct']} % w/w"], 280)
        + bubble(1050, 190, "PT-3201", (1060, 250)) + bubble(960, 200, "DT-3201", (1000, 260)) + bubble(700, 760, "LIC-3201", (780, 670)),
        ["Cyclone feed hopper level LIC-3201 controls pump speed.", "Standby pump PP-3201C identical to A/B.", "Density DT-3201 is nuclear gauge - radiation permit applies."])
    # 41-001 rougher
    cells = "".join(sym("cell", 300 + i * 150, 500, f"FC-410{i+1}") + (pipe([(340 + i * 150, 500), (410 + i * 150, 500)]) if i < 6 else "") for i in range(7))
    P[("RB-4410-PID-41-001", "ROUGHER FLOTATION FC-4101 TO FC-4107")] = (
        sym("tank", 130, 480, "TK-4101") + pipe([(175, 480), (260, 500)]) + cells + pipe([(1240, 500), (1420, 500)], "Rougher tails to TH-6101")
        + pipe([(300, 440), (300, 380), (1240, 380), (1240, 260), (1420, 260)], "Rougher conc S-411 to ML-4201")
        + eq_box(420, 110, ["FC-4101 TO FC-4107 ROUGHER CELLS", "7 x 300 m3 forced-air tank cells", "Air: BL-4101A/B"], 320)
        + bubble(130, 350, "AIC-4101", (130, 430)) + bubble(600, 640, "FIC-4102", (600, 540)),
        ["Lime addition to TK-4101 on pH control AIC-4101 (set point 10.5).", "PAX and frother addition points from RB-4410-PID-45-001.", "Level control per cell by dart valves (typical)."])
    # 45-001 reagents (seeded conflicts C06, C09)
    P[("RB-4410-PID-45-001", "REAGENTS - XANTHATE, FROTHER & LIME")] = (
        sym("tank", 250, 450, "TK-4501") + sym("tank", 470, 450, "TK-4502") + sym("pump", 640, 560, "PP-4501A") + sym("fan", 250, 250, "FN-4501")
        + sym("tank", 930, 450, "TK-4511") + sym("pump", 1060, 560, "PP-4511A") + sym("tank", 1300, 450, "TK-4521")
        + pipe([(295, 470), (425, 470)]) + pipe([(515, 520), (618, 560)]) + pipe([(662, 538), (780, 538), (780, 700)], "PAX to TK-4101 / cells")
        + pipe([(250, 400), (250, 272)]) + pipe([(975, 520), (1038, 560)]) + pipe([(1082, 538), (1160, 538), (1160, 700)], "Frother to cells")
        + eq_box(120, 110, ["TK-4501 PAX MIXING TANK", "40 m3, 316L", "Enclosed room, extraction FN-4501"], 290)
        + eq_box(820, 110, ["TK-4511 FROTHER STORAGE TANK", f"Reagent: {v('PID-45-001','TK-4511','Reagent')}", "30 m3"], 330)
        + eq_box(1200, 110, ["TK-4521 MILK-OF-LIME TANK", "150 m3, 20 % w/w", "From slaker SL-4521"], 300)
        + bubble(380, 330, "LI-4501", (300, 420)) + bubble(1000, 330, "LI-4511", (960, 420)),
        ["PAX mixing room ventilation by FN-4501 (continuous).", "Frother tank bunded; area classification per RB-4410-STD-HAC-001.",
         "Lime slaker SL-4521 on vendor drawing.", "Reagent dosing rates per operating manual RB-4410-OM-001."])
    # 51-001 conc thickener
    P[("RB-4410-PID-51-001", "CONCENTRATE THICKENING & FILTRATION")] = (
        sym("thickener", 400, 420, "TH-5101") + sym("pump", 700, 600, "PP-5101A") + sym("filter", 1050, 500, "FP-5101")
        + pipe([(160, 400), (290, 400)], "Final conc S-431") + pipe([(400, 465), (400, 600), (678, 600)]) + pipe([(722, 578), (994, 500)], "Filter feed")
        + eq_box(260, 110, ["TH-5101 CONCENTRATE THICKENER", f"Diameter: {v('PID-51-001','TH-5101','Diameter')}", "High-rate, U/F 65 % w/w"], 310)
        + eq_box(930, 110, ["FP-5101 FILTER PRESS", "144 m2, cake 8.5 % moisture", "TML 9.8 %"], 280) + bubble(560, 300, "DT-5101", (430, 450)),
        ["Flocculant from TK-4531 (not shown).", "Filtrate returned to TH-5101 feedwell.", "Cake moisture must remain below TML for shipping."])
    # 61-001 tailings
    P[("RB-4410-PID-61-001", "TAILINGS THICKENING & PUMPING TO TSF")] = (
        sym("thickener", 330, 420, "TH-6101") + sym("pump", 640, 600, "PP-6101A") + sym("pump", 820, 600, "PP-6101B") + sym("pump", 1000, 600, "PP-6101C")
        + pipe([(120, 400), (220, 400)], "Tails S-611") + pipe([(330, 465), (330, 600), (618, 600)]) + pipe([(674, 578), (798, 600)]) + pipe([(854, 578), (978, 600)])
        + pipe([(1034, 578), (1400, 578)], "To TSF 6.2 km (S-621)")
        + eq_box(200, 110, ["TH-6101 TAILINGS THICKENER", "Diameter: 60 m", "U/F 62 % w/w"], 280)
        + eq_box(640, 110, ["PP-6101A/B/C TAILINGS PUMPS (SERIES)", f"Rated: {MB['S-621']['slurry_m3h']:,} m3/h", "Stage-3 discharge: 34 bar(g)",
                            f"Stage-3 casing design: {v('PID-61-001','PP-6101A','Casing design pressure (stage 3)')}"], 340)
        + bubble(1120, 480, "PT-6103", (1060, 578)) + bubble(470, 290, "LT-6101", (380, 400)),
        ["PT-6103 PAHH trips all three pumps via SIF-6101 (SIL 2).", "Pipeline pressure rating per RB-4410-STD-TSF-002.", "Flushing water connections not shown."])
    for (dwg, title), (content, nl) in P.items():
        p = d / f"{dwg}_P&ID {fname(title)}_B.pdf"
        chrome_pdf(pid_page(dwg, title, content, nl), p)
        made.append(p)

    # Drawing list + equipment list (EL-001 carries C08)
    rows = "".join(f"<tr><td class='mono'>{dwg}</td><td>{E(t)}</td><td>B</td></tr>" for (dwg, t) in P)
    body = f"<div class='page'>{banner()}<h1>P&amp;ID Drawing List - Ridgeback Concentrator</h1><p>Doc No. <b class='mono'>RB-4410-PID-00-001</b> Rev B</p><table><tr><th>Drawing</th><th>Title</th><th>Rev</th></tr>{rows}</table></div>"
    p = d / "RB-4410-PID-00-001_P&ID DRAWING LIST_B.pdf"
    chrome_pdf(doc("RB-4410-PID-00-001", body), p)
    made.append(p)
    er = "".join(f"<tr><td class='mono'><b>{e.tag}</b></td><td>{E(e.name)}</td><td>{e.area}</td><td>{E(pm.value_in('EL-001', e.tag, 'Installed power') if 'Installed power' in e.params else (e.params.get('Motor power', ('-',''))[0] + ' kW' if 'Motor power' in e.params else '-'))}</td><td>{E(e.cls)}</td></tr>" for e in pm.EQUIPMENT)
    body = f"<div class='page'>{banner()}<h1>Mechanical Equipment List</h1><p>Doc No. <b class='mono'>RB-4410-PID-00-002</b> Rev B - feeds the electrical load list</p><table><tr><th>Tag</th><th>Description</th><th>Area</th><th>Installed / motor power</th><th>Class</th></tr>{er}</table></div>"
    p = d / "RB-4410-PID-00-002_MECHANICAL EQUIPMENT LIST_B.pdf"
    chrome_pdf(doc("RB-4410-PID-00-002", body), p)
    made.append(p)
    return made


# ---------------------------------------------------------------------------
# PFDs with stream tables
# ---------------------------------------------------------------------------
def stream_table(ids: list[str]) -> str:
    keys = [("name", "Description"), ("solids_tph", "Solids t/h"), ("water_tph", "Water t/h"), ("solids_w_pct", "% solids w/w"), ("slurry_m3h", "Slurry m3/h"), ("slurry_sg", "Slurry SG")]
    head = "".join(f"<th>{i}</th>" for i in ids)
    body = "".join("<tr><th>" + lab + "</th>" + "".join(f"<td class='c'>{E(str(MB[i][k]))}</td>" for i in ids) + "</tr>" for k, lab in keys)
    return f"<table><tr><th>Stream</th>{head}</tr>{body}</table>"


def build_pfds(out: Path) -> list[Path]:
    d = out / "pfd"
    made = []
    m = MB["_meta"]
    cover = (f"<div class='page'>{banner()}<h1>Process Flow Diagrams - Cover &amp; Design Basis</h1><p>Doc No. <b class='mono'>RB-4410-PFD-000</b> Rev B</p>"
             + ds_table([(k.replace('_', ' '), str(val)) for k, val in pm.DESIGN.items()] + [("Fresh feed (grinding)", f"{m['fresh_tph']:,} t/h"), ("Concentrate", f"{m['conc_tph']} t/h"), ("Tailings", f"{m['tails_tph']:,} t/h")], "Design basis")
             + "<p>PFD-001 Crushing &amp; grinding; PFD-002 Flotation; PFD-003 Thickening, filtration &amp; tailings.</p></div>")
    p = d / "RB-4410-PFD-000_PROCESS FLOW DIAGRAM COVER AND DESIGN BASIS_B.pdf"
    chrome_pdf(doc("RB-4410-PFD-000", cover), p)
    made.append(p)
    sheets = [
        ("RB-4410-PFD-001", "CRUSHING AND GRINDING", ["S-101", "S-301", "S-305", "S-321", "S-322", "S-323", "S-324"],
         [("mill", 420, 330, "ML-3101"), ("mill", 900, 330, "ML-3201"), ("cyclone", 1250, 300, "CY-3201"), ("pump", 1080, 520, "PP-3201A"), ("crusher", 150, 320, "CR-2101")],
         f"Circulating load {int(pm.DESIGN['circulating_load']*100)} %. Cyclone feed per duty pump {MB['S-322']['slurry_m3h']:,} m3/h at {MB['S-322']['solids_w_pct']} % solids (2 duty + 1 standby)."),
        ("RB-4410-PFD-002", "FLOTATION", ["S-324", "S-411", "S-431", "S-611"],
         [("tank", 180, 320, "TK-4101"), ("cell", 450, 330, "FC-4101"), ("mill", 800, 330, "ML-4201"), ("column", 1150, 320, "FC-4301")],
         "Rougher feed pH 10.5 with lime. Collector PAX 25 g/t, frother MIBC 20 g/t."),
        ("RB-4410-PFD-003", "THICKENING, FILTRATION AND TAILINGS", ["S-431", "S-511", "S-611", "S-621"],
         [("thickener", 350, 320, "TH-5101"), ("filter", 720, 320, "FP-5101"), ("thickener", 1080, 320, "TH-6101"), ("pump", 1350, 380, "PP-6101A")],
         "Tailings to TSF at 62 % solids through 3 series pumps (6.2 km)."),
    ]
    for dwg, title, ids, syms, note in sheets:
        s = "".join(sym(k, x, y, t) for k, x, y, t in syms)
        xs = [x for _, x, _, _ in syms]
        s += "".join(pipe([(xs[i] + 70, 330), (xs[i + 1] - 70, 330)]) for i in range(len(xs) - 1))
        svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} 520' width='100%' font-family='Arial'>"
               f"<rect x='8' y='8' width='{W-16}' height='504' fill='none' stroke='#000' stroke-width='2'/>{s}"
               f"<text x='30' y='40' font-size='18' font-weight='bold'>PROCESS FLOW DIAGRAM - {title}</text>"
               f"<text x='30' y='62' font-size='12'>DWG {dwg} Rev B - {E(SITE['site'])} - SYNTHETIC DEMO</text></svg>")
        body = f"<div class='page'>{banner()}{svg}<h2>Stream table (design mass balance)</h2>{stream_table(ids)}<p><b>Basis:</b> {E(note)}</p></div>"
        p = d / f"{dwg}_PROCESS FLOW DIAGRAM {title}_B.pdf"
        chrome_pdf(doc(dwg, body, "A3 landscape"), p)
        made.append(p)
    return made


# ---------------------------------------------------------------------------
# Operating manual
# ---------------------------------------------------------------------------
def build_manual(out: Path) -> list[Path]:
    m = MB["_meta"]
    cyc_om = pm.value_in("OM-RB-001", "CY-3201", "Feed density")
    sec = []

    def S(h: str, *paras: str) -> None:
        sec.append(f"<h2>{E(h)}</h2>" + "".join(p if p.startswith("<") else f"<p>{E(p)}</p>" for p in paras))

    def tbl(rows: list[tuple[str, ...]], head: tuple[str, ...]) -> str:
        return "<table><tr>" + "".join(f"<th>{E(h)}</th>" for h in head) + "</tr>" + "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in r) + "</tr>" for r in rows) + "</table>"

    S("1. Purpose and scope", "This manual describes normal operation, start-up, shutdown and abnormal situations for the Ridgeback Concentrator (Areas 21 to 61). It is written for control room operators, metallurgists and maintenance planners.",
      "Design values are taken from the process data sheets and the process flow diagrams (RB-4410-PFD-000 to 003). Where this manual gives an operating target it is noted as such.")
    S("2. Plant overview", f"Run-of-mine ore is crushed in the primary gyratory crusher CR-2101 and conveyed to the coarse ore stockpile. The grinding circuit (SAG mill ML-3101, pebble crusher CR-3102, ball mill ML-3201 and cyclone cluster CY-3201) treats {m['fresh_tph']:,} t/h at 93 % availability (60,000 t/d).",
      f"Cyclone overflow at P80 150 um feeds rougher flotation (FC-4101 to FC-4107). Rougher concentrate is reground in ML-4201 to P80 38 um and cleaned in column FC-4301 to a 26 % Cu concentrate ({m['conc_tph']} t/h). Concentrate is thickened (TH-5101) and filtered (FP-5101). Tailings ({m['tails_tph']:,} t/h) are thickened in TH-6101 and pumped to the TSF.")
    for a, name in pm.AREAS.items():
        eqs = [e for e in pm.EQUIPMENT if e.area == a]
        rows = [(e.tag, e.name, "; ".join(f"{k}: {pm.value_in('OM-RB-001', e.tag, k)}" for k in list(e.params)[:3])) for e in eqs]
        S(f"3.{a} Area {a} - {name}", f"Principal equipment in Area {a}:", tbl(rows, ("Tag", "Equipment", "Key design data")))
    S("4. Grinding circuit operating targets",
      tbl([("SAG mill feed rate", f"{m['fresh_tph']:,} t/h", "WIC-3101"), ("SAG mill solids", "75 % w/w", "FIC-3103 water ratio"),
           ("SAG mill power", "18 - 21 MW", "Speed and feed rate"), ("Ball mill power", "19 - 21 MW", "-"),
           ("Cyclone feed density (design)", cyc_om, "DT-3201 / dilution water"), ("Cyclone feed pressure", "100 - 130 kPa", "PT-3201"),
           ("Cyclone overflow P80", "150 um", "PSI analyser"), ("Circulating load", "250 - 300 %", "Calculated")], ("Variable", "Target", "Control")),
      "Operating the cyclones above the design feed density coarsens the overflow and reduces rougher recovery. Operators should reduce feed rate before exceeding the target.")
    S("5. SAG mill start-up",
      "<ul><li>Confirm lube and hydrostatic lift system running, PT-3104 above 90 bar(g) (start permissive SIF-3102).</li><li>Confirm TT-3101/TT-3102 healthy and below alarm (TAH 70 degC).</li>"
      "<li>Check for frozen (locked) charge after a stop longer than 4 hours: inch the mill using GMD inching mode and observe the charge.</li><li>Start the mill at 70 % critical speed, then introduce feed at 50 % of target over 15 minutes.</li>"
      "<li>Start cyclone feed pumps PP-3201A and B before mill discharge reaches the hopper.</li></ul>")
    S("6. SAG mill shutdown and relining",
      "For a planned stop, run the mill empty (grind-out) for 10 to 15 minutes to reduce charge weight. Isolate the GMD at the 33 kV feeder and apply personal locks per site standard RB-4410-SG-005 (mill isolation).",
      "Relining uses the mill relining machine; the liner handler must not be used while the mill is on inching drive. Typical SAG reline duration is 72 to 96 hours.")
    S("7. Abnormal situations - grinding",
      tbl([("SAG bearing temperature high", "Lube oil flow loss, cooler fouling", "TAH 70 degC alarm; SIF-3101 trips mill at TAHH"),
           ("Locked charge", "Stop longer than 4 h with fine ore", "Inch mill; never start at full speed with frozen charge"),
           ("Cyclone roping", "Feed density too high or pump under capacity", "Add dilution water, check pump speed"),
           ("Hopper overflow / sanding", "Cyclone feed pump under capacity", "Reduce fresh feed; start standby pump")], ("Symptom", "Likely cause", "Response")))
    S("8. Reagent handling",
      "PAX (potassium amyl xanthate) is delivered as pellets and mixed to 20 % w/v in TK-4501. Xanthate decomposes in contact with moisture, heat or acid and releases carbon disulfide (CS2), which is highly flammable (LEL 1.3 %, auto-ignition 90 degC) and toxic.",
      "<ul><li>Keep the mixing room extraction fan FN-4501 running whenever PAX is present.</li><li>Do not mix PAX with water above 40 degC.</li><li>Use non-sparking tools in the mixing room.</li><li>Dosing: PAX 25 g/t, frother 20 g/t, lime to pH 10.5.</li></ul>",
      "Frother is stored in TK-4511 (MIBC, flash point 41 degC). The storage area is classified Zone 2.",
      "Quicklime is slaked in SL-4521; the reaction is strongly exothermic. Wear face shields and chemical gloves when handling lime slurry.")
    S("9. Flotation operation", tbl([("Rougher feed pH", "10.5"), ("Rougher residence time", "32 min"), ("Regrind P80", "38 um"), ("Final concentrate grade", "26 % Cu"), ("Cu recovery", "89 %"), ("Au recovery", "70 %")], ("Variable", "Target")))
    S("10. Concentrate thickening and filtration", "Maintain TH-5101 underflow at 65 % solids. Filter cake moisture must stay below the transportable moisture limit (TML 9.8 %); target 8.5 %.")
    S("11. Tailings pumping", f"Three pumps in series (PP-6101A/B/C) deliver {MB['S-621']['slurry_m3h']:,} m3/h to the TSF at 62 % solids. Stage-3 discharge is normally 34 bar(g). PT-6103 PAHH at 38 bar(g) trips all pumps via SIF-6101 (SIL 2).",
      "After a trip, flush the line with water before restart to prevent sanding. Report any pipeline pressure excursion to the Engineer of Record for the TSF.")
    S("12. Safety instrumented functions (summary)", tbl([(t, s, a, f) for t, s, _, a, f in pm.INSTRUMENTS if f not in ("-",)], ("Tag", "Service", "Alarm / trip", "Function")),
      "The cause & effect matrix RB-4410-STD-CE-001 is the controlling document for SIS logic.")
    body = (f"<div class='page'>{banner()}<h1>Ridgeback Concentrator - Operating Manual</h1><p>Doc No. <b class='mono'>RB-4410-OM-001</b> Rev 2 - {E(SITE['owner'])}</p>"
            + "".join(sec) + "</div>")
    p = out / "operating_manuals" / "RB-4410-OM-001_RIDGEBACK CONCENTRATOR OPERATING MANUAL_R2.pdf"
    chrome_pdf(doc("RB-4410-OM-001", body), p)
    return [p]


# ---------------------------------------------------------------------------
# Standards: SIS C&E, HAZOP, SDS summaries, isolation standard
# ---------------------------------------------------------------------------
def build_standards(out: Path) -> list[Path]:
    d = out / "standards"
    made = []
    ce_rows = [
        ("SIF-3101", "TT-3101 / TT-3102 SAG trunnion bearing temperature", "TAHH " + pm._OVERRIDES[("CE-31-001", "TT-3101", "TAHH trip setpoint")], "1oo2", "Stop ML-3101 GMD; stop feed CV-3101", "SIL 1"),
        ("SIF-3102", "PT-3104 hydrostatic lift oil pressure", "PALL 70 bar(g)", "1oo1", "Inhibit start / stop ML-3101", "SIL 1"),
        ("SIF-6101", "PT-6103 tailings stage-3 discharge pressure", "PAHH 38 bar(g)", "2oo3", "Trip PP-6101A/B/C", "SIL 2"),
    ]
    tr = "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in r) + "</tr>" for r in ce_rows)
    body = (f"<div class='page'>{banner()}<h1>SIS Cause &amp; Effect Matrix</h1><p>Doc No. <b class='mono'>RB-4410-STD-CE-001</b> Rev B. Controlling document for safety instrumented functions (IEC 61511).</p>"
            f"<table><tr><th>SIF</th><th>Cause (initiator)</th><th>Trip set point</th><th>Voting</th><th>Effect</th><th>SIL</th></tr>{tr}</table></div>")
    p = d / "RB-4410-STD-CE-001_SIS CAUSE AND EFFECT MATRIX_B.pdf"
    chrome_pdf(doc("RB-4410-STD-CE-001", body), p)
    made.append(p)

    tr = "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in r) + "</tr>" for r in pm.HAZOP_NODES)
    rm = "".join(f"<tr><th>{l}</th>" + "".join(f"<td class='c'>{'H' if l_i + s_i >= 6 else 'M' if l_i + s_i >= 4 else 'L'}</td>" for s_i in range(1, 6)) + "</tr>" for l_i, l in enumerate(["Rare", "Unlikely", "Possible", "Likely", "Almost certain"], 1))
    body = (f"<div class='page'>{banner()}<h1>HAZOP Study - Concentrator (Selected Nodes)</h1><p>Doc No. <b class='mono'>RB-4410-STD-HAZOP-001</b> Rev 1. Recommendations are mandatory unless formally closed.</p>"
            f"<table><tr><th>Node ref</th><th>Node</th><th>Deviation</th><th>Cause</th><th>Consequence</th><th>Existing safeguard</th><th>Recommendation</th></tr>{tr}</table>"
            f"<h2>Risk matrix (likelihood x severity 1-5)</h2><table><tr><th></th>{''.join(f'<th>S{i}</th>' for i in range(1,6))}</tr>{rm}</table></div>")
    p = d / "RB-4410-STD-HAZOP-001_HAZOP STUDY CONCENTRATOR_R1.pdf"
    chrome_pdf(doc("RB-4410-STD-HAZOP-001", body), p)
    made.append(p)

    for name, formula, cas, hz, use in pm.REAGENTS:
        slug = cas.split(" ")[0]
        body = (f"<div class='page'>{banner()}<h1>Safety Data Sheet Summary - {E(name)}</h1><p class='sm'>Site summary for demonstration. Refer to the supplier SDS for the authoritative document.</p>"
                + ds_table([("1. Identification", f"{name}; use: {use}"), ("CAS No.", cas), ("Formula / type", formula), ("2. Hazards identification", hz),
                            ("4. First aid", "Remove to fresh air; flush eyes and skin with water for 15 minutes; seek medical attention."),
                            ("5. Fire fighting", "Dry chemical, CO2 or foam. Do not use water jet on burning xanthate."),
                            ("7. Handling and storage", "Store cool and dry, away from acids and ignition sources; keep containers closed."),
                            ("8. Exposure controls", "Local exhaust ventilation; chemical goggles; nitrile gloves; respirator where exposure limits may be exceeded.")], "SDS sections") + "</div>")
        p = d / f"SDS_{slug}_{name.split(' (')[0].lower().replace(' ', '-').replace('/', '-')}.pdf"
        chrome_pdf(doc(name, body), p)
        made.append(p)

    body = (f"<div class='page'>{banner()}<h1>Site Standard - Grinding Mill Isolation and Entry</h1><p>Doc No. <b class='mono'>RB-4410-SG-005</b> Rev 3</p>"
            "<ul><li>Isolate the GMD at the 33 kV feeder and the cycloconverter; verify zero energy by attempted start.</li><li>Isolate lube and hydrostatic lift systems; bleed PT-3104 to zero.</li>"
            "<li>Chock the mill shell before any person enters; inching drive is locked out during entry.</li><li>Confined-space entry permit and gas test required (no CS2 source expected, but flotation area is adjacent).</li>"
            "<li>Liner handler operation requires a dedicated spotter and exclusion zone.</li></ul></div>")
    p = d / "RB-4410-SG-005_GRINDING MILL ISOLATION AND ENTRY STANDARD_R3.pdf"
    chrome_pdf(doc("RB-4410-SG-005", body), p)
    made.append(p)
    return made


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="corpora/copper-concentrator/raw")
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists():
        shutil.rmtree(out)
    made = build_datasheets(out) + build_pids(out) + build_pfds(out) + build_manual(out) + build_standards(out)
    for sub in sorted({p.parent.name for p in made}):
        print(f"{sub:20s} {sum(1 for p in made if p.parent.name == sub)}")
    print("total", len(made))


if __name__ == "__main__":
    main()
