from elasticsearch import Elasticsearch
from pymongo import MongoClient
from os import getenv
import csv

def openFiles(fileName, type, db, es):
    with open(fileName, 'r', encoding='iso-8859-1') as file:        
        collections = ["empresas", "estabelecimentos", "socios"]
        reader = csv.DictReader(file, delimiter=';')

        ln = 0
        for line in reader:
            if ln == 100000:
                break
            ln += 1
            es.index(
                index=collections[type],
                document=line
            )

client = MongoClient(host=getenv('MONGODB_HOSTNAME'), port=27017, username=getenv('MONGODB_USERNAME'), password=getenv('MONGODB_PASSWORD'))
db = client.searchapp
es = Elasticsearch(getenv('ELASTIC_HOST'))

files = ['csv/Empresas0.csv', 'csv/Estabelecimentos0.csv', 'csv/Socios0.csv']            
for i, f in enumerate(files):
    openFiles(f, i, db, es)