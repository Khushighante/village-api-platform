import os
import pandas as pd
from sqlalchemy import create_engine

def load_clean_data_to_sqlite(clean_dir):
    print("🚀 Initializing Local SQLite Database Engine...")
    
    # This creates a local file named 'nifty100.db' right in your project folder!
    # No passwords, no installations, no server configurations needed.
    db_file_path = "nifty100.db"
    connection_string = f"sqlite:///{db_file_path}"
    
    try:
        engine = create_engine(connection_string)
        print("🔌 Local SQL Engine configured successfully!")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return

    if not os.path.exists(clean_dir):
        print(f"❌ Error: Clean directory '{clean_dir}' does not exist.")
        return
        
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]
    
    for file_name in clean_files:
        table_name = file_name.replace('.csv', '')
        file_path = os.path.join(clean_dir, file_name)
        
        print(f"\n📤 Loading table '{table_name}' into SQL storage...")
        df = pd.read_csv(file_path)
        
        # Write the dataframe into local SQL tables
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        print(f"   ✅ Successfully loaded {len(df)} rows into table '{table_name}'.")

    print(f"\n🎉 Migration complete! All datasets are now saved inside the local database file: '{db_file_path}'")

if __name__ == "__main__":
    load_clean_data_to_sqlite("data/clean")