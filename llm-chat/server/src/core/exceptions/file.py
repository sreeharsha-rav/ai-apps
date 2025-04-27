class FileError(Exception):
    """Base exception for file-related errors"""
    pass

class FileNotFoundError(FileError):
    """Raised when file is not found"""
    pass

class FileAlreadyExistsError(FileError):
    """Raised when file already exists"""
    pass

class FileValidationError(FileError):
    """Raised when file validation fails"""
    pass