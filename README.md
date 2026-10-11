# The Impact of Generative AI Tools on Employee Productivity

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Status: Active](https://img.shields.io/badge/Status-Active-success.svg)
![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)

**Authors:** Tasbolatkyzy Zhanerke, Muratbek Ramazan

## 📖 Project Overview
This repository contains the codebase and reproducibility package for the research project evaluating the empirical impact of Generative AI (LLMs) on knowledge worker productivity. 

* **Research Question:** Does the utilization of Generative AI significantly increase objective productivity metrics (latency) and subjective output quality (accuracy) in cognitive and programming tasks?
* **Hypothesis ($H_1$):** The integration of Generative AI significantly decreases task completion time (latency) and improves the quality of the final output (Pass@1 accuracy) compared to traditional legacy algorithmic baselines.

## 📂 Repository Structure
```text
genai-productivity-benchmark/
├── data/
│   └── sample/          # Sample dataset for pipeline testing (e.g., HumanEval subset)
├── src/                 # Source code for benchmarking
│   ├── benchmark.py     # Main execution script (GenAI vs Legacy baseline)
│   └── metrics.py       # Evaluation logic for Latency and Accuracy calculation
├── notebooks/           # Jupyter notebooks for data analysis & visualization
├── config.yaml          # Experiment configurations (hyperparameters, paths)
├── Dockerfile           # Docker configuration for 100% environment isolation
├── requirements.txt     # Python dependencies 
├── README.md            # This documentation
└── LICENSE              # Open Science MIT License



⚙️ System Requirements
OS: Linux (Ubuntu 20.04/22.04), macOS, or Windows (via WSL2).

Environment: Docker OR Python 3.11 with virtual environment (venv).

Dependencies: datasets, pyarrow, openai (see requirements.txt).

API Keys: An active OpenAI API key is required to run the experimental LLM group.

🚀 Quickstart & Reproducibility Guide
You can fully reproduce our benchmarking experiment in just 3 commands using Docker:

1. Clone the repository:
git clone [https://github.com/ramazanmuratbek-a11y/genai-productivity-benchmark.git](https://github.com/ramazanmuratbek-a11y/genai-productivity-benchmark.git)
cd genai-productivity-benchmark

2. Configure environment:
Update the config.yaml file with your OpenAI API key and desired parameters.

3. Build and Run the Benchmark (Docker):
docker build -t genai-benchmark .
docker run genai-benchmark python src/benchmark.py --config config.yaml

## 📊 Expected Results / Benchmark Table
Running the `benchmark.py` script on the test dataset will generate a comparative analysis log. The expected baseline structure is:

| Method (Agent) | Latency (p50) | Accuracy (Pass@1) | Throughput (tasks/min) | API Cost ($) |
| :--- | :---: | :---: | :---: | :---: |
| **Legacy Script (Baseline)** | 0.05s | ~5.0% | 1200 | $0.00 |
| **GenAI (GPT-4)** | 2.50s | ~85.0% | 24 | ~$0.02 |

*(Note: The AI method is expected to have higher latency per individual task due to network API calls, but drastically higher accuracy/pass rate, reflecting the true productivity gain in solving complex cognitive tasks without human intervention).*


📄 License & Citation
This project is licensed under the MIT License - see the LICENSE file for details.

@misc{muratbek2026genai,
  author = {Tasbolatkyzy, Zhanerke and Muratbek, Ramazan},
  title = {The Impact of Generative AI Tools on Employee Productivity Benchmark},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/ramazanmuratbek-a11y/genai-productivity-benchmark}}
}
