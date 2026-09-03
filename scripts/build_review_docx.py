#!/usr/bin/env python3
"""Build the color-annotated full-review.docx from a run archive.

Usage:
  python3 build_review_docx.py <archive-dir> <output.docx> ["Document title"]

Expects inside <archive-dir>:
  proposal-text-as-reviewed.txt   the reviewed text with "=== PAGE N ===" markers
  annotations.json                {snap, consensus, annotations:[{anchor, comments:[[seat,label,text]], fix}]}
  report-PF.md ... report-R4.md   the five reviews, verbatim
  synthesis.md                    optional; its "Fix list, in order" goes on the cover,
                                  the rest is appended to Part 2
  team-comments-answers.md or
  team-questions-answers.md       optional; appended to Part 2

The output opens in Word and imports to Google Docs with colors intact.
Anchors are matched as substrings of the reassembled paragraphs.
"""
import html
import json
import os
import re
import sys
import zipfile

COL = {"PF": "806000", "R1": "C00000", "R2": "2E7D32", "R3": "C55A11",
       "R4": "0B6E6E", "R5": "6A1B9A", "W": "5D4037", "FIX": "1F4E79", "GRAY": "808080"}
ROLE = {"PF": "Program Fit, Completeness & Overall Merit",
        "R1": "Methodology & Evaluation",
        "R2": "Domain, Related Work & Novelty",
        "R3": "AI Systems & Broader Impacts",
        "R4": "Devil's Advocate",
        "R5": "XR Systems Engineering",
        "W": "Wildcard"}
SEATS = ["PF", "R1", "R2", "R3", "R4", "R5", "W"]

CONTENT_TYPES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>')
RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
DOC_RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
STYLES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
    '<w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr></w:rPrDefault>'
    '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
    '<w:pPr><w:spacing w:before="360" w:after="160"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>'
    '<w:pPr><w:spacing w:before="280" w:after="120"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/>'
    '<w:pPr><w:spacing w:before="240" w:after="100"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:sz w:val="25"/><w:szCs w:val="25"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading4"><w:name w:val="heading 4"/><w:basedOn w:val="Normal"/>'
    '<w:pPr><w:spacing w:before="200" w:after="80"/><w:outlineLvl w:val="3"/></w:pPr><w:rPr><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style></w:styles>')


def esc(s):
    return html.escape(s, quote=False)


def run(text, color=None, bold=False, italic=False):
    rpr = ""
    if bold: rpr += "<w:b/>"
    if italic: rpr += "<w:i/>"
    if color: rpr += '<w:color w:val="%s"/>' % color
    if rpr: rpr = "<w:rPr>%s</w:rPr>" % rpr
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, esc(text))


def inline_md(text, color=None):
    out, pos = [], 0
    for m in re.finditer(r"\*\*(.+?)\*\*|\*(.+?)\*", text):
        if m.start() > pos: out.append(run(text[pos:m.start()], color))
        if m.group(1) is not None: out.append(run(m.group(1), color, bold=True))
        else: out.append(run(m.group(2), color, italic=True))
        pos = m.end()
    if pos < len(text): out.append(run(text[pos:], color))
    return "".join(out)


def para(runs, style=None, indent=None, before=None, after=None):
    ppr = ""
    if style: ppr += '<w:pStyle w:val="%s"/>' % style
    if indent: ppr += '<w:ind w:left="%d"/>' % indent
    if before is not None or after is not None:
        ppr += '<w:spacing w:before="%d" w:after="%d"/>' % (before or 0, after or 120)
    if ppr: ppr = "<w:pPr>%s</w:pPr>" % ppr
    return "<w:p>%s%s</w:p>" % (ppr, runs)


def heading(text, level, color=None):
    return para(run(text, color), style="Heading%d" % level)


def gray(text, bold=False):
    return para(run(text, COL["GRAY"], bold=bold))


def pagebreak():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def comment(seat, label, text):
    return para(run("■ %s · %s | %s: " % (seat, ROLE[seat], label), COL[seat], bold=True)
                + run(text, COL[seat]), indent=360, before=60, after=60)


def fixline(text):
    return para(run("■ FIX: ", COL["FIX"], bold=True) + run(text, COL["FIX"]),
                indent=360, before=40, after=120)


