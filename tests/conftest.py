# tests/conftest.py
import pytest
from pathlib import Path
from datetime import datetime
import json
import shutil
import nltk
import logging

from pm_agents.exceptions import FileValidationError
from pm_agents.agent_types import ProjectInfo, RAIDEntry, ProcessingResult, ProcessingMetadata


# Download NLTK data at the start of testing
def pytest_configure():
    """Download required NLTK data before running tests"""
    try:
        nltk.download('punkt_tab', quiet=True)
    except Exception as e:
        logging.warning(f"Failed to download NLTK data: {str(e)}. Some tests may fail.")

@pytest.fixture
def sample_audio_file(tmp_path):
    """Create a more realistic audio file fixture"""
    audio_file = tmp_path / "test_meeting.mp3"
    # Create a minimal valid MP3 file
    with open(audio_file, 'wb') as f:
        # MP3 file header
        f.write(b'\xFF\xFB\x90\x64\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    return audio_file

@pytest.fixture
def output_dir(tmp_path):
    """Create a temporary output directory"""
    output = tmp_path / "output"
    output.mkdir(exist_ok=True)
    return output

@pytest.fixture
def sample_project_info():
    return ProjectInfo(
        name="Test Project",
        summary="A test project for automated RAID analysis",
        id="TEST-001"
    )

@pytest.fixture
def sample_meeting_text():
    return """
    00:00:00 John: Hi everyone, can you hear me?
    
    00:00:05 Sarah: Yes, we can hear you. Let's discuss the project timeline.
    
    00:00:15 John: There's a risk that the third-party API integration might take longer than expected.
    We should plan for at least 2 extra weeks of buffer.
    
    00:00:30 Sarah: I agree. We're assuming the vendor will provide documentation by next Friday.
    
    00:00:45 John: Currently, we have an issue with the test environment. It's been unstable since yesterday.
    
    00:01:00 Sarah: Okay, I'll look into it. For now, we've decided to proceed with the cloud deployment approach.
    James will be responsible for the infrastructure setup, due by March 15th, 2024.
    
    00:01:15 John: Should we schedule another meeting?
    
    00:01:20 Sarah: Yes, let's meet next week. Um, does Tuesday work for everyone?
    """

@pytest.fixture
def sample_audio_file(tmp_path):
    # Create a dummy audio file
    audio_file = tmp_path / "test_meeting.mp3"
    audio_file.write_bytes(b"dummy audio content")
    return audio_file

@pytest.fixture
def sample_raid_entries():
    return [
        RAIDEntry(
            id="R-20240101000001",
            category="R",
            summary="API integration might take longer than expected",
            confidence_score=0.85,
            date_identified=datetime.now(),
            context="There's a risk that the third-party API integration might take longer than expected",
            solution="Plan for 2 extra weeks of buffer",
            owner=None,
            due_date=None
        ),
        RAIDEntry(
            id="A-20240101000002",
            category="A",
            summary="Vendor will provide documentation by next Friday",
            confidence_score=0.75,
            date_identified=datetime.now(),
            context="We're assuming the vendor will provide documentation by next Friday",
            solution=None,
            owner=None,
            due_date=None
        ),
        RAIDEntry(
            id="I-20240101000003",
            category="I",
            summary="Test environment is unstable",
            confidence_score=0.90,
            date_identified=datetime.now(),
            context="Currently, we have an issue with the test environment. It's been unstable since yesterday",
            solution=None,
            owner="Sarah",
            due_date=None
        ),
        RAIDEntry(
            id="D-20240101000004",
            category="D",
            summary="Proceed with cloud deployment approach",
            confidence_score=0.95,
            date_identified=datetime.now(),
            context="we've decided to proceed with the cloud deployment approach",
            solution=None,
            owner="James",
            due_date=datetime(2024, 3, 15)
        )
    ]

@pytest.fixture
def mock_file_converter(mocker):
    converter = mocker.Mock()
    converter.convert_audio_to_text.return_value = "Mocked transcription text"
    converter.needs_translation.return_value = False
    return converter

@pytest.fixture
def mock_llm_config():
    return {
        "model": "gpt-4o-mini",
        "temperature": 0.1,
        "api_key": "test-api-key"
    }