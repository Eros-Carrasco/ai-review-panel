# Issue Ledger

Deduplicated panel findings with stable IDs, tracked across runs. One row per unique issue; status updated on every run. Per REVIEW-INSTRUCTIONS §4b, statuses are derived **post-hoc** from clean-run reports (reviewers never see this ledger); `orchestrator-observed` marks items noted by the orchestrator rather than a reviewer.

**Status values:** `open` — unresolved in the latest reviewed version · `partial` — moved but not closed · `resolved` — verified fixed in a reviewed version · `superseded` — dissolved by a pivot/reframing · `wontfix` — team decision (reason in Notes).

| ID | Issue | Severity | First seen | Status | Notes (latest evidence) |
|---|---|---|---|---|---|

## How to update (next runs)

For each new run: (1) derive statuses post-hoc from the clean reports (never feed this ledger to reviewers); (2) mark verified fixes `resolved` with the run id; (3) add new issues with the next F-number; (4) record replication/non-replication in the run's `continuity-map.md`; (5) update the log table in `REVIEW-LOG.md`.
