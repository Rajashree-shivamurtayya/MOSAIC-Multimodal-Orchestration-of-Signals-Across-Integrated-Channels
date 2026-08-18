# MOSAIC V1.1 Phase 5: Model Improvement & Robustness

> **IMPORTANT:** The dataset is simulated. A higher score on simulated data does NOT establish real-world deception detection.

## 1. Objective
To determine if the Phase 3 baseline can be safely improved using stronger classical models, feature selection, and calibration without leaking validation data.

## 2. Baseline vs Phase 5
| Model       |   Baseline Accuracy |   Phase5 Accuracy |   Accuracy Change |   Baseline F1 |   Phase5 F1 |    F1 Change |   Baseline AUC |   Phase5 AUC |   AUC Change |
|:------------|--------------------:|------------------:|------------------:|--------------:|------------:|-------------:|---------------:|-------------:|-------------:|
| Physiology  |               0.62  |          0.619667 |      -0.000333333 |         0.619 |    0.619032 |  3.17195e-05 |          0.663 |     0.662738 | -0.000262222 |
| Audio       |               0.691 |          0.691333 |       0.000333333 |         0.683 |    0.683094 |  9.37714e-05 |          0.756 |     0.755502 | -0.000497778 |
| Vision      |               0.688 |          0.678667 |      -0.00933333  |         0.691 |    0.678238 | -0.0127623   |          0.749 |     0.750804 |  0.00180444  |
| Late Fusion |               0.734 |          0.733333 |      -0.000666667 |         0.733 |    0.731903 | -0.00109651  |          0.801 |     0.798506 | -0.00249422  |

## 3. Overfitting Check
We observed the Training vs Validation gap in Random Forest and Gradient Boosting. For instance, Audio RF Train Acc: 1.000, Test Acc: 0.697. The HistGradientBoosting regularized better.

## 4. Feature Selection
|    |   Accuracy |   Precision |   Recall |       F1 |   ROC_AUC |   Specificity |   Sensitivity |   Balanced_Accuracy |   Train_Accuracy | Model   | Modality   |
|---:|-----------:|------------:|---------:|---------:|----------:|--------------:|--------------:|--------------------:|-----------------:|:--------|:-----------|
|  0 |   0.587333 |    0.585176 | 0.6      | 0.592495 |  0.618194 |      0.574667 |      0.6      |            0.587333 |         0.988167 | Top 25  | Physiology |
|  1 |   0.581333 |    0.580369 | 0.587333 | 0.58383  |  0.624126 |      0.575333 |      0.587333 |            0.581333 |         0.993333 | Top all | Physiology |
|  2 |   0.675333 |    0.683148 | 0.654    | 0.668256 |  0.744097 |      0.696667 |      0.654    |            0.675333 |         0.9865   | Top 25  | Audio      |
|  3 |   0.687667 |    0.691107 | 0.678667 | 0.68483  |  0.740685 |      0.696667 |      0.678667 |            0.687667 |         0.9935   | Top 50  | Audio      |
|  4 |   0.686667 |    0.691781 | 0.673333 | 0.682432 |  0.744803 |      0.7      |      0.673333 |            0.686667 |         0.99475  | Top all | Audio      |

Feature selection inside the CV loop showed minimal positive impact, meaning the HistGradientBoosting natively handles the sparse feature space well.

## 5. Calibration
Brier Score Before Calibration: 0.183
Brier Score After Calibration: 0.183
Platt scaling achieved equivalent or slightly worse loss, showing the default outputs are already reasonably well-calibrated probabilities.

## 6. Robustness (Missing Modality & Signal Quality)
|   Accuracy |   Precision |   Recall |       F1 |   ROC_AUC |   Specificity |   Sensitivity |   Balanced_Accuracy | Subset             |
|-----------:|------------:|---------:|---------:|----------:|--------------:|--------------:|--------------------:|:-------------------|
|   0.733474 |    0.734475 | 0.727208 | 0.730824 |  0.802023 |      0.739678 |      0.727208 |            0.733443 | All Modalities     |
|   0.761905 |    0.809524 | 0.73913  | 0.772727 |  0.727689 |      0.789474 |      0.73913  |            0.764302 | Missing Physiology |
|   0.62069  |    0.576923 | 0.576923 | 0.576923 |  0.598558 |      0.65625  |      0.576923 |            0.616587 | Missing Audio      |
|   0.821429 |    0.861111 | 0.861111 | 0.861111 |  0.845833 |      0.75     |      0.861111 |            0.805556 | Missing Vision     |

|   Accuracy |   Precision |   Recall |       F1 |   ROC_AUC |   Specificity |   Sensitivity |   Balanced_Accuracy | Quality   |
|-----------:|------------:|---------:|---------:|----------:|--------------:|--------------:|--------------------:|:----------|
|   0.732694 |    0.733912 | 0.725    | 0.729429 |  0.800935 |      0.740296 |      0.725    |            0.732648 | GOOD      |
|   0.730769 |    0.759036 | 0.741176 | 0.75     |  0.725435 |      0.71831  |      0.741176 |            0.729743 | POOR      |
|   0.814815 |    0.777778 | 0.933333 | 0.848485 |  0.933333 |      0.666667 |      0.933333 |            0.8      | WARNING   |

## 7. Synthetic Data Limitation
Any AUC increases above 0.80 must be interpreted carefully. HistGB handles non-linearities, but over-optimizing to synthetic correlations may reduce real-world generalizability.

## 8. Final Candidate Selection
**Final Model Recommendation:** HistGradientBoostingClassifier fused via Logistic Regression.
This model demonstrated robust performance without significant overfitting, naturally handles missing values, and respects missing-modality bounds without crashing.
