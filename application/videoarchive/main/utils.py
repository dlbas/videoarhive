from django.http import HttpResponseBadRequest
from django.conf import settings
from uuid import uuid4

from .exceptions import FileTooBig, WrongContentType


def generate_filename(suffix: str = ".raw") -> str:
    return str(uuid4()) + suffix


def validate_file(file):
    if file.content_type not in settings.VALID_CONTENT_TYPES:
        raise WrongContentType(
            f"""file is of wrong content type {file.content_type},
            allowed content types: {', '.join(settings.VALID_CONTENT_TYPES)}""",
        )

    if file.size > settings.MAX_FILE_SIZE:
        raise FileTooBig(
            f"file size {file.size} is greater than allowed {str(settings.MAX_FILE_SIZE)}"
        )
