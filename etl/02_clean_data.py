import os
import pandas as pd
import numpy as np

def clean_raw_datasets(raw_dir, clean_dir):
    print("🧹 Initializing Data Transformation Engine...")
    
    if not os.path.exists(clean_dir):
        os.makedirs(clean_dir)
        
    # Check for core extracted tables
    available_files = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]
    print(f"📋 Found {len(available_files)} raw datasets ready for cleaning.")

    for file_name in available_files:
        raw_path = os.path.join(raw_dir, file_name)
        print(f"\n⚡ Processing: {file_name}")
        
        # Load the raw dataset
        df = pd.read_csv(raw_path)
        
        # 1. Standardize column names (lowercase, replace spaces/hyphens with underscores)
        df.columns = (df.columns.str.strip()
                      .str.lower()
                      .str.replace(r'[\s\-]+', '_', regex=True)
                      .str.replace(r'[^\w]', '', regex=True))
        
        # 2. Global string cleanup (strip whitespaces, handle empty string nulls)
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
            # Convert text-based null placeholders to real NumPy NaN values
            df[col] = df[col].replace(['None', 'NULL', 'nan', ''], np.nan)
            
        # 3. Specific table logic configurations
        if 'id' in df.columns:
            # Drop duplicates based on the primary key identifier if present
            initial_count = len(df)
            df = df.drop_duplicates(subset=['id'], keep='first')
            if len(df) < initial_count:
                print(f"   ✂️ Deduped: Removed {initial_count - len(df)} duplicate rows.")

        # Save pristine clean data
        clean_path = os.path.join(clean_dir, file_name)
        df.to_csv(clean_path, index=False)
        print(f"   ✅ Saved pristine dataset to: {clean_path}")

    print("\n🎉 All datasets successfully processed through the cleaning pipeline!")

if __name__ == "__main__":
    clean_raw_datasets("data/raw", "data/clean")