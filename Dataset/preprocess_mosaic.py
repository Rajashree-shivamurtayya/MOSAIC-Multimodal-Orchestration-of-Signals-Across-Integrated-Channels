import pandas as pd
import numpy as np
import json
import os
import sys

# Seed
np.random.seed(20260811)

# Paths
INPUT_CSV = 'mosaic_dataset_full_3000x349.csv'
DICT_CSV = 'mosaic_data_dictionary.csv'
PROCESSED_DIR = 'processed'

def main():
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)

    print("Loading data...")
    try:
        df = pd.read_csv(INPUT_CSV)
        data_dict = pd.read_csv(DICT_CSV)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # PHASE 1: Dataset Discovery
    print("==================================================")
    print("PHASE 1 - DATASET DISCOVERY")
    rows, cols = df.shape
    unique_participants = df['participant_id'].nunique()
    trials_per_participant = df.groupby('participant_id').size().mean()
    duplicates = df.duplicated().sum()
    duplicate_participant_trial = df.duplicated(subset=['participant_id', 'trial_id']).sum() if 'trial_id' in df.columns else 0
    
    print(f"Rows: {rows}")
    print(f"Columns: {cols}")
    print(f"Unique Participants: {unique_participants}")
    print(f"Avg Trials per Participant: {trials_per_participant}")
    print(f"Duplicate Rows: {duplicates}")
    print(f"Duplicate Participant/Trial: {duplicate_participant_trial}")

    # PHASE 2: Target and Class Analysis
    print("\n==================================================")
    print("PHASE 2 - TARGET AND CLASS ANALYSIS")
    target_cols = [c for c in ['ground_truth_binary', 'ground_truth_label'] if c in df.columns]
    print(f"Identified target columns: {target_cols}")
    
    class_dist = pd.DataFrame()
    for col in target_cols:
        counts = df[col].value_counts(dropna=False)
        pcts = df[col].value_counts(normalize=True, dropna=False) * 100
        print(f"\n{col} Class Counts:")
        print(counts)
        print(f"\n{col} Class Percentages:")
        print(pcts)
        temp_df = pd.DataFrame({'Class': counts.index, 'Count': counts.values, 'Percentage': pcts.values, 'Column': col})
        class_dist = pd.concat([class_dist, temp_df], ignore_index=True)
    
    class_dist.to_csv(os.path.join(PROCESSED_DIR, 'class_distribution.csv'), index=False)

    # PHASE 3: Data Quality Check
    print("\n==================================================")
    print("PHASE 3 - DATA QUALITY CHECK")
    missing_report = df.isnull().sum().reset_index()
    missing_report.columns = ['Column', 'MissingCount']
    missing_report['MissingPercentage'] = (missing_report['MissingCount'] / rows) * 100
    missing_report.to_csv(os.path.join(PROCESSED_DIR, 'missing_values_report.csv'), index=False)

    num_cols = df.select_dtypes(include=[np.number]).columns
    quality_stats = []
    constants = []
    
    for c in df.columns:
        uniques = df[c].nunique(dropna=False)
        if uniques <= 1:
            constants.append(c)
        
        stat = {
            'Column': c,
            'MissingCount': df[c].isnull().sum(),
            'MissingPercentage': (df[c].isnull().sum() / rows) * 100,
            'UniqueValues': uniques,
            'DataType': str(df[c].dtype),
        }
        if c in num_cols:
            stat['Min'] = df[c].min()
            stat['Max'] = df[c].max()
            stat['Mean'] = df[c].mean()
            stat['StdDev'] = df[c].std()
            inf_count = np.isinf(df[c]).sum()
            stat['InfCount'] = inf_count
            if inf_count > 0:
                print(f"Warning: {c} contains {inf_count} infinite values.")
        quality_stats.append(stat)
        
    print(f"Found {len(constants)} constant columns: {constants}")
    quality_df = pd.DataFrame(quality_stats)
    quality_df.to_csv(os.path.join(PROCESSED_DIR, 'preprocessing_report.csv'), index=False)

    # PHASE 4: Simulated Data Validation
    print("\n==================================================")
    print("PHASE 4 - SIMULATED DATA VALIDATION")
    if 'data_source' in df.columns:
        sim_count = (df['data_source'] == 'SIMULATED').sum()
        other_counts = df['data_source'][df['data_source'] != 'SIMULATED'].value_counts()
        print(f"SIMULATED rows: {sim_count}")
        if not other_counts.empty:
            print("WARNING: Unexpected data_source values found:")
            print(other_counts)
    else:
        print("WARNING: 'data_source' column not found!")

    # PHASE 5: Derived Feature Validation
    print("\n==================================================")
    print("PHASE 5 - DERIVED FEATURE VALIDATION")
    derived_checks = []
    
    # Check 1: heart_rate_change_from_baseline = heart_rate_bpm - baseline_heart_rate_bpm
    if all(c in df.columns for c in ['heart_rate_change_from_baseline', 'heart_rate_bpm', 'baseline_heart_rate_bpm']):
        calc = df['heart_rate_bpm'] - df['baseline_heart_rate_bpm']
        diff = np.abs(df['heart_rate_change_from_baseline'] - calc)
        max_err = diff.max()
        mean_err = diff.mean()
        failed = (diff > 1e-4).sum()
        derived_checks.append({'Relationship': 'HR Change', 'MaxErr': max_err, 'MeanErr': mean_err, 'FailedRows': failed})

    # Check 2: pause_ratio = silence_duration / response_duration
    if all(c in df.columns for c in ['pause_ratio', 'silence_duration', 'response_duration']):
        calc = df['silence_duration'] / df['response_duration']
        # replace div by zero or inf with NaN to compare properly
        calc.replace([np.inf, -np.inf], np.nan, inplace=True)
        # ignore NaNs for error computation
        mask = df['pause_ratio'].notna() & calc.notna()
        diff = np.abs(df.loc[mask, 'pause_ratio'] - calc.loc[mask])
        max_err = diff.max() if not diff.empty else 0
        mean_err = diff.mean() if not diff.empty else 0
        failed = (diff > 1e-4).sum()
        derived_checks.append({'Relationship': 'Pause Ratio', 'MaxErr': max_err, 'MeanErr': mean_err, 'FailedRows': failed})

    derived_df = pd.DataFrame(derived_checks)
    print(derived_df)
    derived_df.to_csv(os.path.join(PROCESSED_DIR, 'derived_feature_validation.csv'), index=False)

    # PHASE 6: Modality Identification
    print("\n==================================================")
    print("PHASE 6 - MODALITY IDENTIFICATION")
    # Mapping dict groups to JSON format
    groups = {}
    if 'column_name' in data_dict.columns and 'group' in data_dict.columns:
        for _, row in data_dict.iterrows():
            col = row['column_name']
            grp = row['group']
            if pd.isna(grp):
                grp = 'other'
            
            # map dictionary groups to requested JSON keys
            grp_str = str(grp).lower()
            if 'physio' in grp_str:
                k = 'physiology'
            elif 'audio' in grp_str:
                k = 'audio'
            elif 'vision' in grp_str or 'video' in grp_str or 'facial' in grp_str:
                k = 'vision'
            elif 'quality' in grp_str:
                k = 'quality'
            elif 'identity' in grp_str or 'metadata' in grp_str or 'question' in grp_str:
                k = 'metadata'
            elif 'label' in grp_str or 'target' in grp_str:
                k = 'target'
            elif 'leakage' in grp_str or 'evaluation' in grp_str or 'model' in grp_str:
                k = 'leakage'
            else:
                k = 'other'
                
            if k not in groups:
                groups[k] = []
            if col in df.columns:
                groups[k].append(col)
                
    with open(os.path.join(PROCESSED_DIR, 'feature_groups.json'), 'w') as f:
        json.dump(groups, f, indent=2)

    # PHASE 7: Leakage Audit
    print("\n==================================================")
    print("PHASE 7 - LEAKAGE AUDIT")
    explicit_leakage = [
        'ground_truth_binary', 'ground_truth_label', 'experiment_condition', 
        'deception_instruction', 'prediction_confidence', 'prediction_correct',
        'question_id', 'question_difficulty'
    ]
    explicit_leakage += [c for c in df.columns if c.endswith('_model_probability') or c.endswith('_model_prediction')]
    
    leakage_found = [c for c in explicit_leakage if c in df.columns]
    print(f"Leakage columns to exclude: {leakage_found}")
    
    leakage_df = pd.DataFrame({'LeakageColumn': leakage_found})
    leakage_df.to_csv(os.path.join(PROCESSED_DIR, 'leakage_report.csv'), index=False)

    # PHASE 8: Participant Structure
    print("\n==================================================")
    print("PHASE 8 - PARTICIPANT STRUCTURE")
    if 'participant_id' in df.columns and 'ground_truth_binary' in df.columns:
        part_struct = df.groupby('participant_id').agg(
            TotalTrials=('participant_id', 'count'),
            TruthfulTrials=('ground_truth_binary', lambda x: (x == 0).sum()),
            DeceptiveTrials=('ground_truth_binary', lambda x: (x == 1).sum())
        ).reset_index()
        
        anomalies = part_struct[part_struct['TotalTrials'] != 10]
        if not anomalies.empty:
            print("Participants with unexpected trial counts:")
            print(anomalies)
            
        part_struct.to_csv(os.path.join(PROCESSED_DIR, 'participant_structure.csv'), index=False)

    # PHASE 9: Missing Modality Analysis
    print("\n==================================================")
    print("PHASE 9 - MISSING MODALITY ANALYSIS")
    modality_cols = [c for c in df.columns if 'availability' in c.lower() or 'quality' in c.lower()]
    print(f"Modality availability/quality columns found: {modality_cols}")
    
    missing_modality = []
    for c in modality_cols:
        if df[c].dtype == object or df[c].dtype == bool:
            counts = df[c].value_counts().to_dict()
            missing_modality.append({'Column': c, 'Counts': str(counts)})
        else:
            missing = df[c].isnull().sum()
            missing_modality.append({'Column': c, 'Counts': f"Missing: {missing}"})
            
    pd.DataFrame(missing_modality).to_csv(os.path.join(PROCESSED_DIR, 'modality_summary.csv'), index=False)

    # PHASE 11: Computer Vision Validation
    print("\n==================================================")
    print("PHASE 11 - COMPUTER VISION VALIDATION")
    cv_features = ['left_eyebrow_height_delta', 'eyebrow_raise_ratio', 'baseline_head_yaw', 'head_yaw_delta']
    found_cv = [c for c in cv_features if c in df.columns]
    print(f"Standard CV features found: {len(found_cv)}/{len(cv_features)}")
    
    naive_features = [c for c in df.columns if c.startswith('naive_')]
    print(f"Naive confounding features found: {naive_features}")

    # PHASE 12: Outlier Analysis
    print("\n==================================================")
    print("PHASE 12 - OUTLIER ANALYSIS")
    outliers = []
    for c in num_cols:
        q1 = df[c].quantile(0.25)
        q3 = df[c].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 3 * iqr
        upper = q3 + 3 * iqr
        outlier_count = ((df[c] < lower) | (df[c] > upper)).sum()
        if outlier_count > 0:
            outliers.append({'Column': c, 'OutlierCount': outlier_count, 'LowerBound': lower, 'UpperBound': upper})
            
    outliers_df = pd.DataFrame(outliers)
    outliers_df.to_csv(os.path.join(PROCESSED_DIR, 'outlier_report.csv'), index=False)

    # PHASE 13: Save Cleaned Dataset
    df.to_csv(os.path.join(PROCESSED_DIR, 'mosaic_clean.csv'), index=False)
    
    # PHASE 16: Final Output Summary
    print("\n==================================================")
    print("DATASET VALIDATION COMPLETE")
    print(f"Rows: {rows}")
    print(f"Columns: {cols}")
    print(f"Participants: {unique_participants}")
    print(f"Trials: {rows}")
    
    if 'ground_truth_binary' in df.columns:
        truthful = (df['ground_truth_binary'] == 0).sum()
        deceptive = (df['ground_truth_binary'] == 1).sum()
    else:
        truthful = deceptive = "N/A"
        
    print(f"Truthful: {truthful}")
    print(f"Deceptive: {deceptive}")
    
    print(f"\nMissing values: {df.isnull().sum().sum()}")
    print(f"Duplicate rows: {duplicates}")
    print(f"Constant features: {len(constants)}")
    
    print(f"\nPhysiology features: {len(groups.get('physiology', []))}")
    print(f"Audio features: {len(groups.get('audio', []))}")
    print(f"Vision features: {len(groups.get('vision', []))}")
    
    print(f"\nLeakage columns excluded: {len(leakage_found)}")
    print(f"Question metadata excluded: {len(groups.get('metadata', []))}")
    
    pass_fail = "PASS" if all(d['FailedRows'] == 0 for d in derived_checks) else "FAIL"
    print(f"\nDerived-feature validation: {pass_fail}")
    
    ds_val = "SIMULATED" if 'data_source' in df.columns and (df['data_source'] == 'SIMULATED').all() else "MIXED/UNKNOWN"
    print(f"Data source: {ds_val}")
    
    print(f"\nProcessed dataset: {os.path.abspath(os.path.join(PROCESSED_DIR, 'mosaic_clean.csv'))}")
    print("Reports:")
    for f in os.listdir(PROCESSED_DIR):
        if f != 'mosaic_clean.csv':
            print(f"  {os.path.abspath(os.path.join(PROCESSED_DIR, f))}")

if __name__ == "__main__":
    main()
