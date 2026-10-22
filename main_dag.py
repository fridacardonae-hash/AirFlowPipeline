from airflow import DAG 
from airflow.operators.python import PythonOperator
from datetime import datetime 
import json
from MeshDetection.access_folder import get_isn_today
from MeshDetection.db.db_handler import update_db
from MeshDetection.analyze_data import analyze_today, analyze_metrics, analyze_by_machine
import os 


def flow():
    print("Starting process")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(BASE_DIR, "config.json")
    with open (config_path, "r") as f:
        config = json.load(f)


    path = "/networklogs"
    print("path", path)

    isns = get_isn_today(path)
    print("isns", isns)
    
    update_db(isns)

    df = analyze_today()

    total_ng, ng_por_componente = analyze_metrics(df)
    ng_bymachine = analyze_by_machine(df)


    print("Total ng", total_ng)
    print("ng por componente", ng_por_componente) 
    print("ng por maquina:\n", ng_bymachine)
    
with DAG(
    "test_analysis",
    start_date = datetime(2026,5,9),
    schedule= "@daily",
    catchup= False
) as dag:
    
    t1=PythonOperator(
        task_id="process",
        python_callable = flow
    )