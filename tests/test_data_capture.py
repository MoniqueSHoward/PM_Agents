import pytest
from pathlib import Path
from datetime import datetime
import json
from agents.data_capture_agent import DataCaptureAgent, ReportGeneratorAgent
from agent_types import ProcessingResult, ProcessingMetadata, ProjectInfo, RAIDEntry
from exceptions import DataConsistencyError

def test_data_capture_basic(sample_raid_entries, sample_project_info):
    """Test basic data capture functionality"""
    capture = DataCaptureAgent()
    result = ProcessingResult(
        status="completed",
        project_info=sample_project_info,
        raid_entries=sample_raid_entries,
        metadata=ProcessingMetadata(
            start_time=datetime.now(),
            file_name="test.txt"
        )
    )
    
    captured_data = capture.capture_processing_data(result)
    
    assert captured_data is not None
    assert len(captured_data["raid_entries"]) == len(sample_raid_entries)
    assert captured_data["processing_info"]["project_name"] == sample_project_info.name

def test_data_capture_statistics(sample_raid_entries, sample_project_info):
    """Test statistics calculation in data capture"""
    capture = DataCaptureAgent()
    result = ProcessingResult(
        status="completed",
        project_info=sample_project_info,
        raid_entries=sample_raid_entries,
        metadata=ProcessingMetadata(
            start_time=datetime.now()
        )
    )
    
    captured_data = capture.capture_processing_data(result)
    
    stats = captured_data["statistics"]
    assert stats["total_entries"] == len(sample_raid_entries)
    assert all(cat in stats["category_counts"] for cat in ['R', 'A', 'I', 'D'])
    assert isinstance(stats["average_confidence"], float)
    assert 0 <= stats["average_confidence"] <= 1.0

def test_report_generator_markdown(tmp_path, sample_raid_entries, sample_project_info):
    """Test markdown report generation"""
    generator = ReportGeneratorAgent(output_dir=tmp_path)
    
    captured_data = {
        "processing_info": {
            "timestamp": datetime.now().isoformat(),
            "file_name": "test.txt",
            "project_name": sample_project_info.name,
            "project_summary": sample_project_info.summary
        },
        "raid_entries": [entry.__dict__ for entry in sample_raid_entries],
        "statistics": {
            "total_entries": len(sample_raid_entries),
            "category_counts": {"R": 1, "A": 1, "I": 1, "D": 1},
            "average_confidence": 0.86
        }
    }
    
    report_file = generator.generate_analysis_report(captured_data, sample_project_info)
    
    assert Path(report_file).exists()
    content = Path(report_file).read_text()
    assert "# RAID Analysis Report" in content
    assert sample_project_info.name in content

def test_report_generator_csv(tmp_path, sample_raid_entries, sample_project_info):
    """Test CSV export generation"""
    generator = ReportGeneratorAgent(output_dir=tmp_path)
    
    captured_data = {
        "processing_info": {
            "timestamp": datetime.now().isoformat(),
            "file_name": "test.txt",
            "project_name": sample_project_info.name
        },
        "raid_entries": [entry.__dict__ for entry in sample_raid_entries],
        "statistics": {
            "total_entries": len(sample_raid_entries),
            "category_counts": {"R": 1, "A": 1, "I": 1, "D": 1},
            "average_confidence": 0.86
        }
    }
    
    csv_file = generator.generate_csv_export(captured_data)
    
    assert Path(csv_file).exists()
    # Could add pandas read_csv and verify contents if needed

def test_data_capture_validation():
    """Test validation of required fields"""
    capture = DataCaptureAgent()
    
    # Create an invalid RAID entry missing required fields
    invalid_entry = RAIDEntry(
        id="TEST-001",
        category="R",
        summary="Test entry",
        confidence_score=None,  # Missing required field
        date_identified=datetime.now(),
        context=None  # Missing required field
    )
    
    result = ProcessingResult(
        status="completed",
        project_info=ProjectInfo(name="Test", summary="Test project"),
        raid_entries=[invalid_entry],
        metadata=ProcessingMetadata(start_time=datetime.now())
    )
    
    with pytest.raises(DataConsistencyError):
        capture.capture_processing_data(result)
