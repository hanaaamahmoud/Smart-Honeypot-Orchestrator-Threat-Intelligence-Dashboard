# Why Not Supervised Learning?

## 1. Overview
Supervised Learning was considered for the project, but it was not selected as the primary Machine Learning approach.
The main reason is that the available attack labels were not reliable enough to represent independent ground truth for session-level behavioral classification.

---

## 2. Label Quality Issues
The label audit identified several issues with the available labels:

* Missing values in attack-related fields.
* Strong class imbalance between attack types.
* Multiple attack types appearing within the same session.
* Inconsistent session-level label purity.

This makes the labels less suitable for reliable supervised classification.

---

## 3. Target Leakage
Several features were found to be strongly related to the target labels.

Examples include:
* `event_sequence`
* `is_web_attack`
* `has_mitre_activity`

Some of these features were derived from attack information or directly reflected the target.
Using them for supervised training could produce artificially high performance and misleading results.

---

## 4. Dataset Dependency
The audit also showed strong relationships between attack labels and dataset metadata such as:

* `honeypot`
* `protocol`
* `source_dataset`

Some attack types were strongly associated with specific honeypots or protocols.
As a result, a supervised model could learn dataset-specific patterns instead of learning general attacker behavior.

---

## 5. Why Unsupervised Learning Was Selected
The main objective of the project is to discover behavioral patterns and unusual sessions, rather than simply reproduce existing attack labels.

Therefore, Unsupervised Learning was more appropriate because it:
* Does not require trusted attack labels.
* Reduces dependence on predefined attack categories.
* Groups sessions according to their behavioral characteristics.
* Helps identify unusual or noisy sessions.
* Supports behavioral analysis and anomaly detection.

---

## 6. Final Decision
Based on the label quality, leakage risks, and strong dependency between labels and dataset metadata, Unsupervised Learning was selected as the primary ML approach.

The project therefore evaluated:
* **K-Means**
* **DBSCAN**
* **Agglomerative Clustering**

These models were used to discover behavioral clusters directly from the session-level features.