def md_to_ooxml(md, seat=None, color_body=None):
    out = []
    for line in md.split("\n"):
        s = line.rstrip()
        if not s.strip() or s.strip() == "---": continue
        if s.startswith("## "): out.append(heading(s[3:].strip(), 3, COL.get(seat) if seat else None)); continue
        if s.startswith("### "): out.append(heading(s[4:].strip(), 4)); continue
        if s.startswith("# "): continue
        if s.startswith("|"):
            if set(s.replace("|", "").strip()) <= set("-: "): continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            out.append(para(inline_md("  |  ".join(cells), color_body), indent=360)); continue
        m = re.match(r"^\s*([-•*])\s+(.*)", s)
        if m: out.append(para(run("• ", color_body) + inline_md(m.group(2), color_body), indent=360, before=40, after=40)); continue
        m = re.match(r"^\s*(\d+)\.\s+(.*)", s)
        if m: out.append(para(run(m.group(1) + ". ", color_body, bold=True) + inline_md(m.group(2), color_body), indent=360, before=60, after=60)); continue
        out.append(para(inline_md(s, color_body)))
    return "".join(out)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    arch, out_path = sys.argv[1], sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else os.path.basename(os.path.dirname(os.path.abspath(arch)))

    ann = json.load(open(os.path.join(arch, "annotations.json")))
    anchors = [(a["anchor"], a["comments"], a.get("fix")) for a in ann.get("annotations", [])]
    synth = ""
    sp = os.path.join(arch, "synthesis.md")
    if os.path.exists(sp): synth = open(sp).read()

    body = []
    # PART 0 — cover (kept to what the team shares; version metadata lives in archive/README.md)
    body.append(heading("AI PANEL REVIEW", 1))
    body.append(heading("Color legend", 2))
    for s in SEATS:
        body.append(para(run("■ %s — %s" % (s, ROLE[s]), COL[s], bold=True)))
    body.append(para(run("■ FIX — suggested fixes by Claude Fable (has context of previous drafts)", COL["FIX"], bold=True)))
    body.append(heading("NSF panel snapshot", 2))
    for s, r in ann.get("snap", []):
        body.append(para(run("%s — %s: " % (s, ROLE.get(s, s)), COL.get(s), bold=True) + run(r, "000000"), indent=360))
    if ann.get("consensus"):
        body.append(md_to_ooxml(ann["consensus"]))
    if "## Fix list, in order" in synth:
        body.append(heading("Fix list, in order", 2))
        body.append(md_to_ooxml(synth.split("## Fix list, in order")[1].split("\n## ")[0]))

    # PART 1 — annotated document
    body.append(pagebreak())
    body.append(heading("PART 1 — ANNOTATED DOCUMENT", 1))
    used = set()

    def annotate(t):
        out = []
        for idx, (anchor, comments, fix) in enumerate(anchors):
            if idx in used: continue
            if anchor in t:
                used.add(idx)
                for seat, label, ctext in comments:
                    out.append(comment(seat, label, ctext))
                if fix: out.append(fixline(fix))
        return out

    buf = []

    def flush():
        if buf:
            t = " ".join(buf)
            body.append(para(run(t)))
            body.extend(annotate(t))
            buf.clear()

    for l in open(os.path.join(arch, "proposal-text-as-reviewed.txt")):
        l = l.rstrip()
        if l.startswith("=== APPENDIX ==="): break
        m = re.match(r"=== PAGE (\d+) ===", l)
        if m:
            flush(); body.append(para(run("— PAGE %s —" % m.group(1), COL["GRAY"], bold=True))); continue
        if re.match(r"Commented \[", l):
            flush(); body.append(para(run("[margin comment] " + re.sub(r"Commented \[\d+\]:\s*", "", l), COL["GRAY"], italic=True))); continue
        if re.match(r"\[FIGURE \d+", l):
            flush(); body.append(para(run(l, COL["GRAY"], italic=True))); continue
        if not l.strip():
            flush(); continue
        if re.match(r"^[●○]", l.strip()):
            flush()
        buf.append(l.strip())
        joined = " ".join(buf)
        if (joined.endswith((".", ":", "?")) and len(joined) > 180) or len(joined) > 900:
            flush()
    flush()
    missing = [anchors[i][0] for i in range(len(anchors)) if i not in used]
    if missing:
        print("WARNING - unmatched anchors:", missing)

    # PART 2 — full reports
    body.append(pagebreak())
    body.append(heading("PART 2 — FULL PANEL REPORT", 1))
    for s in SEATS:
        rp = os.path.join(arch, "report-%s.md" % s)
        if os.path.exists(rp):
            body.append(md_to_ooxml(open(rp).read(), seat=s))
    for extra, head in [("team-comments-answers.md", "The team's margin comments, and what the panel said"),
                        ("team-questions-answers.md", "The team's questions, and what the panel said")]:
        ep = os.path.join(arch, extra)
        if os.path.exists(ep):
            body.append(heading(head, 2))
            body.append(md_to_ooxml(open(ep).read()))
    if synth:
        body.append(heading("Synthesis", 2))
        sb = "## Ratings" + synth.split("## Ratings")[1] if "## Ratings" in synth else synth
        body.append(md_to_ooxml(sb))

    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
           + "".join(body) +
           '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
           '<w:pgMar w:top="1200" w:right="1200" w:bottom="1200" w:left="1200"/></w:sectPr></w:body></w:document>')
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/document.xml", doc)
    print("wrote", out_path, os.path.getsize(out_path), "bytes;",
          len(anchors), "anchors,", sum(len(c) for _, c, _ in anchors), "comments")


if __name__ == "__main__":
    main()
