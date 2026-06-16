#!/usr/bin/env python3
"""
build_pdfs.py - generate docs/pdf/*.pdf from the Markdown blueprint files.

Pipeline:  Markdown  --(pandoc)-->  standalone HTML  --(wkhtmltopdf)-->  PDF
Mermaid blocks are pre-rendered to PNG with mermaid-cli (mmdc) so they appear
in the PDF; on GitHub the Markdown keeps the native ```mermaid fences.

The Markdown is the single source of truth. The version/footer line is read from
each file's own footer block, so bumping the version in the Markdown updates the
PDF footer automatically. The footer is rendered as a CSS fixed element (works on
any wkhtmltopdf build, patched or not).

Usage:
    python3 build_pdfs.py                 # docs/ -> docs/pdf/
    python3 build_pdfs.py path/to/docs    # custom docs dir
    python3 build_pdfs.py docs out/pdf    # custom docs dir + output dir

Dependencies:
    pandoc        https://pandoc.org/installing.html
    wkhtmltopdf   https://wkhtmltopdf.org/downloads.html
    mmdc          npm install -g @mermaid-js/mermaid-cli   (only if files use ```mermaid)

Note: page footers/numbers require the patched-Qt wkhtmltopdf from wkhtmltopdf.org
(the Windows installer is patched). A distro `apt install wkhtmltopdf` may be an
unpatched build that silently drops footers.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AUTHOR = "Daniel Brule  \u00b7  linkedin.com/in/danielbrule"
DEFAULT_FOOTER = "Talk-to-Data Delivery Blueprint"

PRINT_CSS = """
body { font-family: "DejaVu Sans", Arial, Helvetica, sans-serif; font-size: 10.5pt;
       line-height: 1.5; color: #1a1a1a; }
header#title-block-header { border-bottom: 2px solid #3B5C9F; padding-bottom: 12px;
       margin-bottom: 24px; }
header#title-block-header h1.title { color: #2A4A86; font-size: 20pt; margin-bottom: 4px; }
header#title-block-header .author, header#title-block-header .date { color: #555;
       font-size: 10pt; margin: 0; }
h1 { color: #2A4A86; font-size: 15pt; border-bottom: 1px solid #cdd8ec; padding-bottom: 3px;
     margin-top: 22px; }
