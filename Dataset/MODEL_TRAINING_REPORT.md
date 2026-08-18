# MOSAIC V1.1 Phase 3 Model Training Report

> **IMPORTANT:** The dataset is simulated and these results validate the ML/software pipeline. They do not establish real-world deception-detection accuracy.

## 1. Dataset & Target
- Rows: 3000
- Target: ground_truth_binary
- Participants: 300

## 2. Feature Groups
- Physiology: 41
- Audio: 82
- Vision: 120

## 3. Cross-Validation & Leakage Prevention
- **CV Strategy**: 5-fold StratifiedGroupKFold grouped by participant_id.
- **Leakage Check**: No participant exists in both training and test within a fold. All target and prediction labels were excluded from the feature space. Preprocessing pipelines (imputation and scaling) were strictly fit within the cross-validation folds.

## 4. Modeling Results
| Model       |   Accuracy |   Precision |   Recall |       F1 |   ROC_AUC |   Specificity |   Sensitivity |   Balanced_Accuracy |
|:------------|-----------:|------------:|---------:|---------:|----------:|--------------:|--------------:|--------------------:|
| Physiology  |   0.619667 |    0.620067 | 0.618    | 0.619032 |  0.662738 |      0.621333 |      0.618    |            0.619667 |
| Audio       |   0.691333 |    0.701828 | 0.665333 | 0.683094 |  0.755502 |      0.717333 |      0.665333 |            0.691333 |
| Vision      |   0.687667 |    0.683388 | 0.699333 | 0.691269 |  0.748898 |      0.676    |      0.699333 |            0.687667 |
| Late Fusion |   0.734333 |    0.736382 | 0.73     | 0.733177 |  0.800978 |      0.738667 |      0.73     |            0.734333 |

## 5. Ablation Results
| Combination                 |   Accuracy |   Precision |   Recall |       F1 |   ROC_AUC |   Specificity |   Sensitivity |   Balanced_Accuracy |
|:----------------------------|-----------:|------------:|---------:|---------:|----------:|--------------:|--------------:|--------------------:|
| Physiology                  |   0.617    |    0.617864 | 0.613333 | 0.61559  |  0.662395 |      0.620667 |      0.613333 |            0.617    |
| Audio                       |   0.690333 |    0.698126 | 0.670667 | 0.684121 |  0.753928 |      0.71     |      0.670667 |            0.690333 |
| Vision                      |   0.687667 |    0.684107 | 0.697333 | 0.690657 |  0.748464 |      0.678    |      0.697333 |            0.687667 |
| Physiology + Audio          |   0.703667 |    0.708532 | 0.692    | 0.700169 |  0.765221 |      0.715333 |      0.692    |            0.703667 |
| Physiology + Vision         |   0.692667 |    0.692154 | 0.694    | 0.693076 |  0.760778 |      0.691333 |      0.694    |            0.692667 |
| Audio + Vision              |   0.726667 |    0.728495 | 0.722667 | 0.725569 |  0.798215 |      0.730667 |      0.722667 |            0.726667 |
| Physiology + Audio + Vision |   0.734333 |    0.736382 | 0.73     | 0.733177 |  0.800978 |      0.738667 |      0.73     |            0.734333 |

## 6. Missing Modality Analysis
| Subset                     |   Count |   Accuracy |       F1 |   ROC_AUC |
|:---------------------------|--------:|-----------:|---------:|----------:|
| All Trials                 |    3000 |   0.734333 | 0.733177 |  0.800978 |
| Complete Multimodal Trials |    2844 |   0.734529 | 0.731794 |  0.803999 |
| Missing Physiology         |      42 |   0.785714 | 0.8      |  0.773455 |
| Missing Audio              |      58 |   0.586207 | 0.555556 |  0.566106 |
| Missing Vision             |      56 |   0.839286 | 0.876712 |  0.865278 |

Missing modalities were handled using median imputation alongside availability indicator flags. The model learned to adjust its predictions based on the flags.

## 7. Comparison with v1.1 Reference Results
The accuracy and ROC-AUC numbers are generally comparable to the reference simulated values. The goal was transparent reproducibility rather than hyperparameter over-optimization.

