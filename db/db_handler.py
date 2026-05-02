import os
import pandas as pd
import sqlite3
from datetime import datetime

def get_machine_from_path(path):
    parts = path.split("\\")
    if "logs" in parts:
        idx = parts.index("logs")
        if idx > 0:
            return parts[idx -1]
    return "UNKNOWN"
    

def update_db(isn_dict):
    conn = sqlite3.connect("anomalies.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS anomalies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isn TEXT,
        fecha TEXT,
        maquina TEXT,
        result1 TEXT,
        result2 TEXT,
        result3 TEXT,
        result4 TEXT,
        overall TEXT
    )
    """)
    
    for item in isn_dict:
        path = item["path"]
        date = item["date"]
        
        machine = get_machine_from_path(path)
        print("path", path)
        
        
        files = os.listdir(path)
        print("files", files)
        for file in files:
            if file.endswith(".csv"):
                print("log csv found")
                full_path = os.path.join(path, file)
                df = pd.read_csv(full_path)
                
                df["fecha"] = date
                df["maquina"] = machine
                
                df = df.rename(columns={
                    "ISN": "isn",
                    "Overall_res": "overall"
                })
                
                df= df[[
                    "isn", "fecha", "maquina",
                    "result1", "result2", "result3", "result4", "overall"
                ]]
                
                df = df.drop_duplicates(subset=["isn", "maquina", "fecha"])
                df.to_sql("anomalies", conn, if_exists="append", index=False)
    
    conn.close()
    print("Data recorded in the db")
                
                
                