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
