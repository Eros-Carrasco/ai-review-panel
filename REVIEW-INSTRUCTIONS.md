# NSF Proposal Review Pipeline — Instructions

Run these instructions to get a simulated NSF panel review + revision package for a
proposal document, as a single annotated `.docx`.

**How to use:** drop the document in `document to review/`, open a chat in this
directory, pick a model with `/model`, then say "run REVIEW-INSTRUCTIONS.md".

Everything below is editable. Change it and the next run picks up the changes.

## Folder layout

```
document to review/    ← drop zone: put the version to review here (input)
reviewed documents/    ← one folder per run: reviewed doc + its review + archive
log/                   ← REVIEW-LOG.md (run dashboard) + ISSUES.md (issue ledger)
template/              ← the team's formatting reference (colleague's example)
```

## 1. Input

The document in `document to review/` — if several, the most recently modified
`.pdf` or `.docx`; if empty, say so and stop. Prefer `.docx` when both exist
(cleaner paragraph anchoring than PDF extraction).

Record the exact filename + last-modified date of the version reviewed in every
output header — drafts circulate in multiple versions.

## 2. Target program and maturity

- **Solicitation:** NSF CISE/IIS **Human-Centered Computing (HCC) core program**
  (https://www.nsf.gov/funding/opportunities/hcc-human-centered-computing).
  The panel evaluates responsiveness to HCC — do not guess the program.
- **Maturity: `draft` (default).** All runs are draft mode until the user says
  otherwise. In draft mode, focus on framing, structure, and scientific substance;
  report TODO notes, polish, and formatting as a pre-submission checklist — they must
  not dominate the verdict. In `final` mode, full completeness review, everything
  counts.

## 3. Pre-run checkpoint (green flag)

Before running anything, state: the input file picked (+ date), the panel
configuration, the maturity mode, and which pipeline stages will run — then **wait
for the user's OK**. The user may omit stages for that run (e.g., "solo review",
"omite revision"); by default all stages run.

