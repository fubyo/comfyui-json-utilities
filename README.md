# ComfyUI JSON Utilities

Custom utility nodes for ComfyUI to work with JSON files and objects.

## Features

- Load and save JSON files
- Parse and format JSON data
- Transform and manipulate JSON objects
- Integrate JSON workflows with ComfyUI pipelines

## Installation

1. Clone this repository into your ComfyUI custom_nodes directory:
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/yourusername/comfyui-json-utilities.git
   ```

2. Restart ComfyUI

**No additional dependencies required** - uses only Python standard library.

## Usage

### Load JSON

Loads a JSON file and returns its content as a string. Supports both direct file paths and file upload.

**Inputs:**
- `file_path` (STRING): Direct path to the JSON file (e.g., `/path/to/file.json`)
- `upload` (dropdown): Select uploaded JSON files from ComfyUI's input directory

**Outputs:**
- `json_string` (STRING): Raw JSON content as text

**Features:**
- **"Choose JSON to upload" button**: Opens file picker to upload JSON files to ComfyUI's input directory
- **Direct path input**: Type or paste a file path directly
- Uses UTF-8 encoding (default for JSON)
- Validates JSON syntax before outputting
- Throws exception on errors (file not found, invalid JSON, encoding issues)

**How to use:**

**Method 1: Upload via button**
1. Click "Choose JSON to upload" button
2. Select your JSON file from the file picker
3. File is uploaded to ComfyUI's input directory
4. Select the uploaded file from the `upload` dropdown
5. Node loads and validates the JSON

**Method 2: Direct path**
1. Enter the full path to your JSON file in `file_path`
2. Leave `upload` empty or unset
3. Node loads and validates the JSON

**Example:**
```
LoadJSON → json_string → [next node]
```

### Get JSON Item

Extracts an item from a JSON array at the specified index, or processes a JSON object/primitive. Converts nested objects/arrays to compact JSON strings.

**Inputs:**
- `json_string` (STRING): JSON string to process (output from Load JSON or any JSON string)
- `index` (INT): Index in the array (default: 0). Clamped to valid range [0, length-1]

**Outputs:**
- `json_dict` (DICT): Dictionary representation of the extracted item

**Features:**
- **Array handling**: Extracts item at specified index (clamped to valid range)
- **Non-array handling**: If input is not an array, processes the entire JSON value
- **Nested serialization**: Nested objects/arrays are converted to compact JSON strings
- **Primitive handling**: Primitives return as `{"value": primitive_value}`

**Behavior:**

| Input Type | Behavior |
|------------|----------|
| Array | Returns item at clamped index as dict |
| Object | Returns object as dict (nested values as JSON strings) |
| Primitive (string, number, bool, null) | Returns `{"value": primitive}` |

**Examples:**

**Example 1: Array input**
```json
Input: [{"name": "Alice"}, {"name": "Bob"}], index: 0
Output: {"name": "Alice"}
```

**Example 2: Object with nested array**
```json
Input: {"users": ["Alice", "Bob"], "count": 2}
Output: {"users": "[\"Alice\",\"Bob\"]", "count": 2}
```

**Example 3: Primitive value**
```json
Input: "hello world"
Output: {"value": "hello world"}
```

**Workflow Example:**
```
LoadJSON → json_string → GetJSONItem(index: 0) → json_dict → [next node]
```

## License

MIT License - see [LICENSE](LICENSE) file for details.
