# Project folder layout

A review-panel project is a folder that looks like this:

```
my-project/
├─ REVIEW-INSTRUCTIONS.md     the process file, copied from this repo
├─ document to review/        drop exactly one draft here before a run (.docx or .pdf)
├─ reviewed documents/        one folder per run, created automatically:
│  └─ 2026-09-02-1229 — My Document/
│     ├─ My Document.pdf              the reviewed file, moved here
│     ├─ 2026-09-02-1229-full-review.docx   the human deliverable
│     └─ archive/                     everything machine-readable:
│        ├─ README.md                 run parameters
│        ├─ proposal-text-as-reviewed.txt
│        ├─ pages/ or figures/        what the reviewers saw
│        ├─ report-PF.md … report-R4.md
│        ├─ synthesis.md
│        ├─ continuity-map.md
│        └─ annotations.json
└─ log/
   ├─ REVIEW-LOG.md           one row per run, newest first
   └─ ISSUES.md               the issue ledger: one row per unique finding, stable IDs
```

Conventions:

- Run folders are named `YYYY-MM-DD-HHMM — <document name>` and are never overwritten.
- The document is **moved** from `document to review/` into the run folder, so the review folder always reflects exactly what was reviewed.
- All output is in English.
