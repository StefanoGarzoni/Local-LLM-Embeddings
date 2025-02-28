from sklearn.metrics.pairwise import cosine_similarity
import ollama
import pymssql
import ast

i=1
question=1
vet=[]
chat=[]
server = "192.168.7.226\\SQLEXPRESS"
database = "LlmMail"
username = "stefano"
password = "Fenix123!"
queryDownloadVet="SELECT Vett FROM tblEmb;"
queryDownloadDoc="SELECT Testo FROM tblDocumenti;"

def download_vet(server, username, password, database, query):
  conn = pymssql.connect(server=server, user=username, password=password, database=database)
  cursor = conn.cursor()
  try:
      cursor.execute(query)
      row = cursor.fetchall()
    
  except Exception as e:
      print(f"Errore durante l'esecuzione della query: {e}")
      conn.rollback()

  finally:
      conn.close()
  return row

def download_doc(server, username, password, database, query):
  conn = pymssql.connect(server=server, user=username, password=password, database=database)
  cursor = conn.cursor()
  try:
      cursor.execute(query)
      row = cursor.fetchall()
    
  except Exception as e:
      print(f"Errore durante l'esecuzione della query: {e}")
      conn.rollback()

  finally:
      conn.close()
  return row

#model='mxbai-embed-large'
def retrieve_documents(question, vector_embeddings, top_k=2):
    question_embedding = ollama.embeddings(model='llamaemb', prompt=question)['embedding']
    similarities = cosine_similarity([question_embedding], vector_embeddings)
    sorted_indices = similarities.argsort()[0][::-1][:top_k]
    return sorted_indices

def generate_context( documents, relevant_indices):
    context = " ".join([documents[idx] for idx in relevant_indices])
    return context

def clean_and_eval_string(string_repr):
    cleaned_string = string_repr.strip().replace('}', ']')
    try:
        return ast.literal_eval(cleaned_string)
    except (SyntaxError, ValueError):
        print(f"Errore nella valutazione della stringa: {cleaned_string}")
        return []

def create_vect(vetStr):
  vet = []
  for vec in vetStr:
      string_repr = vec[0]
      result = clean_and_eval_string(string_repr)
      vet.append(result)
  return vet

def clean_document(documents):
    doc = [tup[0] for tup in documents]
    return doc

def generate_question(question, context, type):
    if type==1:
        full_prompt = f"Usando questi dati : {context}\nRispondi a questa domanda: {question}"
        #full_prompt = f"Domanda: {question}\Contesto: {context}"
    else:
        full_prompt=f"Usando le conversazioni precedenti come contesto e questi dati: {context}, rispondi a questa domanda: {question}"
    return full_prompt

def generate_chat(text, chat, role):
    chat.append({'role': role, 'content': text})
    return chat


vetStr = download_vet(server, username, password, database, queryDownloadVet)
documents = download_doc(server, username, password, database, queryDownloadDoc)
vet=create_vect(vetStr)
documents=clean_document(documents)

print("1 per cambiare chat | 0 per terminare")
while question != "0" :
    j=1
    print("\nCHAT "+str(i))
    question=input("\nDomanda: ")

    while question != "1" and question != "0":
        response=""

        if j==1:
            relevant_indices = retrieve_documents(question, vet)
            print(relevant_indices)
            context=generate_context(documents, relevant_indices)
            full_question=generate_question(question, context, 1)
        else:
            full_question=generate_question(question, context, 0)

        chat=generate_chat(full_question, chat, 'user')
        
        stream = ollama.chat(
        model='fenix',
        messages=chat,
        stream=True,
        )
        print("\nRisposta: ")

        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
            response+=chunk['message']['content']

        chat=generate_chat(response, chat, 'assistant')
        question=input("\nDomanda: ")
        j+=1

    i+=1
   