For FOCUSED runs, the checkpoint must additionally list the focus areas **and**
name explicitly any area that was in focus in the previous run but is being
dropped from this one. Silent scope narrowing between runs is prohibited — a
dropped area must be visibly called out and approved. (Added 2026-08-17 after the
intro was dropped from a run's focus without the user noticing.)

## 4. The pipeline (default: all stages, in order)

1. **Panel review** — six frozen + one wildcard independent reviewer agents, dispatched directly with the frozen §4c prompts
   (see §6 legend). The seat design descends from the `academic-paper-reviewer`
   skill's five-seat panel, first run on this team by Keru; the identities were
   adapted to NSF and frozen in §4c so runs stay comparable. The skill itself is
   invoked only for the wildcard seat (§11).
2. **Editorial synthesis** — panel summary with a funding recommendation, consensus
   vs. disagreements (recorded, never averaged away), prioritized fixes, and a
   Devil's-Advocate adjudication. Every substantive claim cites a page/section.
3. **Revision plan** — non-interactive adaptation of `ars-plan`: a section-by-section
   outline of what the *revised* proposal should contain, gaps per section, and an
   evidence map. (For a true Socratic planning dialogue, the user runs `/ars-plan`
   interactively — not part of this pipeline.)
4. **Revision draft** — in the spirit of `ars-revision`: a rewritten proposal draft
   plus a Response-to-Reviewers list (comment → action → where). Rules:
   - Written as *new* content in the output file — the original document is never
     touched.
   - New/changed text is visually marked (blue); unchanged text stays black.
   - Where the revision must make a decision that belongs to the team (an
     architecture choice, a latency target, a named course or partner), it makes a
     concrete proposal AND flags it inline as `[TEAM: …]`. The revised draft is
     starting material, not submission-ready text.

Cross-stage rules:

- Suggested references must be real, verifiable publications (authors, venue, year).
  No invented citations.
- No invented institution facts. The team is the Future Reality Lab at **NYU**.
  Institution-specific suggestions must be verifiably true of NYU or phrased as
  `[TEAM: …]` placeholders.
- Do not detour into `academic-pipeline` or `deep-research`.

## 4b. Review purity — two strictly separated layers

**Layer 1 — the review (pure).** Reviewer agents receive ONLY:
(a) the document under review, and (b) the standing base calibration in this file
(draft/final mode, the HCC target, NSF criteria, format, independence, English).
They receive **nothing else**: no issue ledger, no prior-run findings, no summaries
of team/assistant deliberations, no pointers to specific passages or inconsistencies,
no steering of any kind. Seats are blind to each other AND blind to history. The
annotated document and the panel report contain only what this clean panel produced.

**Layer 2 — continuity (post-hoc, logs only).** AFTER the clean reports are written,
the orchestrator — not the reviewers — maps their findings against `log/ISSUES.md`:
which ledger issues a clean finding matches (resolved / remaining / re-emerged),
and which findings are new. This comparison lives in `log/ISSUES.md`,
`log/REVIEW-LOG.md`, and the run archive (`continuity-map.md`). It is never fed
forward into any reviewer brief, and a finding that appears in both a prior run and
the clean run may be called replicated — but nothing seeded can ever be counted as
independent corroboration, because nothing is seeded.

**Layer 3 — advisory sessions (separate mode).** Panel deliberations on accumulated
direction (hypothesis rounds, design-space discussions, etc.) are a distinct,
explicitly-labeled advisory mode run on request. Their outputs live in logs/archive,
never inside a review document, and never in a review brief.

## 4c. Frozen reviewer prompts (use VERBATIM — no per-run authoring)

The orchestrator MUST dispatch the five reviewers using exactly the texts below. The
only variable is the extracted-text file path. Do not add, remove, or rephrase
anything; do not describe the document's structure, history, or contents; do not read
`log/` before dispatching. If these prompts seem to need improvement, propose the
change to the user for approval in a future edit of this file — never adapt them
inline for a run.

**Shared calibration (identical for all five seats):**

> Read the WHOLE extracted text at: `<PATH>` (page markers `=== PAGE N ===`). It is a
> working draft of an NSF grant proposal. Judge what is on the page.
> This is an NSF GRANT PROPOSAL, not a journal manuscript. Evaluate against NSF merit
> review criteria — (1) Intellectual Merit, (2) Broader Impacts — plus: significance
> and clarity of the research question; soundness and feasibility of the work plan,
> methodology, and timeline; qualifications/resources as evidenced in the document;
> responsiveness to the target program: the NSF CISE/IIS Human-Centered Computing
> (HCC) core program.
> DRAFT MODE: focus on framing, structure, and scientific substance. Internal notes,
> TODOs, typos, and formatting get one brief pre-submission-checklist mention — they
> must not dominate severity or the verdict.
> You review independently; you see no other reviewer's comments. Every substantive
> claim cites a page. Genuine strengths acknowledged; no manufactured balance. Every
> weakness: what's wrong, where, and a concrete fix. Define each technical term at
> first use for a reader newer to experimental methods. READ-ONLY on all files.
> English. Your final message IS the report — raw markdown, no preamble, ~600-900
> words.
> FORMAT: `## <SEAT> — <Name>` — where `<Name>` is the seat's role title (e.g.
> "Methodology & Evaluation"), never an invented persona name. / **Persona:**
> (1 line) / **NSF Summary Rating:**
> Excellent–Poor (may hyphenate) / `### Overall verdict` (short paragraph) /
> `### Strengths` (bullets, page cites) / `### Weaknesses` (numbered; severity
> CRITICAL/MAJOR/MINOR; page; fix) / `### Pre-submission checklist` (brief bullets) /
> `### Bottom line` (2-3 sentences).

**Seat lenses (append the matching one to the shared calibration):**

> **PF — Program Fit, Completeness & Overall Merit.** Senior HCI professor; veteran
> NSF CISE/IIS panelist. Lens: responsiveness to the HCC program's scope; clarity and
> significance of the central research question; Intellectual Merit framing;
> completeness against PAPPG project-description expectations (team qualifications,
> results from prior NSF support, facilities, data management, timeline);
> competitiveness versus typical funded HCC proposals.

