from fastapi import FastAPI
from typing import List, Dict, Optional

class BaseAPI:
    """Base API Class, define the public api"""
    def __init__(
        self,
        title: str,
        description: str,
        docs_url: str,
        redoc_url: str = None,
        openapi_tags: Optional[List[Dict[str, str]]] = None
    ):
        self.tags_metadata = openapi_tags or []
        self.app = FastAPI(
            docs_url=docs_url,
            redoc_url=redoc_url,
            title=title,
            description=description,
            openapi_tags=self.tags_metadata
        )

    def register_routers(self):
        """Register cluster (implemented by the subclass)"""
        raise NotImplementedError