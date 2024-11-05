import os
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Load the model for generating embeddings
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Set the path to the CSV file
data_path = Path(__file__).parent / 'data/emergency_childbirth_preparedness.csv'

# Check if the file exists
if not data_path.is_file():
    raise FileNotFoundError(f"The data file was not found at {data_path}")

# Load the data
data = pd.read_csv(data_path)

# Ensure the 'Content' column exists
if 'Content' not in data.columns:
    raise KeyError("The column 'Content' does not exist in the data.")

# Generate embeddings for the 'Content' column
embeddings = model.encode(data['Content'].tolist())

# Create a FAISS index for the embeddings
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Set the path to save the index and processed data
output_dir = Path(__file__).parent / 'models'
output_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

# Save the FAISS index
faiss.write_index(index, str(output_dir / 'embeddings_index.faiss'))

# Save the data to a CSV file in the models directory
data.to_csv(output_dir / 'data.csv', index=False)

print("Embeddings and index saved successfully.")