> **R1 — Methodology & Evaluation.** Quantitative HCI researcher: controlled
> human-subjects experiments, experimental design, statistical power, unit-of-analysis
> questions, validated instruments, preregistration. Lens: testability of the stated
> hypotheses; validity of the proposed measures for the claimed constructs; the
> comparison structure and its confounds (a confound = a second difference between
> conditions that could explain a result); statistical adequacy; the human-subjects
> plan; whether the work plan can deliver the studies in the stated timeline.

> **R2 — Domain, Related Work & Novelty.** CSCW / mixed-reality collaboration
> researcher. Lens: novelty of the claimed contribution relative to the state of the
> art; currency and adequacy of the related work; whether gap claims are supported;
> the standard citation-integrity audit (do in-text keys resolve to reference entries
> and vice versa; are cited claims plausibly attributed); whether the chosen study
> tasks are well-motivated against the literature.

> **R3 — AI Systems & Broader Impacts.** Applied AI/ML systems researcher who chairs
> Broader Impacts assessments. Lens: credibility, specificity, and feasibility of the
> AI components the document relies on; the Broader Impacts section against NSF
> expectations (named mechanisms, measurable outcomes, broadening participation,
> accessibility); privacy and ethics of the proposed sensing, including where data is
> processed and stored.

> **R4 — Devil's Advocate.** The skeptical panelist who builds the strongest case
> against funding — rigorous, not cruel; where the proposal survives the attack, say
> so. Lens: unstated assumptions and logical gaps; rival explanations; scope versus
> resources; ignored alternatives; stakeholder blind spots; the "so what?" test.
> FORMAT (replaces the default sections): `### Strongest counter-argument` (200-300
> words) / `### Issue list` (numbered; severity; dimension [logic/evidence/
> feasibility/scope/stakeholders]; page; challenge; what would rebut it) /
> `### Ignored alternatives` / `### Missing stakeholder perspectives` /
> `### Observations (non-defects)`. ~700-1000 words.

> **R5 — XR Systems Engineering.** Senior XR/AR systems engineer who has shipped
> tracking and telepresence systems. Lens: feasibility of the sensing and rendering
> pipeline as described on the page: cross-device registration and calibration
> (webcam-to-glasses), tracking accuracy and drift, end-to-end latency budgets,
> device capabilities and risk (field of view, anchoring, hand tracking, shipping
> status), network synchronization under realistic conditions, failure modes and
> fallbacks; whether the engineering plan, team, and timeline can deliver the
> platform the studies require.


## 5. Output — one run folder per review

Timestamp from `date "+%Y-%m-%d-%H%M"`. Create:

```
reviewed documents/<YYYY-MM-DD-HHMM> — <document name without extension>/
├─ <original document>                (MOVED here from "document to review/")
├─ <YYYY-MM-DD-HHMM>-full-review.docx (the human deliverable)
└─ archive/                           (machine-readable sources, for Q&A/re-review)
   ├─ README.md                       (index of the archive + run parameters)
   ├─ proposal-text-as-reviewed.txt   (extracted text with === PAGE N === markers)
   ├─ panel-reports.md                (the 5 reviews, verbatim)
   ├─ synthesis.md                    (verdict, adjudication, fixes, references)
   ├─ plan.md                         (Part 3 source)
   ├─ revision.md                     (Part 4 source, with {{...}} and [TEAM: ...])
   └─ revision-brief.md               (brief given to the revision stage)
```

Then update `log/REVIEW-LOG.md` (new row + run note) and `log/ISSUES.md`
(status pass per §8). **Never overwrite existing outputs. All output in English.**

Structure of the `full-review.docx` (single document, clean heading hierarchy so
the Google Docs outline panel works):

- **PART 0 — COVER** (team standard, matching `template/`): gray banner "AI panel
  review — not part of the proposal; delete colored lines before submission";
  **color legend with each reviewer's name rendered in its own color** (one run per
  reviewer — never all-gray); NSF PANEL SNAPSHOT (per-reviewer ratings + consensus
  funding recommendation + source version + mode); TOP MUST-FIX list. Plain
  readable text throughout — no fancy fonts.
- **PART 1 — ANNOTATED PROPOSAL** (the primary artifact): full original text in
  order, with colored reviewer comments inserted inline immediately after the
  passage they refer to, plus blue `■ FIX:` suggestions. Panel splits are labeled
  as such in the comment.
