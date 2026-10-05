from subprocess import PIPE
import os, subprocess

def run_python_file(
        working_directory: str, file_path: str, args: list[str] | None = None
    ) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if args: command.extend(args)

        subr= subprocess.run(command, cwd=working_dir_abs, 
        stdout=PIPE, stderr=PIPE, text=True, timeout=30)
        if not subr.stdout and not subr.stderr:
            return "No output produced"
        else:
            output = []
            if subr.returncode != 0:
                output.append(f"Process exited with code {subr.returncode}")
            if subr.stdout:
                output.append(f"STDOUT:\n{subr.stdout}")
            if subr.stderr:
                output.append(f"STDERR:\n{subr.stderr}")
            return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes Python files with optional arguments.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to list files from, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional command-line arguments to pass to the script",
                    }
                },
            "required": ["file_path"]
            }
        },
    }

