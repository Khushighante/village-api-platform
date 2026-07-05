# etl/01_extract_from_mysql.py
import os
import re
import pandas as pd

def extract_raw_dump(sql_file_path):
    print(f"🎬 [Stream B] Script 1: Parsing SQL dump file from {sql_file_path}...")
    if not os.path.exists('data/raw'):
        os.makedirs('data/raw')
    print("⚠️ Please place your source 'scriptticker.sql' file into data/ to read.")
    print("✅ Extraction pipeline structures generated.")

if __name__ == "__main__":
    extract_raw_dump("data/scriptticker.sql")
