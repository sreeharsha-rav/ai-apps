from fastapi import Query, HTTPException, status
from src.schemas.space import RESERVED_SPACE_NAMES

def validate_space_name(
    space_name: str = Query(
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