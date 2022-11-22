import csv, headers

def openFiles(fileName, type, db):
    with open(fileName, 'r', encoding='iso-8859-1') as file:
        if type == 0:
            header = headers.header_empresas
        elif type == 1:
            header = headers.header_estabelecimentos
        elif type == 2:
            header = headers.header_socios
        
        collections = ["empresas", "estabelecimentos", "socios"]
        reader = csv.DictReader(file, fieldnames=header, delimiter=';')

        ln = 0
        for line in reader:
            if ln == 100000:
                break
            ln += 1
            coll = db[collections[type]]
            print(line)
            coll.insert_one(line)