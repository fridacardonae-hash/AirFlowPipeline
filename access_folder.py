import os
import json
from datetime import datetime, timedelta
import subprocess

'''def connect_network(user, password):
    try:
        subprocess.run(
            ["net", "use", "\\\\10.232.4.39\\pmxbushare", "/delete"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULLd:
        )
        result = subprocess.run(
            [
                "net", "use",
                "\\\\10.232.4.39\\pmxbushare",
                f"/user:{user}",
                password
            ],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print("Error conectando al servidor")
            print(result.stderr)
        else:
            print("Conectado a servidor correctamente")
    except Exception as e:
        print("Error", e)'''
                


def get_isn_today(path):

    isn_list = []
    today_date = datetime.now().date()
    yesterday_date = today_date - timedelta(days=1)
    print("today", today_date)
    
    for isn in os.listdir(path):
        isn_path = os.path.join(path,isn)
        print("isn_path",isn_path)
        creation_date = datetime.fromtimestamp(os.path.getmtime(isn_path)).date()
        print("creation", creation_date)
        if creation_date == yesterday_date:
            isn_list.append({
                "date": creation_date,
                "path": isn_path
                
            })
    
    return isn_list
        
    