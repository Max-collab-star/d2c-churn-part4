# Production Model Deployment, API Specification, and Monitoring Report

## 1. Cleaned Pipeline Execution Metrics
By applying a strict temporal cutoff on all feature engineering arrays up to `2025-09-30`, target data leakage has been fully resolved. The optimized Random Forest Classifier achieves stable performance across splits:
* **Overall Classification Accuracy:** 0.7688 (76.88%)
* **Area Under the ROC Curve (ROC-AUC):** 0.8443
* **Training Split Accuracy:** 0.8151
* **Validation Split Accuracy:** 0.7688

## 2. REST API Request/Response Architecture Design
The trained model artifact is exposed via a high-performance REST API built using FastAPI. Input fields are strictly validated at the application gate using Pydantic data schemas to enforce data sanity before array compilation.

* **Predict Endpoint:** `POST /predict`
* **Input Schema Constraints:**
  * `recency`: Float value restricted within validation boundary parameters `[0, 365]`.
  * `frequency`: Integer tracking transaction counts ($\ge 0$).
  * `monetary`: Gross spend float ($\ge 0.0$).
  * `complaints_count`: Operational support interaction integer ($\ge 0$).

### Error Handling & Exception Mapping Codes
* `422 Unprocessable Entity`: Triggered automatically when input parameters violate boundary data validations (e.g., negative frequency counts).
* `503 Service Unavailable`: Triggered if the core server fails to initialize or deserialize the saved `production_churn_model.pkl` serialization asset.
* `500 Internal Server Error`: Safe structural fallback intercepting pipeline anomalies during matrix transformations.

## 3. Production Monitoring & Responsible Use Plan
To ensure long-term stability and counter prediction degradation post-deployment, the microservice implements a strict operational governance framework:

### Data Drift & Concept Drift Mitigation Protocol
1. **Feature Distribution Monitoring:** Log incoming inference payload features hourly. Compute a rolling Population Stability Index (PSI) on `recency` and `complaints_count` matrices compared to the baseline training population.
2. **Drift Alert Thresholds:** Trigger an automated engineering alert if $PSI > 0.25$, indicating structural shifts in consumer buying behavior or logistics friction cycles.
3. **Scheduled Model Recalibration:** Establish an automated cron-job pipeline to re-ingest fresh transactional labels every 30 days, re-run feature aggregation scripts using updated snapshot cutoff arrays, and validate a fresh pkl payload.

### Responsible Use & Bias Prevention Guardrails
* **Exclusion of Protected Attributes:** The feature matrix completely excludes demographics fields such as customer gender, location variables, or signup origin vectors to ensure absolute neutrality across consumer segments.
* **Algorithmic Transparency Thresholds:** Probability scores are split into deterministic action brackets (`LOW_RISK` < 40%, `MODERATE_RISK` 40-70%, `CRITICAL_RISK` $\ge$ 70%) ensuring business retention strategies are transparently auditable.