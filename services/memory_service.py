from vector_store.chroma_store import ChromaStore
from services.logger import logger
from agents.writer.models import ResearchReport

import uuid
import json


SIMILARITY_THRESHOLD = 0.30


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
        report: ResearchReport,
    ):
        """
        Save a research report into memory.
        """

        self.store.add(
            document=report.model_dump_json(),
            metadata={
                "topic": topic,
            },
            doc_id=str(uuid.uuid4()),
        )

        logger.info(f"Report saved for topic: {topic}")

    def retrieve(
        self,
        query: str,
        top_k: int = 1,
    ) -> ResearchReport | None:
        """
        Retrieve a relevant report from memory.
        """

        logger.info(
            f"Searching memory for: {query}"
        )

        results = self.store.search(
            query=query,
            top_k=top_k,
        )

        documents = results.get("documents", [])
        distances = results.get("distances", [])

        if not documents or not distances:
            logger.info("Memory miss.")
            return None

        # Chroma returns nested lists
        best_document = documents[0][0]
        best_distance = distances[0][0]

        logger.info(
            f"Best memory distance: {best_distance:.4f}"
        )

        if best_distance > SIMILARITY_THRESHOLD:
            logger.info(
                "No sufficiently similar memory found."
            )
            return None

        logger.info("Memory hit.")

        data = json.loads(best_document)

        return ResearchReport(**data)

    def has_memory(
        self,
        query: str,
    ) -> bool:
        """
        Determine whether relevant memory exists.
        """

        return self.retrieve(query) is not None