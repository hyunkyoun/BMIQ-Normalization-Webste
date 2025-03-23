import pandas as pd
import os

# === STEP 1: Load Sample Info ===
sample_info_path = "info/sample.xlsx"  # <-- Update path if needed
sample_info = pd.read_excel(sample_info_path, sheet_name='Mu EPIC Sample Info dChip')

# Keep only Sample ID and Experiment columns
sample_info = sample_info[['Sample ID', 'Experiment']].dropna()
sample_info['Sample ID'] = sample_info['Sample ID'].astype(str)
sample_info = sample_info[sample_info['Experiment'].isin([1, 2, 3, 4, 5, 6])]

# === STEP 2: Load Beta Matrix ===
beta_matrix_path = "info/beta.xlsx"  # <-- Replace with your actual file
beta_df = pd.read_excel(beta_matrix_path)

# === STEP 3: Prepare Output Directory ===
output_dir = "pca_ready_outputs"
os.makedirs(output_dir, exist_ok=True)

# === STEP 4: Process Each Experiment ===
for exp in range(1, 7):
    sample_ids = sample_info[sample_info['Experiment'] == exp]['Sample ID'].tolist()
    matched_sample_ids = [col for col in beta_df.columns if str(col) in sample_ids]

    # Skip if no matching sample columns
    if not matched_sample_ids:
        print(f"⚠️ No matching samples found for Experiment {exp}")
        continue

    # Filter relevant columns
    cols_to_keep = ['TargetID concat'] + matched_sample_ids
    filtered_df = beta_df[cols_to_keep]

    # Transpose: CpGs become columns, Samples become rows
    transposed_df = filtered_df.set_index('TargetID concat').T
    transposed_df.index.name = 'Sample ID'
    transposed_df.reset_index(inplace=True)

    # File paths
    excel_path = os.path.join(output_dir, f"experiment_{exp}_PCA_ready.xlsx")
    txt_path = os.path.join(output_dir, f"experiment_{exp}_PCA_ready.txt")

    # Save TXT (always)
    transposed_df.to_csv(txt_path, sep='\t', index=False)
    print(f"✅ Saved TXT: {txt_path}")

    # Save Excel only if column count is within Excel's limit
    if transposed_df.shape[1] <= 16384:
        transposed_df.to_excel(excel_path, index=False)
        print(f"✅ Saved Excel: {excel_path}")
    else:
        print(f"⚠️ Skipped Excel for Experiment {exp} — too many columns ({transposed_df.shape[1]})")