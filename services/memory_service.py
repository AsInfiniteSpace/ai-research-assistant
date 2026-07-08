from vector_store.chroma_store import ChromaStore
from services.logger import logger
import uuid



class MemoryService:
    """
    Handles AI memory operations.
    """

    def __init__(self):
        self.store = ChromaStore()

        logger.info("MemoryService initialized.")

    def save(
    self,
    topic: str,
    content: str,
    ):
        """
        Save knowledge into memory.
        """

        self.store.add(
            document=content,
            metadata={
                "topic": topic,
            },
            doc_id=str(uuid.uuid4()),
        )
    
    def retrieve(
    self,
    query: str,
    top_k: int = 3,
    )-> list[str]:
        """
        Retrieve relevant memories.
        """

        logger.info(
            f"Searching memory for: {query}"
        )

        results = self.store.search(
            query=query,
            top_k=top_k,
        )

        documents = results.get("documents", [])

        if not documents:
            return []

        return documents[0]

    def has_memory(
    self,
    query: str,
    ) -> bool:
        """
        Determine whether relevant memory exists.
        """

        memories = self.retrieve(
            query=query,
            top_k=1,
        )

        return len(memories) > 0