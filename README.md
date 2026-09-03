# AI Review Panel

A disciplined way to run a simulated NSF-style review panel on a working draft, using Claude Code. A panel of blind reviewer agents reads the document: five core frozen seats always, plus two optional seats you choose per run (a sixth frozen XR-systems seat, and a wildcard whose identity is generated fresh for each document) (no steering, no history, no sight of each other), each writes a full report, and the results are assembled into a color-annotated Word document the team can read side by side with the draft, plus a running ledger that tracks every finding across runs.

This is the system used by the Future Reality Lab to iterate an NSF CISE/IIS HCC proposal through repeated review rounds. The process file (`REVIEW-INSTRUCTIONS.md`) is the system; everything else here supports it.

## What you need

- **Claude Code** (terminal app or IDE extension) with access to a top-tier Claude model. The panel quality depends directly on the model; this system was built and validated on Claude Fable.
- **macOS** if you want PDF inputs rendered to page images (the renderer uses Apple's PDFKit). Word (.docx) inputs work anywhere.
- A document to review (.docx or .pdf).

## Quick start

```
git clone <this repo>
cd ai-review-panel
./setup.sh ~/my-project
```

Then drop your draft (.docx or .pdf) into `~/my-project/document to review/`,
open Claude Code in `~/my-project`, and type **`/review`**. Claude presents the
options (run type, draft or final, the wildcard card if the skill is installed),
states the checkpoint, and waits for your green flag. When it finishes, open the
`full-review.docx` in the new run folder under `reviewed documents/`.

## Folder layout for a project

Create a working folder for your project (not inside this repo) with:

```
my-project/
├─ REVIEW-INSTRUCTIONS.md     ← copy from this repo
├─ document to review/        ← drop the draft here before a run
├─ reviewed documents/        ← each run creates its folder here
└─ log/
   ├─ REVIEW-LOG.md           ← copy from templates/
   └─ ISSUES.md               ← copy from templates/
```

See `templates/folder-layout.md` for details.

## How a run works

1. Put the draft in `document to review/`.
2. Open Claude Code in the project folder and ask for a review run.
3. Claude states a **checkpoint**: which file it picked, the panel configuration, the mode (draft or final), and which stages will run. **Nothing runs until you give the green flag.** This step is not ceremony; it is where scope mistakes get caught.
4. The reviewer agents run in parallel: the core seats with their §4c prompts, verbatim, plus whichever optional seats you chose (R5 with its frozen prompt; W with its per-run card). They see only the document. As a cost guide: each seat is roughly 45-70k tokens on a 15-page document; the wildcard costs about two seats, because its card is generated first.
5. Claude assembles the outputs: the reports, a synthesis (agreements, disagreements, prioritized fixes), the annotated `full-review.docx`, a post-hoc comparison against the issue ledger, and updates to the two logs.

The scripts in `scripts/` are the mechanical parts Claude uses along the way:

- `extract_document.py` — turns a .docx or .pdf into reviewer-ready text with page markers (and page images for PDFs).
- `render_pdf.swift` — the macOS PDF renderer the extractor calls.
- `build_review_docx.py` — turns a run's archive into the color-annotated Word deliverable.

**The scripts alone do not produce a review.** Between extraction and the deliverable there is a step only Claude performs during the run: reading the reports, writing the synthesis, and deciding which reviewer comment attaches to which passage of the document (that mapping is saved as `annotations.json` in the run's archive, and `build_review_docx.py` reads it). Cloning this repo gives you the process and the tooling; running a review requires Claude Code in the loop.

## Figures and margin comments

What the reviewers see depends on the input type, and comments are always an explicit choice, never an accident:

- **.docx input:** the extractor pulls the text and every embedded figure (reviewers get the images as files). If the file stores margin comments, the extractor also writes them out (author, anchored passage, text) to `team-comments.md`.
- **.pdf input (macOS):** every page is rendered to an image, so reviewers see exactly what is on the page — including margin comments if the PDF was exported with them.
- **At the checkpoint,** if comments exist, you choose one of three: hide them from the reviewers; show them as part of the document; or show them plus an appendix listing each comment, which every reviewer must address in a dedicated section of their report. Figures are always shown.

## Map of the process file, section by section

`REVIEW-INSTRUCTIONS.md` is the whole system. This is what each section does and why it exists:

- **Folder layout.** The project folder convention: `document to review/` (input), `reviewed documents/` (one folder per run, never overwritten), `log/` (the two registers). The document is *moved* into the run folder, so every run folder holds exactly what was reviewed.

- **§1 Input.** Which file gets reviewed (the most recent in `document to review/`) and the rule that its exact filename and modification time are recorded in every output, because drafts circulate in many versions and "which version did the panel see" must never be a guess.

- **§2 Target program and maturity.** What the panel judges against. The venue (NSF HCC as shipped; see `venues/` for variants) and the maturity mode: in **draft** mode, placeholders, TODOs and typos go into a short checklist and do not drag the score; in **final** mode everything counts, which is the dress rehearsal for submission.

- **§3 Pre-run checkpoint (green flag).** Before anything runs, Claude states what it is about to do: the file it picked, the panel, the mode, the stages, what happens with any margin comments (hide / show / show plus an appendix the reviewers must address), and (for FOCUSED runs) the focus areas plus anything dropped since the last run. The human approves or corrects. This section exists because scope mistakes are cheap here and expensive after a run.

- **§4 The pipeline.** The stages of a run: panel review, then editorial synthesis (agreements, disagreements recorded rather than averaged away, a prioritized fix list). Cross-stage rules live here too: suggested references must be real publications, and no institution facts may be invented.

- **§4b Review purity.** The load-bearing idea, in two layers. Layer 1: reviewers receive the document and the base calibration, *nothing else*: no ledger, no earlier findings, no hints, no sight of each other. Layer 2: after the reports exist, the orchestrator (not the reviewers) compares them against the ledger to compute what was resolved, what persists, and what is new. Because nothing is ever fed forward, a finding that reappears across runs is independent corroboration rather than an echo.

- **§4c Frozen reviewer prompts.** The full text every seat receives: one shared calibration (criteria, mode, format) plus one lens per seat: PF (venue fit and completeness), R1 (methodology and statistics), R2 (related work and novelty, including a citation-integrity audit), R3 (AI systems, Broader Impacts, privacy), R4 (Devil's Advocate, who must build the strongest case *against*), R5 (XR systems engineering). "Frozen" means used verbatim, every run: change them only here, in git, where the change is visible, because ratings across runs are comparable only while the instrument holds still.

- **§5 Output.** What a run produces: the run folder, the `full-review.docx` (Part 0: a clean cover with only the color legend, per-seat ratings and the fix list — no banners or run metadata, which live in the archive; Part 1: the full draft in black with each reviewer's comments inline, in that reviewer's color, right after the passage they discuss; Part 2: the five complete reports and the synthesis), and the `archive/` with every machine-readable piece, including which exact document version was reviewed. Everything the orchestrator writes is in plain language; reviewer reports appear verbatim.

- **§6 Color legend.** Each seat's fixed color in the deliverable, stable across runs so readers learn to recognize voices: PF dark gold, R1 red, R2 green, R3 orange, R4 teal, R5 purple, W brown, FIX suggestions blue, scaffolding gray.

- **§7 Q&A mode.** You can interrogate any past run ("why did R1 reject the power analysis?", "what changed between versions?") without triggering a new review; answers come from the archives and cite run, section and page. Q&A never modifies outputs.

- **§8 Logs.** The memory of the project. `REVIEW-LOG.md` is the dashboard: one row per run with ratings and a short narrative. `ISSUES.md` is the ledger: every unique finding gets a stable ID (F01, F02, …) and a status updated after each run. The strictest rule of the system lives here: a drafted fix never counts as resolved — only a *reviewed document version* that incorporates the fix does.

- **§9 FOCUSED review (opt-in).** A steered variant where the user names areas for the panel to concentrate on. Useful before deadlines; the price is honesty about evidence: findings from steered runs are marked as such and never counted as independent corroboration, and their ratings are not compared with clean runs.

- **§10 GAP-FILL session (opt-in).** A generative advisory mode: writer seats draft the text a to-do list asks for (each in its own lane), and a Devil's Advocate stress-tests every drafted passage. Output is working material for the team to curate, never a review, and it stays out of review documents.

- **§11 Wildcard seat.** One extra reviewer per run whose identity is *generated fresh* for the current document by the `academic-paper-reviewer` skill's field-analysis agent, deliberately covering an angle the frozen seats do not. Its card is shown at the checkpoint for approval or veto and archived with the run; its findings are tagged `wildcard` in the ledger and its rating is listed separately, because a lens that changes every run cannot be compared across runs. The frozen seats measure progress; the wildcard hunts blind spots.

## The rules that make it work

Read `REVIEW-INSTRUCTIONS.md` in full before the first run. The load-bearing rules:

- **Frozen prompts (§4c).** The reviewer prompts are used verbatim, every run. If they need improvement, change them here in git, where the change is visible, never inline for one run.
- **Review purity (§4b).** Reviewers never see the issue ledger, earlier findings, or the team's deliberations. Continuity is computed afterward by the orchestrator, in the logs. The moment a reviewer is steered, its findings stop being independent evidence.
- **Checkpoint and green flag (§3).** Every run is approved by a human first, and any change of scope between runs is called out explicitly, never folded silently into a list.
- **The ledger (§8).** Every finding gets a stable ID and a status. "A fix was drafted" never counts as resolved; only a reviewed document version that incorporates the fix does.

## The wildcard seat and the academic-paper-reviewer skill

The wildcard seat (§11 of the process file) is optional, chosen at the checkpoint: a reviewer whose identity is generated fresh each run by the
`academic-paper-reviewer` skill's field-analysis phase, which reads the document
and writes a Reviewer Configuration Card for an angle the frozen seats do not
cover. The card generator is the skill's field-analysis agent: the installed
skill is used if present under `~/.claude/skills/`; otherwise the vendored copy
in `third_party/academic-research-skills/` (CC BY-NC 4.0, by Cheng-I Wu;
attribution and license in the NOTICE there) is used, so the wildcard seat works
out of the box. This repo can also be installed as a Claude Code skill itself:
copy the folder to `~/.claude/skills/review-panel/` (see `SKILL.md`).

## Using it for something other than an NSF HCC proposal

As committed here, the process targets the NSF CISE/IIS HCC core program, because that is what the original project reviews. Two places are venue-specific, and both are edited per project, in git, never inline for one run:

- **§2 of `REVIEW-INSTRUCTIONS.md`** names the target program. Point it at your solicitation, or at a journal/conference if you are reviewing a paper.
- **The shared calibration in §4c** says "This is an NSF GRANT PROPOSAL, not a journal manuscript" and lists NSF merit criteria. For a paper submission, a project keeps its own variant of that paragraph (venue, review criteria, format expectations) and freezes it the same way.

Everything else, the blind panel, the checkpoint, the ledger, the deliverable, works unchanged.

## What the output looks like

Each run produces a folder in `reviewed documents/` containing the original document, a `full-review.docx` (cover with ratings and a prioritized fix list; the full draft annotated inline with each reviewer's comments in that reviewer's color; the five complete reports), and an `archive/` with every machine-readable piece so later questions can be answered without re-running anything.

## Honest limitations

- Ratings are calibrated within this system, not against real NSF panels. Their value is in the trend across runs and in the specific findings, not in the absolute number.
- The panel is only as blind as you keep it. Extra context in a prompt, a steering hint, a peek at the ledger, and the run stops being clean.
- Runs cost real model usage, billed to whoever runs them.
