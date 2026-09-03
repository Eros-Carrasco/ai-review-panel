#!/bin/sh
# Scaffold a new review-panel project folder.
# Usage: ./setup.sh /path/to/my-project
set -e
REPO="$(cd "$(dirname "$0")" && pwd)"
TARGET="$1"
if [ -z "$TARGET" ]; then
  echo "usage: ./setup.sh /path/to/my-project"
  exit 1
fi
mkdir -p "$TARGET/document to review" "$TARGET/reviewed documents" "$TARGET/log" \
         "$TARGET/scripts" "$TARGET/.claude/commands"
cp "$REPO/REVIEW-INSTRUCTIONS.md" "$TARGET/"
cp "$REPO/templates/ISSUES.md" "$REPO/templates/REVIEW-LOG.md" "$TARGET/log/"
cp "$REPO/scripts/extract_document.py" "$REPO/scripts/render_pdf.swift" \
   "$REPO/scripts/build_review_docx.py" "$TARGET/scripts/"
cp "$REPO/commands/review.md" "$TARGET/.claude/commands/"
mkdir -p "$TARGET/venues"
cp "$REPO/venues/"*.md "$TARGET/venues/"
mkdir -p "$TARGET/third_party/academic-research-skills"
cp "$REPO/third_party/academic-research-skills/"*.md "$TARGET/third_party/academic-research-skills/"
echo "Project scaffolded at: $TARGET"
echo
echo "Next steps:"
echo "  1. Drop your draft (.docx or .pdf) into: $TARGET/document to review/"
echo "  2. Open Claude Code in $TARGET"
echo "  3. Type /review, pick your options, and give the green flag."
