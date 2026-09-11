# Step 6 — Unsupervised Machine Learning

## 1. Overview
This step focused on applying Unsupervised Machine Learning to the session-level behavioral features generated in Step 5.
The goal was to discover behavioral patterns and group similar sessions without using attack labels or predefined classes.
The input dataset was:
`session_behavioral_features_v4.csv`

---

## 2. Input Verification
Before model training, the dataset was validated to ensure data integrity and prevent data leakage.
The following checks were performed:

* Verified the dataset using its SHA-256 hash.
* Confirmed the dataset contains 11,880 sessions.
* Checked `reconstructed_session_id` for missing or duplicate values.
* Verified that forbidden labels were not used, including:
  * `attack_type`
  * `attack_stage`
  * `severity`
  * `mitre_technique`
* Checked numeric and non-numeric features.
* Detected unexpected NaN or Inf values.

An audit report was saved as:
`step6a_ml_input_verification_audit.json`

---

## 3. Preprocessing & Standardization
The behavioral features were prepared for clustering without modifying the original dataset.
The preprocessing included:

* Removing ID and timestamp columns.
* Selecting numeric features for machine learning.
* Removing features containing only missing values.
* Applying `StandardScaler` to normalize the feature values.

The ML-ready dataset was exported as:
`session_behavioral_features_v4_ml_ready.csv`

*Scaler parameters and preprocessing audit information were also saved.*

---

## 4. K-Means Clustering
K-Means clustering was evaluated using different numbers of clusters.
Models were tested with:
* $k = 2 \rightarrow 10$

Each configuration was evaluated using:
* Silhouette Score
* Davies-Bouldin Score
* Calinski-Harabasz Score

The configuration with the highest Silhouette Score was selected as the best K-Means model.
The cluster assignments were saved as:
`kmeans_cluster_assignments.csv`

---

## 5. DBSCAN Clustering
DBSCAN was used to identify density-based behavioral groups and isolate unusual sessions as noise.
A grid search was performed using different:

* `eps` values from 0.5 to 3.0
* `min_samples` values of 5, 10, and 20

Each valid configuration was evaluated using:
* Silhouette Score
* Davies-Bouldin Score
* Calinski-Harabasz Score

Invalid configurations were filtered out, including cases with too few clusters or excessive noise.
The best DBSCAN configuration was selected based on clustering performance.
The cluster assignments were saved as:
`dbscan_cluster_assignments.csv`

*Noise sessions were also recorded.*

---

## 6. Agglomerative Clustering
Hierarchical clustering was evaluated using Agglomerative Clustering with Ward linkage.
Models were tested with:
* $k = 2 \rightarrow 10$

The models were evaluated using:
* Silhouette Score
* Davies-Bouldin Score
* Calinski-Harabasz Score

The best configuration was selected using the highest Silhouette Score.
The resulting assignments were saved as:
`agglomerative_cluster_assignments.csv`

---

## 7. Final Model Comparison & Audit
The three clustering approaches were compared:
* K-Means
* DBSCAN
* Agglomerative Clustering

The final audit verified that:
* All 11,880 session IDs were preserved across the clustering outputs.
* No forbidden labels were introduced.
* Model results were consistent with the original session dataset.

The best configurations were ranked using the clustering evaluation metrics.
The consolidated comparison was exported as:
`step6f_model_comparison.csv`

The final audit was saved as:
`step6f_unsupervised_ml_audit.json`

---

## 8. Final Packaging
All Step 6 outputs were checked and packaged into a reproducible archive.
The final package was:
`STEP_6_UNSUPERVISED_ML_COMPLETE.zip`

*A SHA-256 checksum was also generated for the final archive.*

---

## 9. Result
Step 6 successfully transformed the validated behavioral session features into unsupervised behavioral clusters.

The clustering results provide a foundation for:
**Behavioral Analysis $\rightarrow$ Threat Detection $\rightarrow$ Dashboard / Session Replay**

The outputs from this step were used as the basis for identifying groups of similar sessions and detecting unusual or anomalous behavior.
