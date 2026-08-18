# MOSAIC Dataset V1.1 Phase 2: ML Preprocessing Report

## 1. Summary
This report details the machine learning preprocessing strategy implemented for the MOSAIC V1.1 simulated dataset. The goal of this phase was to prepare the cleaned dataset for ML training, ensuring no leakage, proper target extraction, safe handling of missing modalities, and robust cross-validation design. **No models have been trained.**

## 2. Target and Class Balance
- **Target Feature:** `ground_truth_binary`
- **Class Distribution:** 1500 Truthful vs 1500 Deceptive trials (Perfectly balanced)
- **Target Leakage Check:** PASS. The target and associated label fields were fully removed from the input `X` feature matrix.

## 3. Final Feature Groups
After excluding leakage, metadata, and the naive computer vision confound features, the feature sets are organized into three modality matrices:
- **Physiology features:** 41
- **Audio features:** 82
- **Vision features:** 120

These groups are persisted in `ml_feature_config.json`.

## 4. Participant-Level Splitting
Because the dataset contains repeated measures (10 trials per participant), random row-level splitting would leak identity characteristics into the test set. 
- **CV Strategy:** `StratifiedGroupKFold`
- **Grouping Variable:** `participant_id`
- **Participant Leakage Check:** PASS. The implemented split generator ensures no participant ever exists in both the training and testing sets simultaneously. `participant_id` is retained purely for grouping and is NOT included as an ML input feature.

## 5. Missing-Modality Strategy
The dataset contains approximately 5% trials where an entire modality (like video or physiology) is missing.
- **Implemented Strategy:** Option B - Median Imputation + Availability Flags.
- **Handling:** Numeric values for missing modalities are imputed using the median of that specific feature. Concurrently, availability flags (e.g. `audio_available`, `pulse_signal_quality`) are preserved in the input matrix as indicator variables, allowing the model to explicitly learn when a modality should be ignored.
- **Leakage Prevention:** Imputers are built inside `sklearn.pipeline.Pipeline` objects to ensure the median is calculated *only on the training fold* during cross-validation, never on the full dataset.

## 6. Feature Scaling Strategy
- **Implemented Strategy:** `StandardScaler`
- **Handling:** Numeric features within the physiology, audio, and vision domains are scaled to zero mean and unit variance.
- **Leakage Prevention:** Like imputation, scaling is bundled within the cross-validation pipelines. The scaler is fitted solely on the training subsets to prevent distribution leakage from the test subsets.

## 7. Outlier Strategy
- **Implemented Strategy:** Legitimate biological variability retention.
- **Handling:** As determined during Phase 1, the physiological and behavioral signals naturally contain extreme variations. No clipping or outlier deletion has been performed, avoiding artificial inflation of model performance on difficult samples.

## 8. Leakage and Confound Prevention
- **Leakage Exclusions:** 11 identified leakage features (e.g., component model predictions, correct flags) were strictly excluded from the ML pipeline.
- **Question Exclusions:** `question_id` and `question_difficulty` were excluded to prevent the model from learning question-specific shortcuts instead of general deceptive cues.
- **Computer Vision Confounds:** The naive eyebrow features (`naive_left_eyebrow_delta_camera_frame`, `naive_right_eyebrow_delta_camera_frame`) were confirmed excluded from the vision features group (PASS).

## 9. Next Steps
The dataset and preprocessing pipelines are fully configured and verified. Phase 3 (Model Training and Evaluation) can proceed safely using `ml_preprocessing.py`'s reusable loading and cross-validation pipelines.
