---
description: Run the AI review panel on the document in "document to review/"
---

You are running the review-panel system. The single source of truth is the
`REVIEW-INSTRUCTIONS.md` file in this project folder. Do the following, in order:

1. Read `REVIEW-INSTRUCTIONS.md` in full. It defines the pipeline, the frozen
   reviewer prompts (§4c), the purity rules (§4b), the output format (§5), the
   logs (§8), and the wildcard seat (§11). Follow it exactly; never rephrase the
   frozen prompts.

2. Look in `document to review/`. If it is empty, say so and stop. If it holds a
   document, note its exact filename and last-modified time. If the document
   contains margin comments, ask the user whether the reviewers should see them.

3. Present the user a short set of choices before anything runs:
   - Venue: if a `venues/` folder exists in the project, list its variants and
     ask which one applies (default: the process file's own §2 target). A venue
     variant replaces only the pieces it names (shared calibration, PF lens);
     everything else runs as shipped.
   - Run type: CLEAN (default), FOCUSED (§9, user must name the focus areas), or
     GAP-FILL (§10).
   - Maturity: draft (default) or final (§2).
   - Wildcard seat: generate the Reviewer Configuration Card per §11, using
     the `academic-paper-reviewer` field-analysis agent from
     `~/.claude/skills/academic-paper-reviewer/agents/` if installed, else the
     vendored copy at `third_party/academic-research-skills/`. Include the card
     in the checkpoint for approval or veto. If neither source is available,
     say the run proceeds with the frozen seats only.

4. State the full pre-run checkpoint per §3: input file and date, panel
   configuration, maturity mode, stages, and (for FOCUSED) the focus areas plus
   any area dropped since the previous run. Then WAIT for the user's explicit
   green flag. Nothing runs without it.

5. On the green flag, execute the pipeline per §4 and §5: create the run folder,
   extract the document (`scripts/extract_document.py` if this project has the
   scripts; otherwise equivalent means), dispatch every seat in parallel with its
   §4c text verbatim plus only the document, then write the synthesis, the
   annotations, the deliverable (`scripts/build_review_docx.py`), the continuity
   map, and the log updates. Report the outcome in plain language: ratings, the
   headline findings, and where the deliverable is.

Throughout: reviewers see only the document. No ledger, no prior findings, no
steering. All output in English.
