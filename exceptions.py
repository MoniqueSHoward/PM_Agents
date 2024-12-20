class RAIDBaseException(Exception):
    """Base exception class for RAID processing"""
    pass

class FileProcessingError(RAIDBaseException):
    """Exception raised for errors during file processing"""
    pass

class FileValidationError(RAIDBaseException):
    """Exception raised for validation errors"""
    pass

class FileSizeError(FileValidationError):
    """Exception raised when file size exceeds limits"""
    pass

class FileFormatError(FileValidationError):
    """Exception raised for unsupported file formats"""
    pass

class FileEncodingError(FileValidationError):
    """Exception raised for encoding issues"""
    pass

class WordCountError(FileValidationError):
    """Exception raised when text exceeds word limit"""
    pass

class RAIDProcessingError(RAIDBaseException):
    """Exception raised for errors during RAID analysis"""
    pass

class AgentConfigurationError(RAIDBaseException):
    """Exception raised for agent configuration errors"""
    pass

class ChunkProcessingError(RAIDBaseException):
    """Exception raised for errors during chunk processing"""
    def __init__(self, chunk_id: int, message: str):
        self.chunk_id = chunk_id
        self.message = message
        super().__init__(f"Error processing chunk {chunk_id}: {message}")

class ContextError(RAIDBaseException):
    """Exception raised for errors related to context handling"""
    pass

class DataConsistencyError(RAIDBaseException):
    """Exception raised for data consistency errors"""
    pass

class TranslationError(RAIDBaseException):
    """Exception raised for translation-related errors"""
    pass