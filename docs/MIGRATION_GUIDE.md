# SS6 — Repository Migration and Reproducibility Verification

## Project Information

**Research title:** The Impact of Generative AI Tools on Employee Productivity and Work Quality in Knowledge-Based Office Tasks

**Institution:** Narxoz University

**Research team:** Muratbek Ramazan and Tasbolatkyzy Zhanerke

**Status:** SS6 reproducibility infrastructure implemented and tested. The research experiment has not yet been conducted.

## 1. Repository Migration

The original repository contained a HumanEval-based benchmark comparing an LLM API against a regex stub. This approach did not measure employee productivity and was not aligned with the research questions.

The repository was therefore redesigned to support a proposed human-centered crossover experiment comparing professional writing tasks completed with and without Generative AI assistance.

The revised implementation includes:

- A Python data validation and analysis pipeline.
- Reproducible randomized assignment generation.
- Synthetic demonstration data.
- Automated unit tests.
- A documented research protocol and evaluation rubric.
- Pinned Python dependencies and a Docker environment.
- GitHub Actions for automated reproducibility checks.

The previous `config.yaml` and `src/benchmark.py` files were removed and replaced by the new research-oriented implementation.

## 2. GitHub Repository and Pull Request

The SS6 changes were committed and pushed to the `feature/ss6-reproducibility` branch.

**Commit:** `af0df55`

**Pull Request:** [PR #1 — Rebuild SS6 repository for reproducible research](https://github.com/ramazanmuratbek-a11y/genai-productivity-benchmark/pull/1)

**Pull Request status:** Draft, pending final review.

The `main` branch has not yet been updated with these changes.

## 3. Local Python Verification

The project was tested in a local Windows Python environment.

Command:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**Result:** All 7 unit tests passed.

The analysis pipeline was also executed successfully using `data/sample/example_measurements.csv`.

## 4. Docker Reproducibility Verification

Docker Desktop with the WSL 2 Linux backend was installed and used to test the project.

Build command:

```powershell
docker build -t genai-writing-study .
```

**Result:** Docker image built successfully.

Run command:

```powershell
docker run --rm genai-writing-study
```

**Result:** Container executed successfully.

The demonstration processed four complete synthetic participant pairs and returned a mean paired completion-time difference of -3.875 minutes.

**Important:** These measurements are synthetic and demonstrate software functionality only. They are not empirical evidence of improved employee productivity.

## 5. Continuous Integration

GitHub Actions is configured using `.github/workflows/tests.yml`.

The workflow automatically installs the pinned dependencies, runs the unit tests, and executes the synthetic demonstration.

**Verification status:** GitHub Actions checks passed.

## 6. Team Collaboration

Both research team members are listed in the project README.

Muratbek Ramazan is responsible for the research analysis pipeline and reproducibility infrastructure.

Tasbolatkyzy Zhanerke has been added to the GitHub repository as a collaborator. Her independent documentation review and contributions will be recorded through the Git workflow.

Commit authorship must reflect the actual work performed by each contributor.

## 7. Remaining Tasks

Before merging Pull Request #1, the team will complete the documentation review, verify subsequent changes through GitHub Actions, and confirm that the repository accurately represents the experimental methodology.

The real human-participant experiment remains proposed. No real participant results are claimed.

## 8. Conclusion

The SS6 repository has been transformed from a placeholder API benchmark into a reproducible research analysis environment aligned with the project's employee-productivity research questions.

Local testing, GitHub Actions, and Docker execution have all been verified successfully.