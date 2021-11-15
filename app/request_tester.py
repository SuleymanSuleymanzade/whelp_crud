import requests 
from models import User

data = {
    'name': 'suleyman',
    'lastname': 'suleymanzade',
    'phone':'55512345',
    'email':'suleyman.suleymanzade@gmail.com',
    'password': '54322345'
}



resp = requests.post('http://127.0.0.1:8000/api/v1/signup',data=data)
print(resp)