from .BaseController import BaseController
from .ProjectController import ProjectController
from model import ResponseStatus
import re
import os

class DataController(BaseController):

    # Initialize the DataController with any necessary attributes or configurations
    def __init__(self):
        super().__init__()

    def validate_file(self, file):
        # Implement file validation logic here
        if file.content_type not in self.app_Settings.FILE_ALLOWED_EXTENSIONS:
            return False, ResponseStatus.FILE_TYPE_NOT_ALLOWED
        if file.size > self.app_Settings.FILE_MAX_SIZE_MB * 1024 * 1024:
            return False, ResponseStatus.FILE_SIZE_EXCEEDED
        return True, ResponseStatus.FILE_VALIDATION_SUCCESS
    
    def generate_unique_filename(self, project_id: str, filename: str):
        random_string = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)  # Ensure project directory exists
        clean_filename = self.get_clean_filename(filename = filename)
        new_filepath = os.path.join(project_path, f"{random_string}_{clean_filename}")

        while os.path.exists(new_filepath):
            random_string = self.generate_random_string()
            new_filepath = os.path.join(project_path, f"{random_string}_{clean_filename}")
        
        return new_filepath

    def get_clean_filename(self, filename: str):
        # Remove any special characters from the filename to ensure it's safe for storage
        clean_file_name = re.sub(r'[^\w.]', '', filename)
        # Replace spaces with underscores
        cleaned_file_name = clean_file_name.replace(" ", "_")  
        return cleaned_file_name

    def process_file(self, file):
        # Implement file processing logic here
        pass