from fastapi import Path, HTTPException, status
from src.schemas.space import RESERVED_SPACE_NAMES
from src.schemas.file import RESERVED_FILE_NAMES
from src.models.file import FileExtension

def validate_space_name(
    space_name: str = Path(
        min_length=1,
        max_length=100,
        pattern=r'^[a-zA-Z0-9_\- ]+$',
        description="The space name",
    )
) -> str:
    """Validate space name from query parameters"""
    if space_name in RESERVED_SPACE_NAMES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Space name '{space_name}' is reserved and cannot be used"
        )
    return space_name

def validate_file_name(
    file_name: str = Path(
        min_length=1,
        max_length=100,
        pattern=r'^[a-zA-Z0-9_\- ]+\.[a-zA-Z0-9]+$',  # allows name.extension format
        description="The file name",
    )
) -> str:
    """Validate file name from query parameters"""
    # check if base name is reserved
    base_name, extension = file_name.rsplit('.', 1)
    if base_name in RESERVED_FILE_NAMES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File name '{base_name}' is reserved and cannot be used"
        )

    # check if extension is valid
    try:
        FileExtension(extension)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension '{extension}'. Allowed extensions: {[e.value for e in FileExtension]}"
        )

    return file_name