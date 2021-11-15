from fastapi import FastAPI, APIRouter, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import uvicorn
from pathlib import Path 
from typing import Optional 
from pydantic import BaseModel 
from auth import Auth
from tasks import get_api_data
from models import User, Task # peewee models 

class RegisterModel(BaseModel):
    firstname: str
    lastname: str
    phone: str
    email: str #username 
    password_: str

class AuthenticationModel(BaseModel):
    email: str
    password_: str 

class ApiTaskModel(BaseModel):
    dest_ip: str 

security = HTTPBearer()
auth_handler = Auth()

app = FastAPI()
api_router = APIRouter()

@app.get("/", status_code=200)
async def home():
    return {"Data": "Testing"}

@app.post("/api/v1/auth")
async def authentication(user_details: AuthenticationModel):
    query = User.select().where(User.email == user_details.email)
    if not query.exists():
        return HTTPException(status_code=401, detail='Invalid username')
    if not (auth_handler.verify_password(user_details.password_, query.get().password_)):
        return HTTPException(status_code=401, detail='Invalid password')
    token = auth_handler.encode_token({'email': query.get().email, 'password_': query.get().password_})
    return {'token': token}


@app.post("/api/v1/signup")
async def signup(user_details: RegisterModel):
    print(user_details)
    query = User.select().where(User.email == user_details.email)
    if query.exists():
        return {'error':'account already exist'}
    try:
        hashed_password = auth_handler.encode_password(user_details.password_)
        person = User(
            firstname = user_details.firstname,
            lastname = user_details.lastname,
            phone = user_details.phone,
            email = user_details.email,
            password_ = hashed_password        
        )
        
        person.save() # add to DB
        return {'email': user_details.email, 'password_': hashed_password}
    except:
        error_msg = 'Failed to signup user'
        return {'error': error_msg}


@app.post("api/v1/refresh")
async def refresh(credentials: HTTPAuthorizationCredentials = Security(security)):
    expired_token = credentials.credentials
    return auth_handler.refresh_token(expired_token)


@app.get("/api/v1/user")
async def user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials 
    if(auth_handler.decode_token(token)):
        user_email = auth_handler.decode_token(token)["email"]
        query = User.select().where(User.email == user_email)
        if query.exists():
            firstname = query.get().firstname 
            lastname = query.get().lastname 
            email = query.get().email
            phone = query.get().phone 

            return {
                'firstname': firstname,
                'lastname': lastname,
                'phone': phone,
                'email': email
            }
        else:
            return {'error': 'no_user_exist'}
    else:
        return {'error': 'token_expired'}
                  

@app.post("/api/v1/task")
async def create_task(api_addresses: ApiTaskModel, credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        get_task = get_api_data.delay(api_addresses.dest_ip) # celery async 
        resp = get_task.get()
        assert(resp != None)
    except AssertionError as err:
        return {'err': "can't fetch data"}
    token = credentials.credentials 
    if (auth_handler.decode_token(token)):
        user_email = auth_handler.decode_token(token)['email'] 
        user_id = User.select().where(User.email == user_email).get().id # for foreign key 
        task_query = Task(task=resp, user_id=user_id)
        task_query.save()
        return resp
    else:
        return {'error': 'no authorised user'}   


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(f"{Path(__file__).stem}:app", port=8000, host="0.0.0.0", reload=True)
