import os, subprocess
from subprocess import PIPE 
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if target_dir[-3:] != '.py':
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", os.path.abspath(target_dir)]

        if args:
            command.extend(args)


        completed_process = subprocess.run(
            command, 
            cwd=working_dir_abs,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )

        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}\n"
        output = ""
        if completed_process.stdout:
            output += "STDOUT: " + completed_process.stdout + "\n"
        elif completed_process.stderr:
            output += "STDERR: " + completed_process.stderr + "\n"
        else:
            return 'No output produced\n'

        return output
        


    except Exception as e:
        return f'Error: error while running python file ->  {e}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run specified file by the file_path parameter",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,   
                items=types.Schema(      
                    type=types.Type.STRING
                ),
                description="List of arguments that you can use to run a file"
            ),
        },
        required=["file_path"]
    ),
)