- **PART 2 — FULL PANEL REPORT**: the five complete individual reviews (each under
  a heading in its reviewer color), synthesis, disagreements, prioritized fixes,
  suggested references. Concise: no metadata table repeating Part 0 — one line
  naming the panel seats is enough. From the second run on, include the
  resolved / remaining / new comparison.
- **PART 3 — REVISION PLAN** (stage 3 output).
- **PART 4 — REVISED DRAFT** (stage 4 output): revised text with changes in blue +
  `[TEAM: …]` flags, then the Response-to-Reviewers list.

Since everything lives in one document, omit anything that would be repeated
verbatim across parts — say it once in the earliest part it belongs to.

Implementation note: generate the `.docx` by writing minimal OOXML directly (zip:
`[Content_Types].xml`, `_rels/.rels`, `word/document.xml`) — no pandoc/installs.
Must open in Word and import to Google Docs with colors intact.

## 6. Color legend (keep stable across runs)

| ID | Color | Role |
|---|---|---|
| `PF` | dark gold `806000` | Program Fit (vs. HCC), Completeness & Overall Merit |
| `R1` | red `C00000` | Methodology & Evaluation |
| `R2` | green `2E7D32` | Domain, Related Work & Novelty |
| `R3` | orange `C55A11` | AI Systems & Broader Impacts |
| `R4` | teal `0B6E6E` | Devil's Advocate |
| `FIX` | blue `1F4E79` | Revision suggestions, revised text, suggested references |
| `R5` | purple `6A1B9A` | XR Systems Engineering |
| `W` | brown `5D4037` | Wildcard seat — dynamic persona per run (§11); rating listed separately |
| — | gray `808080` | Banner/legend scaffolding |

Original text stays black; the author's own pre-existing notes are unchanged.
Comment format: `■ <ID> · <Role> | <CRITICAL/MAJOR/MINOR>:` bold, then the comment
in the same color.

## 7. Q&A mode (ask anything, full context)

The user can ask questions about any run or across runs without triggering a new
review — e.g., "why did R1 reject the power analysis?", "which issues are still
open since v1?", "what changed between the v1 and v2 documents?".

- Load context from the relevant run folder's `archive/` (+ `log/ISSUES.md`);
  answer citing run, section, and page.
- If the question is addressed to a specific seat ("ask R1 …"), answer from that
  reviewer's persona using their archived report as context.
- Version comparisons diff the `proposal-text-as-reviewed.txt` files across runs.
- Q&A never modifies outputs or the ledger.

## 8. Logs (`log/`)

- **`REVIEW-LOG.md`** — dashboard: one row per run (ratings, recommendation,
  deduplicated C/M counts, Res/Rem/New, run folder) + a short run note.
- **`ISSUES.md`** — the deduplicated issue ledger with stable IDs (F01, F02, …).
  On each run: mark issues verified-fixed in the newly reviewed version as
  `resolved`, add new issues with the next F-number, leave the rest `open`.
  "Fix drafted" in Part 4 does NOT count as resolved — only a reviewed document
  version that incorporates the fix does. Res/Rem/New in the log derives from
  this ledger.

## 9. FOCUSED review (opt-in variant — user must request it by name)

