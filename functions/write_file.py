import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if valid_target_dir == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_dir) == True:
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    os.makedirs(os.path.dirname(target_dir), exist_ok=True)

    with open(target_dir, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites files.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to list files from, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "String to be written"
                },
            },
            "required": ["file_path", "content"]
        },
    },
}