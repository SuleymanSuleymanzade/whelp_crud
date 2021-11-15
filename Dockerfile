FROM python:3.9

WORKDIR /myapp
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000 

#CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--reload"]
CMD ["python3", "./app/main.py"]

