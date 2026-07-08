import chromadb

from services.logger import logger


class ChromaStore:
    """
    Wrapper around ChromaDB.
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="data/chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="research_memory"
        )

        logger.info("ChromaDB initialized.")

    def add(
    self,
    document: str,
    metadata: dict,
    doc_id: str,
    ):

        """
        Store a document.
        """

        self.collection.add(
            documents=[document],
            metadatas=[metadata],
            ids=[doc_id],
        )
    
    def search(
        self,
        query: str,
        top_k: int = 3,
    ):
        """
        Retrieve similar documents.
        """

        return self.collection.query(
            query_texts=[query],
            n_results=top_k,
        )