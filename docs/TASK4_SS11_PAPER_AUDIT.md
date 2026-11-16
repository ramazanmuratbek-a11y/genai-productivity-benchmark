# Task 4 / SS11 — Research-paper completion and submission audit

**Scope:** This update synchronizes the author's currently compiled Overleaf manuscript with `overleaf/` in the GitHub repository. It adds conclusion, citations and the existing study diagram / writing-time plot while preserving the earlier SS5–SS10 Python research pipeline.

## Course deliverables

- **Task 4:** Exactly four IEEE-style pages (as verified in the user's Overleaf export), English abstract ~193 words, Introduction, Methodology, Synthetic Demonstration Results, Discussion & Limitations, Conclusion & Future Work.
- **SS11:** Discuss limitations; add explicit conclusion/future work; validate cross-references, bibliography and manuscript structure.
- **Bibliography:** Twelve cited Zotero-derived journal and conference works. Some are software engineering or workplace AI literature used as background rather than directly comparable writing experiments.
- **Figures/tables:** IEEE TikZ workflow `fig:pipeline` (Fig. 1), synthetic writing-condition time plot `fig:writing_time` (Fig. 2), parameter table `tab:design` and separate writing/software summaries `tab:writing` and `tab:software`.
- **Equations:** `eq:pairedtime` (paired time saving, in minutes), `eq:factmetrics` (factual P/R/F1). Their references use standard LaTeX commands.

## Research honesty and limitations

Do not label any synthetic records as recruited employees. The writing time example uses four fictional participant pairs (3.875-minute illustrative mean saving, bootstrap CI [0.00, 6.25], includes zero). Software measurement has 100 timed Python executions in milliseconds, not an AI inference or human-workload experiment. The provisional -5-point quality guardrail has not undergone non-inferiority testing. The paper is a proposal and demonstration, not evidence of AI effectiveness.

## What the automated tests verify

- Five LaTeX sections and the IEEEtran entrypoint.
- 150–250-word abstract.
- Twelve distinct cited BibTeX records and no citation-key mismatches.
- All `\ref`/`\eqref` targets exist and labels are unique.
- Actual vector PDF figure exists and is included.
- Synthetic-provenance and unit disclosures remain present.

## Manual pre-submission checks

1. Overleaf shows **four pages** after `Recompile` and all sections I–V.
2. All 12 references are printed, no `??` or undefined citations; assess scientific relevance, DOIs and bibliography style.
3. Diagram and Fig. 2 are readable at 100%, tables are not clipped.
4. The Abstract has 150–250 words; no claims of real participant effects.
5. Review any underfull/overfull `\hbox` warnings for visible gaps or overflow.
6. Download final PDF from Overleaf and submit only the requested files / GitHub link to Canvas.
7. Check the exact Task 4/SS11 submission rubric and deadline before uploading.

## How to update the repository

Apply the overlay ZIP at repository root in a new branch, run all unit tests, commit only the included paths, push, open a pull request, verify GitHub Actions, and merge. **No repository push or pull request is performed by this update package.**
