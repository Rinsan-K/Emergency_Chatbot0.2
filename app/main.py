import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from transformers import pipeline
from pathlib import Path

# Initialize FastAPI app
app = FastAPI()

# Set up static file serving from the 'static' directory
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

# Load the model for generating embeddings
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
qa_pipeline = pipeline('text2text-generation', model='t5-large')

# Load the data and FAISS index
data = pd.read_csv(Path(__file__).parent / 'models/data.csv')
index = faiss.read_index(str(Path(__file__).parent / 'models/embeddings_index.faiss'))

# Serve the HTML home page
@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    html_path = Path(__file__).parent / "static/index.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text())
    return HTMLResponse("<h1>index.html not found</h1>", status_code=404)

@app.post("/query")
async def query(request: Request):
    body = await request.json()
    user_input = body.get("user_input")
    if not user_input:
        return {"response": "Please provide a valid query."}

    try:
        query_embedding = model.encode([user_input])
        D, I = index.search(query_embedding, k=5)
        
        if I.size == 0 or not I[0].size:
            return {"response": "No relevant documents found."}
        
        relevant_docs = data.iloc[I[0]]['Content'].tolist()
        context = " ".join(relevant_docs)
        
        response = qa_pipeline(f"User: {user_input} Context: {context}", max_length=100)
        return {"response": response[0]['generated_text']}
    except Exception as e:
        return {"response": f"An error occurred during processing: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
