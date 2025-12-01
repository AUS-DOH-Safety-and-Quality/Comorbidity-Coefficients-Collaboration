import pandas as pd
import json
import os

def process_dataset(input_path, output_path, weights):
    print(f"Processing {input_path}...")
    if not os.path.exists(input_path):
        print(f"Error: File {input_path} not found.")
        return

    df = pd.read_csv(input_path)
    
    # Filter weights to only those columns present in df
    valid_weights = {k: v for k, v in weights.items() if k in df.columns}
    
    # Check if any weights were missed
    missed_weights = set(weights.keys()) - set(valid_weights.keys())
    if missed_weights:
        print(f"Warning: The following weight columns were not found in {input_path}: {missed_weights}")
    
    # Calculate score
    # Create a dataframe of just the weighted columns
    if valid_weights:
        weighted_df = df[list(valid_weights.keys())].mul(pd.Series(valid_weights))
        df['score'] = weighted_df.sum(axis=1)
    else:
        print("Warning: No matching columns found for weights. Score will be 0.")
        df['score'] = 0
    
    print(f"Saving to {output_path}...")
    df.to_csv(output_path, index=False)

def main():
    # Load weights
    try:
        with open("original_weights.json", "r") as f:
            all_weights = json.load(f)
    except FileNotFoundError:
        print("Error: original_weights.json not found.")
        return
    
    elix_weights = all_weights['elixhauser']
    charlson_weights = all_weights['charlson']
    
    datasets_dir = "datasets"
    
    # Elixhauser files
    process_dataset(
        os.path.join(datasets_dir, "elixhauser_training.csv"),
        os.path.join(datasets_dir, "elixhauser_training_scored.csv"),
        elix_weights
    )
    process_dataset(
        os.path.join(datasets_dir, "elixhauser_testing.csv"),
        os.path.join(datasets_dir, "elixhauser_testing_scored.csv"),
        elix_weights
    )
    
    # Charlson files
    process_dataset(
        os.path.join(datasets_dir, "charlson_training.csv"),
        os.path.join(datasets_dir, "charlson_training_scored.csv"),
        charlson_weights
    )
    process_dataset(
        os.path.join(datasets_dir, "charlson_testing.csv"),
        os.path.join(datasets_dir, "charlson_testing_scored.csv"),
        charlson_weights
    )

if __name__ == "__main__":
    main()
