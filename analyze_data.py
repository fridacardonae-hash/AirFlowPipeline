import os
import sqlite3
import pandas as pd 

def analyze_today():
    conn = sqlite3.connect("anomalies.db")
    
    query = """
    SELECT *
    FROM anomalies
    WHERE fecha = DATE('now')
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def analyze_metrics(df):
    total_ng = len(df)
    componentes = df.columns.tolist()
    componentes.remove("isn")
    componentes.remove("fecha")
    componentes.remove("overall")
    componentes.remove("maquina")
    
    ng_por_componente = {}
    for comp in componentes:
        ng_por_componente[comp] = (df[comp] == "NG").sum()
    
    return total_ng, ng_por_componente

def analyze_by_machine(df):
    result = df.groupby("maquina").apply(
        lambda x: (x["overall"]== "NG").sum()
    )
    return result