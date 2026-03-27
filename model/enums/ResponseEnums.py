from enum import Enum

class ResponseStatus(Enum):

    FILE_TYPE_NOT_ALLOWED = "File type not allowed."
    FILE_SIZE_EXCEEDED = "File size exceeded."
    FILE_VALIDATION_SUCCESS = "File validation successful."
    FILE_VALIDATION_FAILED = "File validation failed."
    FILE_UPLOADED_FAILED = "File upload failed."
    FILE_UPLOADED_SUCCESS = "File uploaded successfully."
