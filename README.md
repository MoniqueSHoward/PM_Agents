# PM Sidekick

Project management automation agents using AutoGen framework. This package provides automated analysis of meeting recordings and transcripts to identify risks, assumptions, issues, and decisions (RAID).

## Project Overview
This project implements a RAID (Risks, Assumptions, Issues, Decisions) analysis system using the AutoGen framework. It processes meeting recordings and transcripts to automatically identify and categorize project management artifacts. The system uses parallel processing and AI agents to analyze content while maintaining context and providing confidence scores for each identified item.

## Problem Being Solved
[https://github.com/MoniqueSHoward/PM_Agents/issues/1#issue-2752072969](https://private-user-images.githubusercontent.com/54523934/397643633-0ee662f7-aba5-4349-bb1d-8369751cbcfa.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzQ2Nzc5NzQsIm5iZiI6MTczNDY3NzY3NCwicGF0aCI6Ii81NDUyMzkzNC8zOTc2NDM2MzMtMGVlNjYyZjctYWJhNS00MzQ5LWJiMWQtODM2OTc1MWNiY2ZhLm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjIwVDA2NTQzNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTE3ZTgyMWVjZTg5NDI2MDgyZTcyN2Y0NDIzMDYwZjI0ZTMzMWZlZmVlYWJhNDE5OGQ0NTRlZWY4Mzk5NTUwZmUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.pq5Bt1SZ2KJ_658QMo5nKCg9Yb1HCmKOVdf_zmrA-tg)

## Our Solution
https://private-user-images.githubusercontent.com/54523934/397646852-b373ddb2-0919-42f5-8f98-65ae75127857.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzQ2Nzg3OTIsIm5iZiI6MTczNDY3ODQ5MiwicGF0aCI6Ii81NDUyMzkzNC8zOTc2NDY4NTItYjM3M2RkYjItMDkxOS00MmY1LThmOTgtNjVhZTc1MTI3ODU3Lm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjIwVDA3MDgxMlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWNmN2I4ZWIyZmMzOWE3MGQxZDlkNGE0MWRhMGZkNjU5M2Y4MTY1ZDY2OTNmYTIyZWFkYWE1NGNhNjk0MzljZjkmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.aN_JxSK5VqhpqmZIxq-0JSQg1OggOkIxESUwrapx5_4

## The Impact
https://private-user-images.githubusercontent.com/54523934/397649765-7ab52c93-b3e7-463f-ba19-d911c982e7c8.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzQ2Nzk1MTUsIm5iZiI6MTczNDY3OTIxNSwicGF0aCI6Ii81NDUyMzkzNC8zOTc2NDk3NjUtN2FiNTJjOTMtYjNlNy00NjNmLWJhMTktZDkxMWM5ODJlN2M4Lm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjIwVDA3MjAxNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTFjNWRiNDEyNTY1YmI4Nzk3NzRkNWUzNjM0YTQwMDVhYjVlMzkzMGY4OWI2ZmFjYjQ4NDRlNjAyZGE2MzkzZWQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.UDSPXzfEAkqH9CNVfZkXD1Kj9MpIbVEIYldougarQTk

## AutoGen Framework 
https://private-user-images.githubusercontent.com/54523934/397652995-99dca5ee-d7ff-48f7-b01e-f2c8e50388fc.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzQ2ODAzMDEsIm5iZiI6MTczNDY4MDAwMSwicGF0aCI6Ii81NDUyMzkzNC8zOTc2NTI5OTUtOTlkY2E1ZWUtZDdmZi00OGY3LWIwMWUtZjJjOGU1MDM4OGZjLm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjIwVDA3MzMyMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWFiZGI1YjA3YjNjYWRiOTY1Y2RiNzAxMjQ2YjVkYmE2Yjk4MjU5N2IxYmE3NWNhM2EzNTViZDFlOWU3OGJlYzgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.YEj87T4Io2wMC5skAkJNqEJ4I27nvwnxCanRar4al7E

## Screen Demo
https://private-user-images.githubusercontent.com/54523934/397647883-cc3c2e39-f8e0-4806-8886-03c5b946b48f.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzQ2NzkwNzEsIm5iZiI6MTczNDY3ODc3MSwicGF0aCI6Ii81NDUyMzkzNC8zOTc2NDc4ODMtY2MzYzJlMzktZjhlMC00ODA2LTg4ODYtMDNjNWI5NDZiNDhmLm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjIwVDA3MTI1MVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTdkMWI0NDdmYTY4N2RhMTA5YjMwNGY3NzUyMzNhYWUxZGJiZmRiZGZkYzg3OTRkZjE3NzkyM2I5MzBmN2Q3MzMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.dVzJlX0StEYBLW6CvTZ8dfKe0rAFe-fp-bYf2sNxcJg

## VS Code Demo
https://private-user-images.githubusercontent.com/54523934/397653900-587920ed-9e6f-4b6a-917d-d74e71ef26fc.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzQ2ODA1MTUsIm5iZiI6MTczNDY4MDIxNSwicGF0aCI6Ii81NDUyMzkzNC8zOTc2NTM5MDAtNTg3OTIwZWQtOWU2Zi00YjZhLTkxN2QtZDc0ZTcxZWYyNmZjLm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjIwVDA3MzY1NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTM0NWI4ZmFmN2QzNzhmODJiZjJhMGJkMTkwMDI1MmMzZDk1MjA3MjYxMmUyNDU0ZDJkZjE4YmJhY2IyZTUwZjcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.iGFoYQ4KQh3t9dWEg1BqZb1-vK4aFuY6oF4VTlfpU-U

## Features

- **Enhanced File Processing**: 
  - Audio formats: .mp3, .wav, .m4a, .wma (max 60 minutes)
  - Text formats: .txt, .md, .doc, .docx (max 10,000 words)
  - UTF-8 encoding validation
  - Automatic format detection and conversion

- **Automated RAID Analysis**:
  - Risks: Potential future problems or uncertainties
  - Assumptions: Facts taken as true without proof
  - Issues: Current problems or challenges
  - Decisions: Confirmed choices or determinations

- **Advanced Text Processing**:
  - Parallel chunk processing
  - Context preservation
  - Intelligent text segmentation

- **Multi-language Support**: 
  - Automatic language detection
  - Translation to English

- **Intelligent Analysis**:
  - Confidence scoring for each RAID entry
  - Context preservation during analysis
  - Owner and due date extraction
  - Solution/mitigation tracking

- **Report Generation**:
  - Markdown analysis reports
  - CSV exports for database integration
  - JSON data exports
  - Customizable output formats

- **Comprehensive Validation**:
  - File format validation
  - Size limit enforcement
  - Encoding verification
  - Word count checks

- **Error Handling**:
  - Comprehensive error tracking
  - File validation safeguards
  - Processing metadata capture

## System Requirements

- Python 3.8 or higher
- Memory: Sufficient for parallel processing (recommended 4GB+)
- Storage: Space for audio files and generated reports
- Network: Internet connection for OpenAI API access
- pip package manager
- OpenAI API key

## Architecture

The system consists of several specialized agents:
- **GroupChatManager**: Orchestrates all agent interactions
- **FileConverterAgent**: Handles file conversion and translation
- **FileCleanupAgent**: Preprocesses and cleans text
- **ChunkProcessingAgent**: Manages text segmentation
- **RAIDAnalyzerAgent**: Performs RAID analysis
- **DataCaptureAgent**: Captures and processes results
- **ReportGeneratorAgent**: Generates output reports

## Installation

### Installing from source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pm_agents.git
cd pm_agents
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

For development installation with additional tools:
```bash
pip install -e ".[dev]"
```

## Configuration

1. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_api_key_here  # Required for GPT and Whisper
```

## Core Dependencies

- pyautogen>=0.2.0: AutoGen framework for agent orchestration
- openai-whisper>=20231117: Audio transcription
- nltk>=3.8.1: Natural language processing
- openai>=1.0.0: GPT integration
- python-docx>=0.8.11: Word document processing
- langdetect>=1.0.0: Language detection
- pandas>=2.0.0: Data processing
- psutil>=5.9.0: System resource management
- python-dotenv>=1.0.0: Environment management
- numpy>=1.24.0: Numerical operations

## Usage

Basic usage example:

```python
from pm_agents import RAIDOrchestrator, ProjectInfo
from pathlib import Path

# Initialize the orchestrator
orchestrator = RAIDOrchestrator()

# Define project information
project_info = ProjectInfo(
    name="My Project",
    summary="A sample project for demonstration"
)

# Process a file
file_path = Path("path/to/your/meeting/transcript.txt")
results = orchestrator.process_file(file_path, project_info)

# Access the results
for entry in results.raid_entries:
    print(f"Category: {entry.category}")
    print(f"Summary: {entry.summary}")
    print(f"Confidence: {entry.confidence_score}")
```

## File Support

### Audio Files
- Supported formats: .mp3, .wav, .m4a, .wma
- Maximum duration: 60 minutes
- Automatically converted to text using OpenAI Whisper

### Text Files
- Supported formats: .txt, .md, .doc, .docx
- Maximum word count: 10,000 words
- Must be UTF-8 encoded

## Output Formats

The system generates multiple output formats:
1. **Markdown Reports**: Detailed analysis with categorized entries
2. **CSV Export**: Database-ready format with all RAID entries
3. **JSON Export**: Complete data export including metadata
4. **Processing Metadata**: Details about the analysis process

## Web App Screens

https://github.com/MoniqueSHoward/PM_Agents/blob/main/Screen%20Images/Analyze%20Section.png

## Error Handling

The system includes comprehensive error handling for:
- File validation errors
- Processing errors
- Data consistency errors
- Translation errors
- Memory management
- Chunk processing errors

Errors are logged and can be tracked in the processing metadata.

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking
- flake8 for code linting

To format code:
```bash
black pm_agents/
isort pm_agents/
```

## Limitations

- Audio files limited to 60 minutes duration
- Text files limited to 10,000 words
- English language output (with automatic translation)
- Requires active internet connection for OpenAI services

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using [AutoGen](https://github.com/microsoft/autogen)
- Uses OpenAI's Whisper for audio transcription
- Special thanks to contributors and maintainers

## Support

For support, please open an issue in the GitHub repository.
