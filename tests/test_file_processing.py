import pytest
from pathlib import Path
from pm_agents.agents.file_processing_agents import FileConverterAgent, FileCleanupAgent
from pm_agents.exceptions import FileValidationError

def test_file_converter_init():
    converter = FileConverterAgent()
    assert converter.supported_formats == {'.mp3', '.wav', '.m4a', '.wma'}
    assert converter.max_file_size_bytes == 60 * 60 * 32000

def test_file_converter_validate_file(sample_audio_file):
    converter = FileConverterAgent()
    # Should not raise an exception
    converter.validate_file(sample_audio_file)

def test_file_converter_validate_file_not_found():
    converter = FileConverterAgent()
    with pytest.raises(FileValidationError):
        converter.validate_file(Path("nonexistent.mp3"))

def test_file_cleanup_remove_timestamps(sample_meeting_text):
    cleanup = FileCleanupAgent()
    cleaned = cleanup._remove_timestamps(sample_meeting_text)
    assert "00:00:00" not in cleaned
    assert "00:01:20" not in cleaned

def test_file_cleanup_remove_speaker_labels(sample_meeting_text):
    cleanup = FileCleanupAgent()
    cleaned = cleanup._remove_speaker_labels(sample_meeting_text)
    assert "John:" not in cleaned
    assert "Sarah:" not in cleaned
