# Task 4 / SS11 — IEEE four-page research-paper draft

**Research title:** The Impact of Generative AI Tools on Employee Productivity and Work Quality in Knowledge-Based Office Tasks
**Authors:** Muratbek Ramazan and Tasbolatkyzy Zhanerke, Narxoz University

## Research status (important)

This paper presents a **proposed randomized, counterbalanced human writing study** and **synthetic verification data**, not a completed experiment with employees. The writing example has four fictional participant pairs (eight task records, minutes). A **separate** technical stream has five warm-ups and 100 measured Python validation-and-analysis executions (milliseconds). The 100 software runs do not measure AI response time, employee productivity, or 100 real participants. No causal inference is justified from the demonstration data.

## Files

| File | Purpose |
|---|---|
| `main.tex` | IEEEtran preamble, 150–250-word abstract, section inputs, bibliography |
| `sections/01_introduction.tex` | Research context, gap, questions, 12 scholarly citations |
| `sections/02_methodology.tex` | Proposed crossover, metrics, TikZ protocol diagram, design table |
| `sections/03_demonstration_results.tex` | Fictional writing-task analysis, separate software benchmark, illustration and tables |
| `sections/04_discussion.tex` | Interpretation, internal/external/construct validity limits |
| `sections/05_conclusion.tex` | Methodological contribution, answers to RQs, future real study |
| `references.bib` | Twelve Zotero-derived, cleaned journal/conference citations |
| `fig1_latency_vs_load.pdf` | Existing vector plot of **synthetic human writing time**; name is historical, not software latency |

## Open in Overleaf

This directory mirrors the author's working Overleaf project at the time of the Task 4 / SS11 update. To update an **existing** Overleaf project, upload or replace the files from this directory while keeping the `sections/` structure. Set `main.tex` as the main document and use the **pdfLaTeX** compiler; the template uses IEEEtran and BibTeX (`references.bib`). Recompile twice if citations need a second pass. **Do not replace `main.tex` with a section file**.

The user-verified Overleaf export was **four pages with 12 references and Fig. 2**. LaTeX page counts can differ across TeX distributions, so inspect the compiled PDF after importing.

## GitHub test commands

From repository root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe src\generate_ss9_report.py --check
```

`tests/test_ss10_overleaf.py` remains backward-compatible with the wording and cross-references of this revised paper. `tests/test_task4_ss11_paper.py` checks manuscript structure, abstract word range, citation/label integrity, figure presence, and honest synthetic-data provenance. **Tests do not verify visual page count or PDF typography**; check the Overleaf preview and exported PDF separately.

## Citation hygiene and ethics

* Use relevant `\cite{key}` commands in the text; 12 entries are currently cited.
* Preserve identifiers in `references.bib` when editing Zotero exports.
* Do not upload private Zotero attachments, copyrighted full-text PDFs, or identifiable participant data.
* This IEEE-style layout is for the course draft, not evidence of submission to a conference.
* If results are later collected from real participants, re-run the analysis and revise every empirical claim.

## Verification summary

The exact `.tex`, `.bib`, and figure source files were taken from the supplied Overleaf ZIP. The README and Python source-integrity tests were updated for Task 4 / SS11. The independently supplied four-page PDF was visually reviewed in the earlier audit. Current test execution evidence should be recorded in GitHub CI after creating the pull request.
