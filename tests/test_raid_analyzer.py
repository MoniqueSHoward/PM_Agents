import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types import Choice

from agents.raid_analyzer_agent import RAIDAnalyzerAgent
from agent_types import ProjectInfo, RAIDEntry

@pytest.fixture
def mock_openai_response():
    """Create a mock OpenAI chat completion response"""
    return ChatCompletion(
        id="mock_id",
        model="gpt-4o-mini",
        object="chat.completion",
        created=int(datetime.now().timestamp()),
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(
                    content="""### ENTRY ###
Category: R
Summary: Risk of project delay due to resource constraints
Context: There's a significant risk that the project might be delayed due to resource constraints
Solution: None
Owner: None
Due Date: None
### ENTRY ###""",
                    role="assistant",
                )
            )
        ]
    )

@pytest.fixture
def mock_llm_config(mock_openai_response):
    """Create mock LLM configuration with OpenAI client"""
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    
    return {
        "model": "gpt-4o-mini",
        "temperature": 0.1,
        "client": mock_client
    }

@pytest.fixture
def sample_project_info():
    """Create sample project info for testing"""
    return ProjectInfo(
        name="Test Project",
        summary="A test project for automated RAID analysis",
        id="TEST-001"
    )

def test_analyze_chunk_with_risk(mock_llm_config, sample_project_info):
    """Test analyzing text containing a risk"""
    analyzer = RAIDAnalyzerAgent(mock_llm_config)
    text = "There's a significant risk that the project might be delayed due to resource constraints."
    entries = analyzer.analyze_chunk(text, sample_project_info)
    
    assert len(entries) > 0
    assert any(e.category == "R" for e in entries)
    assert any("delay" in e.summary.lower() for e in entries)

def test_analyze_chunk_with_assumption(mock_llm_config, mock_openai_response, sample_project_info):
    """Test analyzing text containing an assumption"""
    # Override mock response for this test
    mock_openai_response.choices[0].message.content = """### ENTRY ###
Category: A
Summary: Assumption about client data delivery
Context: We are definitely assuming the client will provide all required data by next week
Solution: None
Owner: None
Due Date: 2024-12-22
### ENTRY ###"""
    
    analyzer = RAIDAnalyzerAgent(mock_llm_config)
    text = "We are definitely assuming the client will provide all required data by next week."
    entries = analyzer.analyze_chunk(text, sample_project_info)
    
    assert len(entries) > 0
    assert any(e.category == "A" for e in entries)
    assert any("client" in e.summary.lower() for e in entries)

def test_analyze_chunk_with_issue(mock_llm_config, sample_project_info):
    """Test analyzing text containing an issue"""
    analyzer = RAIDAnalyzerAgent(mock_llm_config)
    text = "We currently have a critical issue with the database performance."
    entries = analyzer.analyze_chunk(text, sample_project_info)
    
    assert len(entries) > 0
    assert any(e.category == "I" for e in entries)
    assert any("database" in e.summary.lower() for e in entries)

def test_analyze_chunk_with_decision(mock_llm_config, sample_project_info):
    """Test analyzing text containing a decision"""
    analyzer = RAIDAnalyzerAgent(mock_llm_config)
    text = "We have definitely decided to use AWS for cloud hosting."
    entries = analyzer.analyze_chunk(text, sample_project_info)
    
    assert len(entries) > 0
    assert any(e.category == "D" for e in entries)
    assert any("aws" in e.summary.lower() for e in entries)

