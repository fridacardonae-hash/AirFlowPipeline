import json
from access_folder import get_isn_today, connect_network
from db.db_handler import update_db
from analyze_data import analyze_today, analyze_metrics, analyze_by_machine



with open ("config.json", "r") as f:
    config = json.load(f)
    
user = config["user"]
password = config["password"]
connect_network(user, password)


path = config["path_logs"]
#print("path", path)

isns = get_isn_today(path)
print("isns", isns)

update_db(isns)

df = analyze_today()

total_ng, ng_por_componente = analyze_metrics(df)
ng_bymachine = analyze_by_machine(df)

print("Total ng", total_ng)
print("ng por componente", ng_por_componente)
print("ng por maquina:\n", ng_bymachine)