h2 { color: #34528a; font-size: 12.5pt; margin-top: 16px; }
h3 { color: #3B5C9F; font-size: 11pt; }
h1, h2, h3 { page-break-after: avoid; }
nav#TOC { border: 1px solid #cdd8ec; background: #f6f9fd; padding: 10px 16px;
          border-radius: 4px; font-size: 9.5pt; }
nav#TOC ul { list-style: none; padding-left: 14px; margin: 2px 0; }
nav#TOC > ul { padding-left: 0; }
nav#TOC a { color: #34528a; text-decoration: none; }
table { border-collapse: collapse; width: 100%; font-size: 8.5pt; margin: 10px 0; }
th, td { border: 1px solid #c9c9c9; padding: 4px 6px; text-align: left; vertical-align: top;
         overflow-wrap: anywhere; }
th { background: #eef3fb; color: #2A4A86; }
tr:nth-child(even) td { background: #fafbfe; }
code { background: #f0f2f5; padding: 1px 4px; border-radius: 3px;
       font-family: "DejaVu Sans Mono", monospace; font-size: 8.5pt; }
pre { background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 4px; padding: 10px;
      overflow-x: auto; font-size: 8.5pt; }
pre code { background: none; padding: 0; }
img { max-width: 90%; height: auto; display: block; margin: 12px auto; }
blockquote { border-left: 3px solid #3B5C9F; margin-left: 0; padding-left: 14px; color: #333; }
"""

PUPPETEER_CFG = '{ "args": ["--no-sandbox", "--disable-setuid-sandbox"] }'


def need(tool, hint):
    if shutil.which(tool) is None:
        sys.exit(f"ERROR: '{tool}' not found on PATH.\n  Install: {hint}")


def render_mermaid(body, workdir, have_mmdc):
    blocks = list(re.finditer(r"```mermaid\n(.*?)```", body, flags=re.S))
    if not blocks:
        return body
    if not have_mmdc:
        print("    ! mermaid found but 'mmdc' missing - left as code "
              "(npm install -g @mermaid-js/mermaid-cli)")
        return body
    cfg = workdir / "puppeteer.json"
    cfg.write_text(PUPPETEER_CFG)
    out = body
    for i, m in enumerate(blocks):
        mmd = workdir / f"diagram_{i}.mmd"
        png = workdir / f"diagram_{i}.png"
        mmd.write_text(m.group(1), encoding="utf-8")
        r = subprocess.run(["mmdc", "-i", str(mmd), "-o", str(png), "-b", "white",
                            "-p", str(cfg), "--scale", "2"], capture_output=True, text=True)
        if r.returncode == 0 and png.exists():
            out = out.replace(m.group(0), f"![Diagram]({png.as_posix()})")
        else:
            print(f"    ! mmdc failed on diagram {i}; left as code.")
    return out


def build(md_path, out_dir, have_mmdc):
    text = md_path.read_text(encoding="utf-8")
    title = text.split("\n", 1)[0].lstrip("# ").strip()

    fm = re.search(r"\n\n---\n\n\*(" + re.escape(DEFAULT_FOOTER) + r"[^\n*]*)\*", text)
    footer_left = fm.group(1).strip() if fm else DEFAULT_FOOTER
    if fm:
        text = text[:fm.start()]
    version = footer_left.split("\u00b7", 1)[1].strip() if "\u00b7" in footer_left else ""

    toc = text.find("**Table of contents**")
    if toc != -1:
        end = text.find("\n\n---\n\n", toc)
        if end != -1:
            text = text[end + len("\n\n---\n\n"):]

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        body = render_mermaid(text, work, have_mmdc)

        (work / "print.css").write_text(PRINT_CSS, encoding="utf-8")
        src_md = work / "in.md"
        src_md.write_text(f'---\ntitle: "{title}"\nauthor: "{AUTHOR}"\n'
                          f'date: "{version}"\n---\n\n' + body, encoding="utf-8")

        html = work / "out.html"
        r1 = subprocess.run(
            ["pandoc", str(src_md), "-o", str(html), "--standalone",
             "--toc", "--toc-depth=3", "--shift-heading-level-by=-1",
             "--embed-resources", "--css", str(work / "print.css"),
             "--metadata", "lang=en"],
            capture_output=True, text=True)
        if r1.returncode != 0:
            print(f"    ! pandoc failed:\n{r1.stderr[-400:]}")
            return False

        out_pdf = out_dir / (md_path.stem + ".pdf")
        subprocess.run(
            ["wkhtmltopdf", "--quiet", "--enable-local-file-access",
             "--margin-top", "14", "--margin-bottom", "16",
             "--margin-left", "14", "--margin-right", "14",
             "--footer-left", footer_left, "--footer-right", "[page] / [topage]",
             "--footer-font-size", "7", "--footer-spacing", "4", "--footer-line",
             str(html), str(out_pdf)],
            capture_output=True, text=True)
        return out_pdf.exists() and out_pdf.stat().st_size > 0


def main():
    docs = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs")
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else docs / "pdf"
    if not docs.is_dir():
        sys.exit(f"ERROR: docs directory not found: {docs.resolve()}")

    need("pandoc", "https://pandoc.org/installing.html")
    need("wkhtmltopdf", "https://wkhtmltopdf.org/downloads.html")
    have_mmdc = shutil.which("mmdc") is not None

    out_dir.mkdir(parents=True, exist_ok=True)
    md_files = sorted(p for p in docs.rglob("*.md")
                      if out_dir not in p.parents and p.name.lower() != "readme.md")
    if not md_files:
        sys.exit(f"No .md files found under {docs.resolve()}")

    print(f"Building {len(md_files)} PDFs -> {out_dir}/  (mermaid: {'on' if have_mmdc else 'off'})")
    ok = 0
    for md in md_files:
        print(f"  {md.relative_to(docs)}")
        if build(md, out_dir, have_mmdc):
            ok += 1
    print(f"\nDone: {ok}/{len(md_files)} PDFs written to {out_dir}/")
    sys.exit(0 if ok == len(md_files) else 1)


if __name__ == "__main__":
    main()
