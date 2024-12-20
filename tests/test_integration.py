import pytest
from pathlib import Path
from datetime import datetime
from openai import OpenAI
import json

from pm_agents import RAIDOrchestrator
from pm_agents.agent_types import ProjectInfo, ProcessingResult, TextChunk
from pm_agents.exceptions import FileProcessingError

def test_end_to_end_processing(sample_audio_file, sample_project_info, output_dir):
    """Test complete processing pipeline with audio input"""
    orchestrator = RAIDOrchestrator(output_dir=output_dir)
    
    # Initialize OpenAI client
    client = OpenAI()
    orchestrator.base_llm_config["client"] = client
    
    try:
        results = orchestrator.process_file(sample_audio_file, sample_project_info)
        assert results.status == "completed"
        assert results.project_info == sample_project_info
        assert results.metadata is not None
        assert results.metadata.file_name == sample_audio_file.name
    except FileProcessingError as e:
        if "whisper" in str(e).lower():
            pytest.skip("Whisper model not available for testing")

def test_text_processing_flow(sample_meeting_text, sample_project_info, tmp_path, output_dir):
    """Test complete processing pipeline with text input"""
    # Create a text file with UTF-8 encoding
    text_file = tmp_path / "meeting.txt"
    text_file.write_text(sample_meeting_text, encoding='utf-8')
    
    orchestrator = RAIDOrchestrator(output_dir=output_dir)
    
    # Initialize OpenAI client
    client = OpenAI()
    orchestrator.base_llm_config["client"] = client
    
    # Mock the chunk processing to ensure proper TextChunk objects
    def mock_process_chunk(chunk_text: str) -> TextChunk:
        return TextChunk(
            id=1,
            content=chunk_text,
            preceding_context="",
            following_context="",
            start_position=0,
            end_position=len(chunk_text),
            word_count=len(chunk_text.split())
        )
    
    # Patch the parallel processor's create_chunks method
    orchestrator.parallel_processor.create_chunks = lambda text: [
        mock_process_chunk(text)
    ]
    
    results = orchestrator.process_file(text_file, sample_project_info)
    
    assert results.status == "completed"
    assert len(results.raid_entries) > 0
    
    # Verify RAID entries were correctly identified
    categories = [entry.category for entry in results.raid_entries]
    assert any(cat in categories for cat in ['R', 'A', 'I', 'D'])

def test_parallel_processing(sample_meeting_text, sample_project_info, tmp_path, output_dir):
    """Test parallel processing of large text"""
    # Create a larger text file by repeating the sample text
    large_text = sample_meeting_text * 5
    text_file = tmp_path / "large_meeting.txt"
    text_file.write_text(large_text, encoding='utf-8')
    
    orchestrator = RAIDOrchestrator(output_dir=output_dir)
    
    # Initialize OpenAI client
    client = OpenAI()
    orchestrator.base_llm_config["client"] = client
    
    # Mock chunk processing
    def mock_process_chunk(chunk_text: str, chunk_id: int) -> TextChunk:
        return TextChunk(
            id=chunk_id,
            content=chunk_text,
            preceding_context="",
            following_context="",
            start_position=chunk_id * 1000,  # Arbitrary position
            end_position=(chunk_id + 1) * 1000,
            word_count=len(chunk_text.split())
        )
    
    # Patch the parallel processor's create_chunks method
    orchestrator.parallel_processor.create_chunks = lambda text: [
        mock_process_chunk(text[i:i+1000], i//1000)
        for i in range(0, len(text), 1000)
    ]
    
    results = orchestrator.process_file(text_file, sample_project_info)
    
    assert results.status == "completed"
    assert len(results.raid_entries) > 0
    assert any(cat in [e.category for e in results.raid_entries] for cat in ['R', 'A', 'I', 'D'])

def test_output_generation(sample_meeting_text, sample_project_info, tmp_path, output_dir):
    """Test generation of all output files"""
    text_file = tmp_path / "meeting.txt"
    text_file.write_text(sample_meeting_text, encoding='utf-8')
    
    orchestrator = RAIDOrchestrator(output_dir=output_dir)
    
    # Initialize OpenAI client
    client = OpenAI()
    orchestrator.base_llm_config["client"] = client
    
    # Mock chunk processing
    orchestrator.parallel_processor.create_chunks = lambda text: [
        TextChunk(
            id=0,
            content=text,
            preceding_context="",
            following_context="",
            start_position=0,
            end_position=len(text),
            word_count=len(text.split())
        )
    ]
    
    results = orchestrator.process_file(text_file, sample_project_info)
    
    assert results.status == "completed"
    assert results.metadata.report_file is not None
    assert results.metadata.csv_file is not None
    assert results.metadata.json_file is not None
    
    # Verify files exist
    assert Path(results.metadata.report_file).exists()
    assert Path(results.metadata.csv_file).exists()
    assert Path(results.metadata.json_file).exists()