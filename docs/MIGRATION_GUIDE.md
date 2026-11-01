# Update guide for the existing GitHub repository (Windows)

These files **replace old HumanEval/regex stub code**. They have not been
pushed to GitHub by ChatGPT: the connected GitHub integration rejected write
access. Save the ZIP locally and follow the steps below using your GitHub account.

## Step 1 — Clone and create a new branch

Open PowerShell (Git for Windows installed):

```powershell
git clone https://github.com/ramazanmuratbek-a11y/genai-productivity-benchmark.git
cd genai-productivity-benchmark
git checkout -b feature/ss6-reproducibility
```

## Step 2 — Copy the revised ZIP files

Extract the supplied ZIP to a temporary folder. Copy its **contents** into the
cloned repository directory, replacing README.md, Dockerfile, requirements.txt,
and .gitignore. Keep the repository's existing MIT `LICENSE` file and `.git/`
directory untouched. Do not copy files from `outputs/` or `__pycache__/`.

Remove these **two obsolete tracked files only**, which are replaced by
`configs/experiment.yaml` and `src/analyze.py`:

```powershell
git rm config.yaml src/benchmark.py
```

## Step 3 — Review and test (Python 3.11 recommended)

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python src/analyze.py
```

The report is a **synthetic data demonstration**, not findings about employees.
If Docker Desktop is available:

```powershell
docker build -t genai-writing-study .
docker run --rm genai-writing-study
```

The Docker build/run still needs to be tested on your computer.

## Step 4 — Commit your actual work and open a Pull Request

```powershell
git status
git add -A
git commit -m "Rebuild SS6 repository for writing-task reproducibility"
git push -u origin feature/ss6-reproducibility
```

On GitHub, choose **Compare & pull request**, target `main` and review the
change. Later, invite the second author through Settings → Collaborators and
have them genuinely contribute or review in their own account. Do not alter
commits to pretend they were written by another person.
