# SS10 — IMRaD, Overleaf, BibTeX, Introduction and Methodology

**Lab focus:** Overleaf initialization, IEEE/ACM project setup, sanitized Zotero `.bib` import, five-step Introduction, reproducible Methodology, formulas, pipeline diagram, and cross-reference audit.

**Selected default:** IEEE conference layout (`\documentclass[conference]{IEEEtran}`); this is a studio-format choice, not a claim of conference submission.

## What is IMRaD?
Introduction motivates the problem and articulates research questions; Methods specify a reproducible protocol; Results state measured or (here) clearly synthetic outcomes; Discussion interprets evidence and limitations. A successful scientific argument connects these parts without conflating demonstration output with empirical observations.

## Mapping of lab deliverables
| SS10 requirement | File |
|---|---|
| Main IEEE template and essential packages | `overleaf/main.tex` |
| Five-step Introduction funnel and citations | `overleaf/sections/01_introduction.tex` |
| Randomized counterbalanced crossover and estimator | `overleaf/sections/02_methodology.tex` |
| Equation labels and figure/parameter-table cross-references | `overleaf/sections/02_methodology.tex` |
| Zotero `.bib`, cleaned metadata and stable citation keys | `overleaf/references.bib` |
| Complete IMRaD skeleton incl. explicitly synthetic Results | `overleaf/sections/03_demonstration_results.tex`, `04_discussion.tex` |
| Project import and typesetting audit | `overleaf/README.md` |

## IEEE vs ACM
IEEE conference layouts use `\documentclass[conference]{IEEEtran}` and numeric citations by default; ACM uses `\documentclass[sigconf]{acmart}` and ACM-specific rights/metadata. Switching requires adapting the template preamble, author blocks, citation style, and publication metadata. Simply swapping the documentclass line is **not** sufficient to produce a valid ACM submission.

## Bibliography and citation syntax
In IEEE source, `\cite{noyExperimentalEvidenceProductivity2023}` is a numeric reference with `\bibliographystyle{IEEEtran}`. For `\citep` / `\citeauthor`, first configure a natbib-compatible style; do not assume these exist in default IEEEtran. `\bibliography{references}` loads the sanitized Zotero-derived `references.bib` file. Citation keys must exactly match.

## Audit
The project is self-contained. The input sections have `\label` and are referenced. The TikZ pipeline figure and the design table have explicit labels; mathematical expressions have equation labels and citations use `~\cite` nonbreaking spaces. All recorded measurements remain clearly labeled synthetic. A built-in Python structure test checks keys, labels, privacy, and provenance. The accompanying preview PDF should compile with pdfLaTeX/BibTeX; on Overleaf recompile to regenerate cross-references.

## Reproducibility status
No real participant data exist. `SS10` is typesetting and academic communication, **not** a newly completed clinical/behavioral study. The public GitHub `main` now includes merged SS5-SS10 artifacts and their automated checks. Source figures from previous tasks remain unaffected.
