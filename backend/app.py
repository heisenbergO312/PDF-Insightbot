from dotenv import load_dotenv, find_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
import os
import openai
import sys
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
from typing import Optional

sys.path.append("../..")

_ = load_dotenv(find_dotenv())

openai.api_key = os.environ["OPENAI_API_KEY"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Updated PostgreSQL configuration
POSTGRES_USER = os.getenv("POSTGRES_USER", "your_username")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "your_password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "your_database")

CONNECTION_STRING = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

COLLECTION_NAME = "document_collection"

class ChatRequest(BaseModel):
    query: str
    file_path: str

@app.post('/upload')
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if file.filename != '':
            target_directory = "./docs"
            os.makedirs(target_directory, exist_ok=True)
            unique_filename = str(uuid.uuid4()) + ".pdf"
            file_path = os.path.join(target_directory, unique_filename)

            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)

            return JSONResponse({
                "message": "PDF file uploaded and saved successfully",
                "original_filename": file.filename,
                "file_path": file_path
            })
        else:
            raise HTTPException(status_code=400, detail="No file selected")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/chat')
async def chat(request: ChatRequest):
    try:
        query = request.query
        uploaded_file_path = request.file_path

        print(f"Query: {query}")
        print(uploaded_file_path)

        if uploaded_file_path:
            print(f"Using PDF from: {uploaded_file_path}")
            loader = PyPDFLoader(uploaded_file_path)
            pages = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(pages)

            embeddings = OpenAIEmbeddings()

            try:
                # Updated PGVector initialization
                vectordb = PGVector.from_documents(
                    embedding=embeddings,
                    documents=splits,
                    collection_name=COLLECTION_NAME,
                    connection_string=CONNECTION_STRING
                )

            except Exception as e:
                print(f"Error creating vector database: {e}")
                raise HTTPException(status_code=500, detail=f"Error creating vector database: {str(e)}")

            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )

            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)
            retriever = vectordb.as_retriever()

            try:
                qa_chain = RetrievalQA.from_chain_type(
                    llm,
                    retriever=retriever,
                    memory=memory
                )

                result = qa_chain({"query": query})
                answer = result.get("result")
                print(answer)

                conversation_chain = ConversationalRetrievalChain.from_llm(
                    llm,
                    retriever=retriever,
                    memory=memory
                )

                conversation_result = conversation_chain({"question": query})
                conversation_answer = conversation_result["answer"]

                return JSONResponse({
                    "result": answer,
                    "conversation_result": conversation_answer
                })
            except Exception as e:
                print(f"Error in QA chain: {e}")
                raise HTTPException(status_code=500, detail=f"Error in QA chain: {str(e)}")
        else:
            raise HTTPException(status_code=400, detail="No PDF file path provided in the request")

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
