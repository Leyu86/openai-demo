from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class Organization(BaseModel):
    entity_id: Optional[str] = None
    name: Optional[str] = None
    country: Optional[str] = None
    logo: Optional[str] = None
    is_startup: Optional[bool] = None
    is_unicorn: Optional[bool] = None


class DocumentMetadata(BaseModel):
    news_id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[str] = None
    organization: List[Optional[Organization]] = None


class DocumentChunkMetadata(DocumentMetadata):
    document_id: Optional[str] = None


class DocumentChunk(BaseModel):
    id: Optional[str] = None
    text: str
    metadata: DocumentChunkMetadata
    embedding: Optional[List[float]] = None


class DocumentChunkWithScore(DocumentChunk):
    score: float


class Document(BaseModel):
    id: Optional[str] = None
    text: str
    metadata: Optional[DocumentMetadata] = None


class DocumentWithChunks(Document):
    chunks: List[DocumentChunk]


class DocumentMetadataFilter(BaseModel):
    document_id: Optional[str] = None
    source_id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    organization_name: Optional[str] = None
    start_date: Optional[str] = None  # any date string format
    end_date: Optional[str] = None  # any date string format


class Query(BaseModel):
    query: str
    filter: Optional[DocumentMetadataFilter] = None
    top_k: Optional[int] = 3


class QueryWithEmbedding(Query):
    embedding: List[float]


class QueryResult(BaseModel):
    query: str
    results: List[DocumentChunkWithScore]