A lighter, steered alternative to the clean pipeline, for early drafts where the
team wants directional feedback on specific parts ("what's good here — expand
from there") rather than a full formal verdict. First used: run 2026-08-07-0232.

**When to use:** draft/skeleton stage; the team names the areas they care about;
speed and signal matter more than review purity. When in doubt, run the clean
pipeline — a focused run can never replace a clean one before submission.

**How it differs from the default pipeline:**

1. **Steered brief.** The frozen §4c prompts are used as the base, plus ONE
   "FOCUSED RUN ADDENDUM" inserted after the DRAFT MODE line, identical for all
   seats, containing only: (a) the user-named focus areas, (b) a strengths-first
   instruction ("identify what is genuinely solid and how to expand it, then only
   the few weaknesses that matter at this stage"), (c) a compact word target
   (~450-700; R4 ~500-800). R4 keeps its adversarial format but adds a
   "What survives the attack" section. Nothing else may be added — no document
   history, no ledger content, no passage pointers beyond the user's named areas.
2. **Stages 1-2 only** by default (panel + synthesis; no revision plan/draft),
   unless the user asks otherwise.
3. **Deliverable:** the usual annotated .docx, simplified — Part 0 cover (with a
   gray "FOCUSED RUN" disclosure line), Part 1 annotated proposal with the
   reviewers' VERBATIM comments inline (strengths marked `STRENGTH`; no
   paraphrasing, no separate `■ FIX:` lines), Part 2 full reports + synthesis.
   The synthesis leads with "What the panel likes — build from here."
4. **Contamination rule (the price of steering):** everything a focused panel
   produces is advisory. In `ISSUES.md` and `continuity-map.md`, matches are
   recorded as "re-raised (steered)" and NEVER count as independent
   corroboration or replication; ratings are not comparable to clean runs and
   the log row must say so. Only orchestrator-level text-diff facts (e.g., "this
   version removed X, resolving F-nn") carry evidential weight from a focused
   run. Reviewers still never see the ledger or any prior-run material — the
   steering is limited to the user's focus areas, nothing historical.
5. **Run folder naming:** append ` — FOCUSED` to the folder name; archive
   README states the focus areas and the addendum used.

## 10. GAP-FILL session (generative advisory — user must request it by name)

A **generative working session, not a review.** The panel reads the current draft plus
the team's to-do list and comments, and each seat *writes the text it would put in* to
fill the gaps in its lane. First used: session 2026-08-15. Falls entirely under §4b
Layer 3 (advisory): fully steered, no ratings, produces no review evidence, never
touches `ISSUES.md`; one note in `REVIEW-LOG.md`.

1. **Input:** the document in `document to review/` (draft + to-do list; embedded
   comments are extracted and included).
2. **Stage 1 — four writer seats, one lane each** (avoids duplicate drafts):
   PF → intro/IM framing, PAPPG skeleton, timeline; R1 → statistics (power, dyadic
   analysis, preregistration), mechanism measures; R2 → related work, reference list,
   gap statement, task motivation; R3 → Broader Impacts, privacy paragraph, AI
   evidence plan. Writers work independently and in parallel.
3. **Stage 2 — R4 stress-test:** every drafted passage gets SURVIVES / SURVIVES WITH
   FIX / WEAK plus a one-line reason.
4. **Hard rules:** real, verifiable citations only; no invented lab/NYU facts — any
   team-specific content becomes a `[TEAM: …]` placeholder; all output labeled
   *starting material, not submission-ready*; English.
5. **Deliverable:** one .docx organized by to-do topic — gap → drafted text (in the
   writer seat's §6 color) → R4 verdict → `[TEAM]` flags — plus `archive/` with the
   verbatim seat outputs. Lives in `gap-fill sessions/<timestamp> — <doc name>/`,
   separate from `reviewed documents/` (these sessions are personal working material,
   not team review runs).

## 11. Wildcard seat (W) — dynamic persona via the academic-paper-reviewer skill

On every run, one additional reviewer whose identity is
generated fresh for the current document, using the `academic-paper-reviewer`
skill's Phase 0 (field analysis): an analyst agent reads the document and writes
a Reviewer Configuration Card (specific identity, three review focuses tailored
to this document, declared blind spots), deliberately choosing an angle the
frozen seats do not cover.

Rules:

- The card is presented in the pre-run checkpoint (§3) together with the rest of
  the run parameters; the user may adjust or veto it before the run.
- W receives the §4c shared calibration verbatim plus its card as the seat lens —
  never a frozen lens, never another seat's report, never the ledger.
- W's rating is listed separately from the NSF panel snapshot and never enters
  cross-run comparisons. W's findings enter `ISSUES.md` tagged `wildcard`:
  replication or non-replication across runs is meaningless for this seat,
  because the lens changes every time.
- The card is archived as `wildcard-card.md` in the run's archive.
- The wildcard card is generated by the `academic-paper-reviewer` skill's
  field-analysis agent: the installed skill (`~/.claude/skills/`) if present,
  otherwise the vendored copy at
  `third_party/academic-research-skills/field_analyst_agent.md` (CC BY-NC 4.0,
  attribution in the NOTICE there). If neither is available, the run proceeds
  with the frozen seats only, and the checkpoint says so.

