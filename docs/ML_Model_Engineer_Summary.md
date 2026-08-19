# ML Model Comparison — Engineer Summary

## Model Comparison

| Model | Configuration | Clusters | Noise | Silhouette | Davies-Bouldin | Calinski-Harabasz |
|---|---|---:|---:|---:|---:|---:|
| KMeans | k=5 | 5 | 0% | 0.530189 | 0.672791 | 3209.496424 |
| DBSCAN | eps=0.5, min_samples=20 | 38 | 14.11% | 0.749525 | 0.404699 | 20175.806989 |
| Agglomerative | k=6 | 6 | 0% | 0.530656 | 0.582562 | 3028.434056 |

## Selected Model

**DBSCAN** was selected as the primary model because it achieved the strongest separation metrics and explicitly identified noisy/anomalous sessions.

- Silhouette Score: **0.749525**
- Davies-Bouldin Index: **0.404699**
- Calinski-Harabasz Score: **20175.806989**
- Noise fraction: **14.11%**

KMeans was kept as a baseline, while Agglomerative was used as a secondary comparison model.

## Production Reference

The selected production configuration is:

- Algorithm: **DBSCAN**
- `eps = 0.5`
- `min_samples = 20`
- Behavioral features: **48**
- Mode: **FROZEN_PRODUCTION_REFERENCE**
- Assignment: **EXISTING_REFERENCE_ONLY**

New logs are processed using the same production feature contract and assigned against the frozen reference rather than retraining the model.

## Note

Some artifacts report **38 non-noise clusters**, while another cluster-size summary reports **39 total clusters** because that count includes the noise group. The production reference uses **38 non-noise clusters + noise**.