def test_analyze_chunk_with_multiple_entries(mock_llm_config, mock_openai_response, sample_project_info):
    """Test analyzing text containing multiple RAID entries"""
    # Override mock response for multiple entries
    mock_openai_response.choices[0].message.content = """### ENTRY ###
Category: R
Summary: Risk of budget overrun
Context: There's a serious risk of budget overrun
Solution: None
Owner: None
Due Date: None
### ENTRY ###
Category: A
Summary: Team size stability assumption
Context: We definitely assume the team size will remain stable
Solution: None
Owner: None
Due Date: None
### ENTRY ###
Category: I
Summary: Test environment issues
Context: Currently facing a critical issue with the test environment
Solution: None
Owner: None
Due Date: None
### ENTRY ###
Category: D
Summary: Decision on architecture
Context: We have absolutely decided to proceed with the microservices architecture
Solution: None
Owner: None
Due Date: None
### ENTRY ###"""
    
    analyzer = RAIDAnalyzerAgent(mock_llm_config)
    text = """
    There's a serious risk of budget overrun.
    We definitely assume the team size will remain stable.
    Currently facing a critical issue with the test environment.
    We have absolutely decided to proceed with the microservices architecture.
    """
    entries = analyzer.analyze_chunk(text, sample_project_info)
    
    categories = [e.category for e in entries]
    assert len(entries) >= 4
    assert "R" in categories
    assert "A" in categories
    assert "I" in categories
    assert "D" in categories

import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from openai.types.chat import ChatCompletion, ChatCompletionMessage

from agents.raid_analyzer_agent import RAIDAnalyzerAgent
from agent_types import ProjectInfo, RAIDEntry

@pytest.fixture
def mock_openai_response():
    """Create a mock OpenAI chat completion response"""
    return ChatCompletion(
        id="mock_id",
        model="gpt-4o-mini",
        object="chat.completion",
        created=int(datetime.now().timestamp()),
        choices=[{
            "finish_reason": "stop",
            "index": 0,
            "message": ChatCompletionMessage(
                content="""### ENTRY ###
Category: R
Summary: Risk of project delay due to resource constraints
Context: There's a significant risk that the project might be delayed due to resource constraints
Solution: None
Owner: None
Due Date: None
### ENTRY ###""",
                role="assistant",
            )
        }],
        usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150}
    )

@pytest.fixture
def mock_llm_config(mock_openai_response):
    """Create mock LLM configuration with OpenAI client"""
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    
    return {
        "model": "gpt-4o-mini",
        "temperature": 0.1,
        "client": mock_client
    }

@pytest.fixture
def sample_project_info():
    """Create sample project info for testing"""
    return ProjectInfo(
        name="Test Project",
        summary="A test project for automated RAID analysis",
        id="TEST-001"
    )

def test_analyze_chunk_with_risk(mock_llm_config, sample_project_info):
    """Test analyzing text containing a risk"""
    analyzer = RAIDAnalyzerAgent(mock_llm_config)
    text = "There's a significant risk that the project might be delayed due to resource constraints."
    entries = analyzer.analyze_chunk(text, sample_project_info)
    
    assert len(entries) > 0
    assert any(e.category == "R" for e in entries)
    assert any("delay" in e.summary.lower() for e in entries)

def test_analyze_chunk_with_assumption(mock_llm_config, mock_openai_response, sample_project_info):
    """Test analyzing text containing an assumption"""
    # Override mock response for this test
    mock_openai_response.choices[0]["message"].content = """### ENTRY ###
Category: A
Summary: Assumption about client data delivery
Context: We are definitely assuming the client will provide all required data by next week
Solution: None
Owner: None
Due Date: 2024-12-22
### ENTRY ###"""
    
    analyzer = RAIDAnalyzerAgent(mock_llm_config)
    text = "We are definitely assuming the client will provide all required data by next week."
    entries = analyzer.analyze_chunk(text, sample_project_info)
    
    assert len(entries) > 0
    assert any(e.category == "A" for e in entries)
    assert any("client" in e.summary.lower() for e in entries)

def test_analyze_chunk_with_issue(mock_llm_config, sample_project_info):
    """Test analyzing text containing an issue"""
    analyzer = RAIDAnalyzerAgent(mock_llm_config)
    text = "We currently have a critical issue with the database performance."
    entries = analyzer.analyze_chunk(text, sample_project_info)
    
    assert len(entries) > 0
    assert any(e.category == "I" for e in entries)
    assert any("database" in e.summary.lower() for e in entries)

