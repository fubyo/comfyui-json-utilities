import json
import os
import folder_paths


def convert_to_dict(value):
    """Convert a JSON value to a dict with nested objects/arrays as strings."""
    if isinstance(value, dict):
        result = {}
        for key, val in value.items():
            if isinstance(val, (dict, list)):
                result[key] = json.dumps(val, separators=(',', ':'))
            else:
                result[key] = val
        return result
    elif isinstance(value, list):
        return {"value": json.dumps(value, separators=(',', ':'))}
    else:
        return {"value": value}


class LoadJSON:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = []
        if os.path.exists(input_dir):
            for f in os.listdir(input_dir):
                if os.path.isfile(os.path.join(input_dir, f)):
                    file_parts = f.split('.')
                    if len(file_parts) > 1 and file_parts[-1].lower() == 'json':
                        files.append(f)
        
        return {
            "required": {
                "file_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "upload": (sorted(files), {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_string",)
    FUNCTION = "load"
    CATEGORY = "JSON"

    def load(self, file_path, upload=""):
        # Use uploaded file if selected
        if upload and upload != "":
            file_path = folder_paths.get_annotated_filepath(upload)
        
        if not file_path or not file_path.strip():
            raise ValueError("No file path provided")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text_content = f.read()
        except UnicodeDecodeError:
            raise ValueError(f"Failed to decode file with UTF-8 encoding: {file_path}")

        try:
            json.loads(text_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file: {file_path}. Error: {str(e)}")

        return (text_content,)

    @classmethod
    def VALIDATE_INPUTS(s, file_path, upload=""):
        if upload and upload != "":
            if not folder_paths.exists_annotated_filepath(upload):
                return f"Invalid uploaded file: {upload}"
        elif file_path and os.path.exists(file_path):
            return True
        else:
            return "No valid file path provided"
        return True


class GetJSONItem:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json_string": ("STRING", {"default": ""}),
                "index": ("INT", {"default": 0, "min": -999999, "max": 999999}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("json_dict",)
    FUNCTION = "get_item"
    CATEGORY = "JSON"

    def get_item(self, json_string, index):
        if not json_string or not json_string.strip():
            raise ValueError("No JSON string provided")

        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {str(e)}")

        if isinstance(data, list):
            if len(data) == 0:
                raise ValueError("JSON array is empty")
            
            clamped_index = max(0, min(index, len(data) - 1))
            item = data[clamped_index]
        else:
            item = data

        return (convert_to_dict(item),)


NODE_CLASS_MAPPINGS = {
    "LoadJSON": LoadJSON,
    "GetJSONItem": GetJSONItem,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadJSON": "Load JSON",
    "GetJSONItem": "Get JSON Item",
}
