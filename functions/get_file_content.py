import os 
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:  
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if os.path.isfile(target_file):
            f'Error: File not found or is not a regular file: "{file_path}"'
            
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS) 
            if f.read(1):
                file_content_string += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string

    except Exception as e:
        return f'Error: error while getting file content ->  {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return content of specified file by the file_path parameter",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"]
    ),
    
)