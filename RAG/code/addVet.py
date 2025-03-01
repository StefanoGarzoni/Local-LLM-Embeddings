import ollama
import os
import glob
import pymssql

i=0
server = "dbIP"
database = "dbName" 
username = "username"
password = "password"
queryDoc = "INSERT INTO tblDocuments (Text) VALUES (%s);" 
queryVet= "INSERT INTO tblEmbeddings (Vector, IdDocument) VALUES (%s, %d);" 
queryIdu="SELECT MAX(IdDocument) FROM tblDocuments;"

def read_all_txt_files_in_folder(folder_path):
    documents = []
    txt_files_path = os.path.join(folder_path, '*.txt')
    txt_files = glob.glob(txt_files_path)

    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as file:
            content = file.read()
            documents.append(content)
    return documents

documents = read_all_txt_files_in_folder("path to the folder containing the files")

conn = pymssql.connect(server=server, user=username, password=password, database=database)
cursor = conn.cursor()

for doc in documents:
    i+=1
    try:
        cursor.execute(queryDoc,(str(doc)))
        conn.commit()
    
    except Exception as e:
        print(f"Error during query execution: {e}")
        conn.rollback()
        conn.close()

conn.close()

conn = pymssql.connect(server=server, user=username, password=password, database=database)
cursor = conn.cursor()
try:
    cursor.execute(queryIdu)
    row = cursor.fetchone()
    value = row[0]

except Exception as e:
    print(f"Error during query execution: {e}")
    value=1
    conn.rollback()

finally:
    conn.close()

value=value-i+1

embeddings = [ollama.embeddings(model='model', prompt=doc) for doc in documents]
vector_embeddings = [embedding['embedding'] for embedding in embeddings]

conn = pymssql.connect(server=server, user=username, password=password, database=database)
cursor = conn.cursor()
for vet in vector_embeddings:
    try:
        cursor.execute(queryVet,(str(vet), value))
        conn.commit()

    except Exception as e:
        print(f"Error during query execution: {e}")
        conn.rollback()
        conn.close()
    
    value+=1
conn.close()
