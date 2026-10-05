import os 

def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if valid_target_dir == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if os.path.isdir(target_dir) == False:
        return f'Error: "{directory}" is not a directory'
    if os.path.isdir(target_dir) == True:
        strings = []
        print (f'Success: "{directory}" is within the working directory')
        for content in os.listdir(target_dir):
            fix_con = os.path.normpath(os.path.join(target_dir, content))
            strings.append(f'- {content}: file_size={os.path.getsize(fix_con)} bytes, is_dir={os.path.isdir(fix_con)}')
        return "\n".join(strings)

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}