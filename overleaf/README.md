# SS10 — IEEE Overleaf manuscript

**Research status:** Proposed human writing study. All quantitative results displayed in the manuscript are **synthetic demonstrations**, not empirical findings.

## Import to Overleaf
1. Create a new **Blank Project** at https://www.overleaf.com/.
2. Upload the **contents** of this folder (or upload the standalone `SS10_Overleaf_Project.zip` as a new project).
3. Set `main.tex` as the main document and compiler **pdfLaTeX**.
4. Recompile (Overleaf handles the BibTeX bibliography automatically). Verify all `\cite` and `\ref` markers resolve.

## Project structure
- `main.tex`: `IEEEtran` conference template, abstract, packages and IMRaD entrypoint.
- `sections/01_introduction.tex`: five-step academic funnel, RQ and contributions.
- `sections/02_methodology.tex`: counterbalanced crossover, paired estimator, quality/factual guardrails, TikZ pipeline and parameter table.
- `sections/03_demonstration_results.tex`: **fictional** writing sample and separate software-timing example.
- `sections/04_discussion.tex`: limitations and future empirical study.
- `references.bib`: sanitized subset of the team's existing Zotero bibliography (four cited references).

## Zotero / Better BibTeX workflow
Export selected items via Zotero > Export Items > Better BibTeX (`.bib`) and preserve stable citation keys. Replace `references.bib` only after verifying the exported keys match each `\cite{key}`. Remove `file`, `abstract`, `urldate`, and other private or extraneous fields as appropriate; retain author, title, venue, year, page range and DOI. Exporting does not grant permission to redistribute full article PDFs.

IEEE uses numeric `\cite{key}` with the `IEEEtran` style. `\citep` and `\citeauthor` are natbib-based commands and are not portable defaults in this IEEE setup; do not add them without configuring a compatible package and style.

## Compile locally
Run from the `overleaf/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Academic integrity checklist
- Do not label synthetic records as actual recruits or make productivity causal claims.
- Never mix human elapsed time (minutes) with Python execution time (milliseconds).
- Verify actual AI model, trial recruitment, task-set pilot, ethics and sample-size decisions before empirical execution.
- Keep `\label` / `\ref` for figures, sections and equations rather than typing hardcoded numbers.
- Use LaTeX directional quotation marks ``example'' rather than straight literal quotes in prose.
- Use `word~\cite{key}` for stable spacing in citations.
- Inspect compiler log for undefined citations/references and overfull/underfull boxes.
- Avoid committing local Zotero file paths, proprietary PDFs or real participants' data.

## Notes on source provenance
Content is based on the team's existing Task 2 study protocol, Task 3 synthetic summaries and SS7–SS9 technical pipeline. The LaTeX paper does not replace `reports/paper_section_4.md`; it formats a consistent manuscript for the SS10 Overleaf exercise. The IEEE/ACM venue has **not** been selected for actual submission; IEEE is the classroom default here.
