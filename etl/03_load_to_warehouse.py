# etl/03_load_to_warehouse.py
from sqlalchemy import create_engine
import pandas as pd

def load_star_schema():
    print("🎬 [Stream B] Script 3: Connecting to PostgreSQL Data Warehouse...")
    print("📌 Loading strategy: Dimension tables first -> Fact tables second (Idempotent Upserts).")

if __name__ == "__main__":
    load_star_schema()
