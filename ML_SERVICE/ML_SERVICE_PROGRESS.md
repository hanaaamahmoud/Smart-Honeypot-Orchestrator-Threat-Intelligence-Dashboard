│   │   ├── step7d_dbscan_cluster_sizes.csv
│   │   ├── step7d_dbscan_detailed_cluster_profiles.csv
│   │   ├── step7d_dbscan_noise_behavioral_profile.csv
│   │   ├── step7d_dbscan_top_behavioral_features.csv
│   │   ├── step7e_corrected_cluster_validation_audit.json
│   │   ├── step7e_corrected_stability_results.csv
│   │   ├── step7e_pairwise_stability_results.csv
│   │   ├── step7g_dbscan_behavioral_reference_centroids.csv
│   │   ├── step7g_production_cluster_pipeline_audit.json
│   │   ├── step7g_production_config.json
│   │   ├── step7g_reference_behavioral_assignments.csv
│   │   ├── step7g_reference_distance_summary.csv
│   │   ├── step7h_future_log_distance_summary.csv
│   │   ├── step7h_future_log_simulated_assignments.csv
│   │   ├── step7h_manifest.json
│   │   └── step7h_production_feature_schema.json
│   └── frozen_reference_sha256.json
├── tests/
│   ├── integration/
│   │   ├── init.py
│   │   ├── test_l210_real_elk_frozen_pipeline.py
│   │   ├── test_l29_pipeline_compatibility.py
│   │   └── test_real_elk_canonical.py
│   ├── unit/
│   │   ├── init.py
│   │   ├── test_canonical_adapter.py
│   │   └── test_elasticsearch_reader.py
│   ├── init.py
│   ├── test_d2_contract.py
│   ├── test_d2_regression.py
│   ├── test_d3_7_feature_assembly.py
│   ├── test_d3_8_feature_validation.py
│   ├── test_d3_regression.py
│   ├── test_d4_feature_validation.py
│   ├── test_d4_integration.py
│   ├── test_feature_contract.py
│   ├── test_feature_generation_base.py
│   ├── test_feature_generation_density.py
│   ├── test_feature_generation_diversity.py
│   ├── test_feature_generation_geo.py
│   ├── test_feature_generation_temporal.py
│   ├── test_feature_validation.py
│   ├── test_health.py
│   ├── test_input_adapter.py
│   ├── test_output_adapter.py
│   ├── test_output_analytics_contract.py
│   ├── test_output_session_contract.py
│   ├── test_process_integration.py
│   ├── test_session_boundaries.py
│   ├── test_session_contract.py
│   ├── test_session_grouping.py
│   ├── test_session_id_policy.py
│   ├── test_session_ordering.py
│   └── test_session_reconstruction.py
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
