---
name: review-panel
description: "Run a disciplined, simulated NSF/venue review panel on a working draft: six frozen reviewer seats plus a per-run wildcard seat, blind to each other, with a human checkpoint before anything runs, a color-annotated Word deliverable, and a cross-run issue ledger. Triggers on: run a review, review my proposal, review panel, panel review, run the reviewers, /review."
---

# Review Panel

This skill runs the review-panel system defined in this folder's
`REVIEW-INSTRUCTIONS.md`. That file is the single source of truth; this skill is
the entry point.

When invoked:

1. Read `REVIEW-INSTRUCTIONS.md` in the current project folder (if the project
   does not have one, offer to scaffold the project with `setup.sh` from this
   skill's folder first).
2. Follow the `/review` flow defined in `commands/review.md`: inspect
   `document to review/`, present the options (venue variant from `venues/`,
   run type, maturity, the wildcard card), state the §3 checkpoint, and wait
   for the user's explicit green flag before running anything.
3. Execute the pipeline per §4 and §5 with the §4c prompts verbatim; assemble
   the deliverable with `scripts/build_review_docx.py`; update the logs per §8.

Wildcard seat (§11): generate the Reviewer Configuration Card using the
`academic-paper-reviewer` skill's field-analysis agent if installed under
`~/.claude/skills/`; otherwise use the vendored copy at
`third_party/academic-research-skills/field_analyst_agent.md` (see the NOTICE
there for attribution and license).

Hard rules, non-negotiable: reviewers see only the document (§4b); prompts are
never rephrased inline (§4c); nothing runs before the human green flag (§3);
"fix drafted" never counts as resolved in the ledger (§8).
