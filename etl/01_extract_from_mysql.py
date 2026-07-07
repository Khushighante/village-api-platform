import os
import pandas as pd

def migrate_excel_to_raw_csv(source_dir, output_dir):
    print("🔄 Starting Excel data migration to raw CSV layer...")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List of files we need to convert to CSV format
    target_files = [
        'companies.xlsx', 'analysis.xlsx', 'balancesheet.xlsx', 
        'profitandloss.xlsx', 'cashflow.xlsx', 'prosandcons.xlsx', 
        'documents.xlsx', 'sectors.xlsx', 'peer_groups.xlsx', 
        'market_cap.xlsx', 'financial_ratios.xlsx', 'stock_prices.xlsx'
    ]

    for file_name in target_files:
        source_path = os.path.join(source_dir, file_name)
        
        if os.path.exists(source_path):
            print(f"🔍 Reading {file_name}...")
            # Read the excel sheet
            df = pd.read_excel(source_path)
            
            # Create standard CSV name (e.g., companies.csv)
            csv_name = file_name.replace('.xlsx', '.csv')
            output_path = os.path.join(output_dir, csv_name)
            
            # Save it down to data/raw/
            df.to_csv(output_path, index=False)
            print(f"✅ Success! Saved {len(df)} rows to {output_path}\n")
        else:
            print(f"⚠️ Warning: Optional/missing file skipped: {file_name}")

if __name__ == "__main__":
    # Since your Excel files are right in your root directory:
    migrate_excel_to_raw_csv(".", "data/raw")