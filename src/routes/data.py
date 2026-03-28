from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
from model import ResponseStatus
from .schema.data import ProcessDataRequest
import os
import aiofiles
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile = File(...),
    app_Settings: Settings = Depends(get_settings),
):
    data_controller = DataController()
    is_valid, response_status = data_controller.validate_file(file=file)
    
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": response_status.value
            }
        )

    project_dir = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filename(project_id=project_id, filename=file.filename)

    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(app_Settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": ResponseStatus.FILE_UPLOAD_FAILED.value,
                "error": str(e)
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": ResponseStatus.FILE_UPLOADED_SUCCESS.value, 
            "file_id": file_id,
        }
    )
        
@data_router.post("/process/{project_id}")
async def process_data(
    project_id: str,
    request: ProcessDataRequest,
):
    file_id = request.file_id
    chunk_size = request.chunk_size
    overlap_size = request.overlap_size

    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id) 
    file_content_chunks = process_controller.process_file_content(
        file_id=file_id, 
        file_content=file_content, 
        chunk_size=chunk_size, 
        overlap_size=overlap_size
    )

    if file_content_chunks is None or len(file_content_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": ResponseStatus.FILE_PROCESSING_FAILED.value
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": ResponseStatus.FILE_PROCESSING_SUCCESS.value,
            "file_content_chunks": [file_content_chunk.dict() for file_content_chunk in file_content_chunks]
        }
    )

