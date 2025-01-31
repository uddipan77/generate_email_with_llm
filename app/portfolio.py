import pandas as pd
import chromadb
import uuid
import os
from pathlib import Path


class Portfolio:
    def __init__(self, file_path="resource/my_portfolio.csv"):
        script_dir = Path(__file__).parent.resolve()
        full_path = script_dir / file_path
        # Verify if the file exists
        if not full_path.is_file():
            raise FileNotFoundError(f"Portfolio CSV file not found at: {full_path}")
        
        self.file_path = full_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])