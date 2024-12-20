from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

@dataclass 
class TextChunk:
    """Represents a chunk of text with context"""
    id: int
    content: str
    preceding_context: str
    following_context: str
    start_position: int
    end_position: int
    word_count: int

@dataclass
class ChunkGroup:
    """Represents a group of related text chunks"""
    id: int
    chunks: List[TextChunk]
    total_words: int
    context_overlap: str
    start_position: int
    end_position: int
    metadata: Dict

@dataclass
class ProjectInfo:
    """Project information structure"""
    name: str
    summary: str
    id: Optional[str] = None

@dataclass
class FileInfo:
    """Information about a processed file"""
    path: Path
    format: str
    word_count: Optional[int] = None
    duration: Optional[float] = None  # For audio files, in seconds
    encoding: Optional[str] = None
    size_bytes: int = 0

@dataclass
class RAIDEntry:
    """Structure for a RAID (Risk, Assumption, Issue, Decision) entry"""
    id: str
    category: str  # 'R', 'A', 'I', or 'D'
    summary: str
    confidence_score: float
    date_identified: datetime
    context: str  # Original text context
    solution: Optional[str] = None
    owner: Optional[str] = None
    due_date: Optional[datetime] = None
    file_info: Optional[FileInfo] = None  # Added file source information

@dataclass
class ProcessingMetadata:
    """Metadata for processing operations"""
    start_time: datetime
    end_time: Optional[datetime] = None
    file_info: Optional[FileInfo] = None
    processing_steps: List[Dict[str, str]] = None
    total_entries: Optional[int] = None
    category_counts: Optional[Dict[str, int]] = None
    average_confidence: Optional[float] = None
    error_type: Optional[str] = None
    error_details: Optional[Dict[str, str]] = None

@dataclass
class ProcessingResult:
    """Structure for processing results"""
    status: str  # 'processing', 'completed', 'error'
    project_info: ProjectInfo
    clean_text: Optional[str] = None
    raid_entries: List[RAIDEntry] = None
    metadata: ProcessingMetadata = None
    error: Optional[str] = None

@dataclass
class AgentConfig:
    """Configuration for an AutoGen agent"""
    name: str
    llm_config: Dict
    system_message: str
    max_retries: int = 3
    timeout: int = 300
    supported_formats: Optional[Set[str]] = None  # Added format support info