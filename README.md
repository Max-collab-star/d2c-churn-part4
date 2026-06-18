# Part 4: D2C Customer Churn Intelligence - Production Modeling & Leakage Remediation

## Project Overview
This repository contains the final production-grade machine learning classification pipeline for the D2C Personal-Care Brand Customer Churn project. The objective of this final phase is to implement a strict temporal cutoff data framework, remediate the data leakage found in the baseline model, engineer robust untainted historical features, and deploy an optimized, highly generalizable Random Forest Classifier.

## Project Structure
The repository is structured with the following core deliverables:
* `production_modeling.ipynb`: Jupyter notebook containing the leakage-remediated feature pipeline, regularized Random Forest model training, and generalization tests.
* `production_model_report.md`: Formal technical report detailing the final model execution metrics ($ACC \approx 76.88\%$, $AUC \approx 0.8443$), overfitting validation, and feature importance hierarchies.
* `requirements.txt`: Standard list of locked environment dependencies required to execute the pipeline.

## Setup & Running Instructions
To execute the production modeling pipeline locally, ensure you are utilizing a Python 3.x environment and follow these steps:

1. Download or clone this public repository.
2. Place your source `customers.csv`, `orders.csv`, `support_tickets.csv`, and `churn_labels.csv` files directly into the root directory.
3. Install the required environment libraries using the terminal command:
   ```bash
   pip install -r requirements.txt
4.Launch and run the production notebook:
  jupyter notebook production_modeling.ipynb
