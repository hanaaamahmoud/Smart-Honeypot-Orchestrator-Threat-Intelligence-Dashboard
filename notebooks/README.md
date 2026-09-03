
# Honeypot Security Data Pipeline

This folder contains the notebooks used to build the project pipeline from raw honeypot logs to behavioral analysis, machine learning, and dashboard preparation.

The project was developed as a sequence of connected stages, where the output of each stage becomes the input for the next one.


## 1. Data Collection & Cleaning

The first stage focused on processing the raw honeypot datasets and preparing them for analysis. Different honeypot sources were processed and cleaned, including SSH, HTTP, FTP, and Dionaea-related logs.

**Main Notebooks:**
* [`ssh-honeypot-data-pipeline.ipynb`](./data_preprocessing/ssh-honeypot-data-pipeline.ipynb)
* [`http_honeypot_log_pipeline.ipynb`](./data_preprocessing/http_honeypot_log_pipeline.ipynb)
* [`ftp_json_commands_pipeline.ipynb`](./data_preprocessing/ftp_json_commands_pipeline.ipynb)
* [`dionaea_ftp_sqlite_logins.ipynb`](./data_preprocessing/dionaea_ftp_sqlite_logins.ipynb)

These notebooks handled the initial parsing, cleaning, normalization, and preparation of the different raw log formats.



## 2. Dataset Merge

After cleaning the individual datasets, the next stage was to combine them into a unified security-events dataset.

**Notebook:**
* [`merge_honeypot_datasets.ipynb`](./data_preprocessing/merge_honeypot_datasets.ipynb)

The purpose of this stage was to align the different sources and produce a common dataset that could be used consistently in the following stages.



## 3. Session Reconstruction

After the datasets were merged, the next step was to reconstruct logical sessions from individual security events.

**Notebook:**
* [`session_reconstruction.ipynb`](./session_reconstruction/session_reconstruction.ipynb)

This stage connected related events and organized them into reconstructed sessions. The reconstructed sessions became the main unit of analysis for the behavioral features and machine learning stages.



## 4. Behavioral Feature Engineering

After session reconstruction, behavioral features were generated from the session activity.

**Notebook:**
* [`Behavioral Feature Engineering.ipynb`](./Behavioral%20Feature%20Engineering/Behavioral%20Feature%20Engineering.ipynb)

**Extracted Behavioral Information:**
* Event and activity statistics
* Authentication behavior
* Command activity
* Network and protocol characteristics
* Data transfer behavior
* Session-level behavioral patterns

The goal was to transform raw session activity into structured numerical features suitable for machine learning.



## 5. Machine Learning

The engineered behavioral features were then used for machine learning and behavioral analysis.

**Notebooks:**
* [`Machine_learning.ipynb`](./Machine_learning/Machine_learning.ipynb)
* [`behavioral_analysis.ipynb`](./behavioral_analysis/behavioral_analysis.ipynb)

This stage focused on analyzing session behavior and identifying groups or patterns of similar activity. The machine learning stage was based on behavioral features generated from the reconstructed sessions rather than directly using raw log rows.



## 6. Dashboard & Threat Intelligence

The results from the previous stages were then prepared for dashboard visualization and security analysis.

**Notebook:**
* [`Geoip-enrichment-dashboard.ipynb`](./dashboard/Geoip-enrichment-dashboard.ipynb)

This stage combined the available behavioral and security information with enrichment and dashboard-oriented analysis, including geographic context and attacker-related information.

**Components Integrated into the Dashboard:**
* Session information
* Behavioral analysis
* Machine learning results
* GeoIP enrichment
* Attacker IP analytics
* Threat intelligence
* Session replay
* Temporal trends


## 7. Real-Time / Production Stage

The final part of the project is the production-oriented pipeline for processing new honeypot logs using the approved existing ML pipeline.


```

New Logs
│
▼
Parsing & Normalization
│
▼
Session Reconstruction
│
▼
Behavioral Feature Generation
│
▼
Feature Validation
│
▼
Frozen ML Model / Reference
│
▼
Production Assignment
│
▼
Threat Analytics
│
▼
Dashboard / Real-Time Visualization

```

The production stage is designed to use the existing approved machine-learning reference without retraining it on new logs.

---

## 8. Complete Project Flow


```

Raw Honeypot Logs
│
▼
Data Cleaning & Parsing
│
▼
Dataset Normalization
│
▼
Dataset Merge
│
▼
Session Reconstruction
│
▼
Behavioral Feature Engineering
│
▼
Machine Learning
│
▼
Behavioral Analysis
│
▼
GeoIP / Threat Intelligence Enrichment
│
▼
Dashboard & Session Replay
│
▼
Real-Time / Production Inference

```

---

## 9. Notebook Organization

| Stage | Notebook |
| :--- | :--- |
| **SSH Data Pipeline** | [`ssh-honeypot-data-pipeline.ipynb`](./data_preprocessing/ssh-honeypot-data-pipeline.ipynb) |
| **HTTP Data Pipeline** | [`http_honeypot_log_pipeline.ipynb`](./data_preprocessing/http_honeypot_log_pipeline.ipynb) |
| **FTP Data Pipeline** | [`ftp_json_commands_pipeline.ipynb`](./data_preprocessing/ftp_json_commands_pipeline.ipynb) |
| **Dionaea Data Pipeline** | [`dionaea_ftp_sqlite_logins.ipynb`](./data_preprocessing/dionaea_ftp_sqlite_logins.ipynb) |
| **Dataset Merge** | [`merge_honeypot_datasets.ipynb`](./data_preprocessing/merge_honeypot_datasets.ipynb) |
| **Session Reconstruction** | [`session_reconstruction.ipynb`](./session_reconstruction/session_reconstruction.ipynb) |
| **Behavioral Feature Engineering** | [`Behavioral Feature Engineering.ipynb`](./Behavioral%20Feature%20Engineering/Behavioral%20Feature%20Engineering.ipynb) |
| **Machine Learning** | [`Machine_learning.ipynb`](./Machine_learning/Machine_learning.ipynb) |
| **Behavioral Analysis** | [`behavioral_analysis.ipynb`](./behavioral_analysis/behavioral_analysis.ipynb) |
| **GeoIP & Dashboard** | [`Geoip-enrichment-dashboard.ipynb`](./dashboard/Geoip-enrichment-dashboard.ipynb) |

---

## 10. Large Final Notebooks

Some of the final Dashboard / Real-Time notebooks and related outputs are large and could not be uploaded directly to this repository. They are therefore treated as part of the final project stage even when the corresponding notebook or generated artifact is not included in the repository.

The documented pipeline and previous outputs describe how these final components connect to the rest of the project.

---

## 11. Final Result

The project progresses from heterogeneous raw honeypot logs to a unified, session-based behavioral analysis pipeline.

**Final Architecture:**
Data Cleaning $\rightarrow$ Merge $\rightarrow$ Session Reconstruction $\rightarrow$ Behavioral Features $\rightarrow$ Machine Learning $\rightarrow$ Behavioral Analysis $\rightarrow$ Threat Intelligence $\rightarrow$ Dashboard $\rightarrow$ Real-Time Production

Each stage is separated into its own notebook or project component so that the full workflow can be traced from the original raw data to the final security analysis and visualization.
