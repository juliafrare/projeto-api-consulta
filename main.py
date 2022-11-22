from pymongo import MongoClient
from openfiles import openFiles
from decouple import config

API_USER = config('USER')
API_PASSWORD = config('PASSWORD')

client = MongoClient(f"mongodb+srv://{API_USER}:{API_PASSWORD}@cluster0.zhnesp4.mongodb.net/?retryWrites=true&w=majority")
db = client.test

files = ['csv/Empresas0.csv', 'csv/Estabelecimentos0.csv', 'csv/Socios0.csv']            
for i, f in enumerate(files):
    openFiles(f, i, db)