def test_analyze_chunk_with_decision(mock_llm_config, sample_project_info):
    """Test analyzing text containing a decision"""
    analyzer = RAIDAnalyzerAgent(mock_llm_config)
    text = "We have definitely decided to use AWS for cloud hosting."
    entries = analyzer.analyze_chunk(text, sample_project_info)
    
    assert len(entries) > 0
    assert any(e.category == "D" for e in entries)
    assert any("aws" in e.summary.lower() for e in entries)

def test_analyze_chunk_with_multiple_entries(mock_llm_config, mock_openai_response, sample_project_info):
    """Test analyzing text containing multiple RAID entries"""
    # Override mock response for multiple entries
    mock_openai_response.choices[0]["message"].content = """### ENTRY ###
Category: R
Summary: Risk of budget overrun
Context: There's a serious risk of budget overrun
Solution: None
Owner: None
Due Date: None
### ENTRY ###
Category: A
Summary: Team size stability assumption
Context: We definitely assume the team size will remain stable
Solution: None
Owner: None
Due Date: None
### ENTRY ###
Category: I
Summary: Test environment issues
Context: Currently facing a critical issue with the test environment
Solution: None
Owner: None
Due Date: None
### ENTRY ###
Category: D
Summary: Decision on architecture
Context: We have absolutely decided to proceed with the microservices architecture
Solution: None
Owner: None
Due Date: None
### ENTRY ###"""
    
    analyzer = RAIDAnalyzerAgent(mock_llm_config)
    text = """
    There's a serious risk of budget overrun.
    We definitely assume the team size will remain stable.
    Currently facing a critical issue with the test environment.
    We have absolutely decided to proceed with the microservices architecture.
    """
    entries = analyzer.analyze_chunk(text, sample_project_info)
    
    categories = [e.category for e in entries]
    assert len(entries) >= 4
    assert "R" in categories
    assert "A" in categories
    assert "I" in categories
    assert "D" in categories

def test_confidence_scores(mock_llm_config, mock_openai_response, sample_project_info):
    """Test that confidence scores are properly calculated"""
    # Override mock response for confidence testing
    mock_openai_response.choices[0]["message"].content = """### ENTRY ###
Category: D
Summary: Decision on containerization with clear ownership and timeline
Context: We have definitely decided to use Docker for containerization. This decision is final and has been approved by all stakeholders. The implementation must be completed by March 15, 2024.
Solution: Immediate team training on Docker
Owner: John Smith
Due Date: 2024-03-15
### ENTRY ###"""
    
    analyzer = RAIDAnalyzerAgent(mock_llm_config)
    text = """
    We have definitely decided to use Docker for containerization.
    This decision is final and has been approved by all stakeholders.
    The implementation must be completed by March 15, 2024.
    """
    entries = analyzer.analyze_chunk(text, sample_project_info)
    
    assert len(entries) > 0
    assert all(0 <= e.confidence_score <= 1.0 for e in entries)
    assert any(e.confidence_score > 0.8 for e in entries), "Expected at least one high confidence score"

def test_low_confidence_scores(mock_llm_config, sample_project_info):
    """Test that uncertain language results in lower confidence scores"""
    analyzer = RAIDAnalyzerAgent(mock_llm_config)
    text = "We might possibly consider using containers at some point."
    entries = analyzer.analyze_chunk(text, sample_project_info)
    
    assert len(entries) > 0
    assert all(e.confidence_score <= 0.7 for e in entries), "Expected lower confidence scores for uncertain language"
def test_confidence_score_factors(mock_llm_config, sample_project_info):
    """Test different factors affecting confidence scores"""
    analyzer = RAIDAnalyzerAgent(mock_llm_config)
    high_confidence_text = """
    RISK: We definitely cannot meet the March 15th deadline due to critical resource constraints.
    Owner: John Smith
    Solution: Must immediately hire two senior developers.
    """
    entries = analyzer.analyze_chunk(high_confidence_text, sample_project_info)
    
    assert len(entries) > 0
    high_confidence_entry = max(entries, key=lambda e: e.confidence_score)
    assert high_confidence_entry.confidence_score > 0.8, (
        "Expected high confidence due to strong language, specific date, "
        "named owner, and solution"
    )
