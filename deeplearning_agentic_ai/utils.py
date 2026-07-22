import base64
from pathlib import Path


def encode_image_b64(image_path: str) -> tuple[str, str]:
    """Return (media_type, base64_string) for an image."""
    ext = Path(image_path).suffix.lower()
    media_type = f"image/{ext.lstrip('.')}" if ext else "image/png"
    with open(image_path, "rb") as image_file:
        return media_type, base64.b64encode(image_file.read()).decode('utf-8')
