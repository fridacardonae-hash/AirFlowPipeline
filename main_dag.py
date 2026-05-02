from airflow import DAG 
from airflow.operators.python import PythonOperator
from datetime import datetime 
import json
from access_folder import get_isn_today, connect_network
from db.db_handler import update_db
from analyze_data import analyze_today, analyze_metrics, analyze_by_machine


def flow():
    print("Starting process")
    with open ("config.json", "r") as f:
        config = json.load(f)
    
    user = config["user"]
    password = config["password"]
    connect_network(user, password)


    path = config["path_logs"]
    #print("path", path)

    isns = get_isn_today(path)
    
    update_db(isns)

    df = analyze_today()

    total_ng, ng_por_componente = analyze_metrics(df)
    ng_bymachine = analyze_by_machine(df)

    print("Total ng", total_ng)
    print("ng por componente", ng_por_componente)
    print("ng por maquina:\n", ng_bymachine)
    
with DAG(
    "test_analysis",
    start_date = datetime(2026,4,22),
    schedule= "@daily",
    catchup= False
) as dag:
    
    t1=PythonOperator(
        task_id="saludo",
        python_callable = flow
    )