
# Data Document

This folder contains the documentation for the complete honeypot security analytics pipeline.

The documentation is organized by project stage, from raw dataset preprocessing to session reconstruction, behavioral feature engineering, machine learning, behavioral analysis, dashboard integration, and production runtime.

---

## Project Pipeline

```text
Raw Honeypot Datasets
        │
        ▼
Data Preprocessing & Normalization
        │
        ▼
Session Reconstruction
        │
        ▼
Behavioral Feature Engineering
        │
        ▼
Unsupervised Machine Learning
        │
        ▼
Behavioral Analysis
        │
        ▼
Dashboard & Analytics
        │
        ▼
Production Runtime Pipeline

```

---

## Documentation Structure

```text
docs/datasets/
├── README.md
│
├── preprocessing/
│   ├── ftp-dataset.md
│   ├── http-dataset.md
│   ├── ssh-dataset.md
│   └── unified-dataset.md
│
├── 2_session_reconstruction/
│   └── session-reconstruction.md
│
├── Behavioral Feature Engineering/
│   └── Behavioral_Feature.md
│
├── Unsupervised Machine Learning/
│   ├── Unsupervised_ML.md
│   └── Why_not_Supervised_Learning.md
│
├── behavioral_analysis/
│   └── behavioral_analysis.md
│
├── dashboard/
│   └── dashboard.md
│
└── Runtime Pipeline/
    └── Runtime Pipeline.md

```

---



## Documentation Index

| Stage | Document Link | Description |
| :--- | :--- | :--- |
| **1. FTP Preprocessing** | [ftp-dataset.md](preprocessing/ftp-dataset.md) | Preprocessing and normalization of FTP honeypot data |
| **2. HTTP Preprocessing** | [http-dataset.md](preprocessing/http-dataset.md) | Preprocessing and normalization of HTTP honeypot data |
| **3. SSH Preprocessing** | [ssh-dataset.md](preprocessing/ssh-dataset.md) | Preprocessing and normalization of SSH honeypot data |
| **4. Unified Dataset** | [unified-dataset.md](preprocessing/unified-dataset.md) | Schema alignment and merging of the processed datasets |
| **5. Session Reconstruction** | [session-reconstruction.md](2_session_reconstruction/session-reconstruction.md) | Reconstruction of individual events into logical sessions |
| **6. Behavioral Features** | [Behavioral_Feature.md](Behavioral%20Feature%20Engineering/Behavioral_Feature.md) | Creation of session-level behavioral features |
| **7. Unsupervised ML** | [Unsupervised_ML.md](Unsupervised%20Machine%20Learning/Unsupervised_ML.md) | Clustering and behavioral pattern discovery using unsupervised learning |
| **7.1 ML Approach** | [Why_not_Supervised_Learning.md](Unsupervised%20Machine%20Learning/Why_not_Supervised_Learning.md) | Explanation of why supervised learning was not selected |
| **8. Behavioral Analysis** | [behavioral_analysis.md](behavioral_analysis/behavioral_analysis.md) | Analysis of attacker behavior, patterns, and threat intelligence |
| **9. Dashboard & Analytics** | [dashboard.md](dashboard/dashboard.md) | Dashboard integration, session replay, GeoIP, MITRE, clustering, and trends |
| **10. Runtime Pipeline** | [Runtime Pipeline.md](Runtime%20Pipeline/Runtime%20Pipeline.md) | Production new-log inference and frozen-model runtime pipeline |


---

## Data Flow

```text
FTP ──────┐
HTTP ─────┼──► Preprocessing & Normalization
SSH ──────┘
                    │
                    ▼
             Unified Dataset
                    │
                    ▼
          Session Reconstruction
                    │
                    ▼
        Behavioral Feature Engineering
                    │
                    ▼
          Unsupervised Machine Learning
                    │
              ┌─────┴─────┐
              ▼           ▼
           Clusters      Noise
              │           │
              └─────┬─────┘
                    ▼
           Behavioral Analysis
                    │
                    ▼
          Dashboard & Analytics
                    │
                    ▼
           Production Runtime

```

---

## Main Project Components

* **Data Preprocessing:** Raw FTP, HTTP, and SSH honeypot datasets are cleaned, normalized, and aligned into a unified dataset.
* **Session Reconstruction:** Individual events are grouped into logical sessions while preserving traceability to the original events.
* **Behavioral Feature Engineering:** Session-level behavioral features are extracted to represent attacker activity and interaction patterns.
* **Unsupervised Machine Learning:** Unsupervised clustering is used to discover behavioral patterns without relying on attack labels.
* **Behavioral Analysis:** The discovered behaviors are analyzed using attacker IP information, MITRE ATT&CK mapping, session replay, clustering, and temporal analysis.
* **Dashboard & Analytics:** The processed intelligence is integrated into a unified dashboard dataset for visualization and investigation.
* **Production Runtime:** New security logs can pass through the same validated feature pipeline and be assigned using the frozen production clustering reference without retraining.

---

## Documentation Purpose

The files in this directory document how each stage of the project was implemented and validated. The actual analysis notebooks are maintained separately under the project's `notebooks/` directory.

```text
Documentation
     │
     └── docs/datasets/

Analysis & Experiments
     │
     └── notebooks/

```

*This separation keeps the documentation organized while allowing the notebooks to contain the actual implementation and experiments.*

```

```
