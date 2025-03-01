# Local-LLM-Embeddings
Local LLM Embeddings extracts text and images from PDF, generates embeddings locally, stores them in SQL, and uses an LLM to answer questions. It retrieves context using cosine similarity for effective prompt engineering, ensuring privacy and performance without relying on the cloud.

------------------

🔍 Introduction  
Local LLM Embeddings is a project that enables:

Extracting text and images from documents  
Generating vector embeddings locally  
Storing data in an SQL database  
Performing searches based on cosine similarity  
Obtaining contextualized answers from a language model  
The entire process runs locally, with no data sent to external servers, ensuring complete privacy and control.  

------------------

🛠️ Features

✔ Data Extraction – Reads text and images from documents (PDF, images, etc.)

✔ Embedding Generation – Creates vector representations of text

✔ SQL Database – Stores embeddings in a structured manner

✔ Vector Search – Finds the most relevant contexts using cosine similarity

✔ Chat with LLM – Improves responses through embedding-based prompt engineering

------------------

⚙️ How It Works?

1️⃣ Text and Image Extraction  
Two scripts analyze documents in various formats, extract text and images, and pre-process them for embedding generation.

2️⃣ Embedding Creation  
Embeddings are generated locally by an LLM, converting text into numerical vectors. These vectors capture meaning and semantic relationships between words.

3️⃣ Storage in SQL Database  
Another script normalizes and stores the embeddings in an SQL database, making them easily accessible for future searches.

4️⃣ Vector Search and Cosine Similarity  
When a user asks a question in the chat, an embedding of the query is generated and compared with stored embeddings using cosine similarity. This identifies the most relevant content.

5️⃣ Prompt Engineering and Model Response  
The retrieved context is included in the prompt sent to the LLM, enhancing the quality of the generated response. This approach optimizes answer accuracy without external searches.

------------------

🔒 Benefits

✅ Fully Local – No risk of data loss or cloud dependency

✅ Increased Privacy – No sensitive document sharing

✅ More Relevant Results – Thanks to vector search and prompt engineering

------------------

NOTE:  
- This code can only be used and tested via CLI, if you are interested in a GUI interface that integrates these features and many others that can be used for your company, contact me privately

- This is a project that aims to lay the foundations of testing to create an embeddings system for local PDF documents. There are many applicable improvements and cases that can differentiate the result of the code. Contact me if you want to know more.

------------------
📧 Contact  
For questions or contributions, open an Issue or contact me on GitHub! 🚀
