#!/usr/bin/env python3
"""Extract a document for the review panel.

Usage:
  python3 extract_document.py <input.docx|input.pdf> <output-dir>

For a .docx: writes <output-dir>/proposal-text-as-reviewed.txt with estimated
"=== PAGE N ===" markers (a marker roughly every 3000 characters) and, if the
file embeds images, saves them under <output-dir>/figures/ with [FIGURE N]
markers in the text.

For a .pdf (macOS only): calls scripts/render_pdf.swift to render every page to
<output-dir>/pages/page-NN.png and writes proposal-text-as-reviewed.txt with the
PDF's real page markers. Reviewers can then be pointed at both the text and the
page images.
"""
import os
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
CHARS_PER_PAGE = 3000


def extract_docx(path, outdir):
    z = zipfile.ZipFile(path)
    rels = {r.get("Id"): r.get("Target")
            for r in ET.fromstring(z.read("word/_rels/document.xml.rels"))}
    body = ET.fromstring(z.read("word/document.xml")).find(W + "body")
    figdir = os.path.join(outdir, "figures")
    lines, page, chars, fig = ["=== PAGE 1 ==="], 1, 0, 0

    def add(line):
        nonlocal page, chars
        lines.append(line)
        chars += len(line) + 1
        if chars > CHARS_PER_PAGE:
            page += 1
            chars = 0
            lines.append("=== PAGE %d ===" % page)

    def walk_paragraph(p):
        nonlocal fig
        for blip in p.iter(A + "blip"):
            target = rels.get(blip.get(R + "embed"))
            if target:
                fig += 1
                os.makedirs(figdir, exist_ok=True)
                name = "figure-%02d%s" % (fig, os.path.splitext(target)[1])
                with open(os.path.join(figdir, name), "wb") as f:
                    f.write(z.read("word/" + target))
                add("[FIGURE %d: embedded image, see figures/%s]" % (fig, name))
        text = "".join(n.text or "" for n in p.iter(W + "t"))
        if text.strip():
            add(text)

    for el in body:
        if el.tag == W + "p":
            walk_paragraph(el)
        elif el.tag == W + "tbl":
            for p in el.iter(W + "p"):
                walk_paragraph(p)
    out = os.path.join(outdir, "proposal-text-as-reviewed.txt")
    with open(out, "w") as f:
        f.write("\n".join(lines))
    print("wrote %s (%d estimated pages, %d figures)" % (out, page, fig))


def extract_pdf(path, outdir):
    pages = os.path.join(outdir, "pages")
    swift = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render_pdf.swift")
    subprocess.run(["swift", swift, path, pages], check=True)
    shutil.move(os.path.join(pages, "text.txt"),
                os.path.join(outdir, "proposal-text-as-reviewed.txt"))
    n = len([f for f in os.listdir(pages) if f.endswith(".png")])
    print("wrote proposal-text-as-reviewed.txt and %d page images in %s" % (n, pages))


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    path, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        extract_docx(path, outdir)
    elif ext == ".pdf":
        extract_pdf(path, outdir)
    else:
        sys.exit("unsupported file type: " + ext)


if __name__ == "__main__":
    main()
