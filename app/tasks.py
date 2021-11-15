from ipdata import ipdata 
import socket 
from celery import Celery 

broker_url="pyamqp://guest:guest@rabbitmq:5672//"
#before docker
#backend_db = "db+mysql://root:pass123!@localhost:3306/users_tasks_database"

backend_db = "db+mysql://root:example@db:3306/test"
app = Celery('tasks', broker=broker_url)

@app.task 
def get_api_data(dest_ip):
    source_ip = socket.gethostbyname(socket.gethostname())
    ip_data = ipdata.IPData(source_ip)
    response = ip_data.lookup(dest_ip)
    return response 