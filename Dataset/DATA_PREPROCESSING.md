# MOSAIC Dataset V1.1 Preprocessing and Validation Report

## 1. Dataset Description
The dataset processed is the MOSAIC simulated dataset v1.1. It contains simulated physiological, audio, and visual features corresponding to simulated participants undergoing structured question/answer trials. 

## 2. Why the Dataset is Simulated
The dataset is explicitly SIMULATED and is used for software and ML pipeline validation. It provides a structured data layout mimicking a multimodal setup (Physiology, Audio, Computer Vision) but does NOT represent real human deception. The data was generated to validate the machine learning architecture prior to data collection.

## 3. Dataset Dimensions
- **Rows:** 3,000
- **Columns:** 349

## 4. Participant/Trial Structure
- **Unique Participants:** 300
- **Trials per Participant:** 10
- **Total Trials:** 3,000
- All participants followed the correct 10-trial structure. No duplicate rows or participant-trial combinations were identified.

## 5. Target Definition
- **Target Columns:** `ground_truth_binary`, `ground_truth_label`
- **Class Balance:** Perfectly balanced (1,500 Truthful vs 1,500 Deceptive trials).

## 6. Feature Groups
Modality identification grouped the features into the following categories:
- **Physiology Features:** 41
- **Audio Features:** 82
- **Vision Features:** 122
- **Metadata/Question Features:** 12
- **Leakage/Model Output Features:** 16

## 7. Missing-Value Analysis
- **Missing Values:** 16,064 total missing cells.
- The missing values are intentionally simulated to represent real-world missing modalities (e.g., failed sensor connections, missing audio quality scores, dropped video frames).
- **Resolution:** These missing cases have been intentionally preserved for later robustness testing (e.g., missing modality imputation handling).

## 8. Data-Quality Checks
- **Constant Features:** 10 constant columns were identified (e.g., `camera_fps`, `camera_resolution`, `microphone_type`, `data_source`). 
- **Derived-feature validation:** The check for derived mathematical relationships (`HR Change`) resulted in a FAIL for 2,667 rows, indicating that `heart_rate_bpm - baseline_heart_rate_bpm` did not exactly equal `heart_rate_change_from_baseline` (with an absolute error up to 0.1). This reflects typical simulated float variability, but models must be mindful of how derived metrics are utilized.

## 9. Leakage Prevention
16 specific columns have been identified and flagged for removal from the final feature set. These include target labels, experiment conditions, question properties, and direct output predictions from component models.
Excluded:
- `ground_truth_binary`
- `ground_truth_label`
- `experiment_condition`
- `deception_instruction`
- `prediction_confidence`
- `prediction_correct`
- `question_id`
- `question_difficulty`
- All `*_model_probability` and `*_model_prediction` columns

## 10. Participant-Level Splitting Requirement
Because there are multiple trials (10) for each participant, the eventual ML pipeline MUST use participant-level splitting (e.g., `GroupKFold` or `StratifiedGroupKFold`) with groups set to `participant_id`. Random row-level splitting is strictly prohibited as it will cause data leakage.

## 11. CV Feature Validation
- 3 out of 4 expected standard Computer Vision features were found.
- **Naive Features:** The `naive_left_eyebrow_delta_camera_frame` and `naive_right_eyebrow_delta_camera_frame` features were correctly identified in the dataset.
- **IMPORTANT:** These naive features are deliberately included as a confound demonstration and MUST NOT be used in the final ML feature set.

## 12. Outlier Handling
Potential outliers were identified via IQR bounds for numerical features. 
- **Resolution:** Outliers have not been deleted, as physiological and behavioral signals naturally contain significant variation, and these simulated bounds may represent valid simulated edge cases.

## 13. What Was Changed
- Data schema was validated, missing values and constants were audited.
- Modality group assignments were created into `feature_groups.json`.
- A set of CSV reports identifying distributions, outliers, and leakage was produced.
- A clean copy of the dataset was saved to `processed/mosaic_clean.csv`.

## 14. What Was Deliberately NOT Changed
- No rows were deleted.
- No simulated data was altered.
- `data_source` remains `SIMULATED`.
- No target/label imputation or transformation was performed.

## 15. Next Step
The next step is ML preprocessing and model training. Any scaler or imputer used during the ML phase must be fitted ONLY on the training folds. Model training should not proceed until explicitly requested.
