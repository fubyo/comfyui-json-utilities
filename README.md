# ComfyUI JSON Utilities

Custom utility nodes for ComfyUI to work with JSON files and objects.

## Features

**Available Nodes:**
- **Load JSON**: Load JSON files from disk with file upload button or direct path input
- **Get JSON Item**: Extract items from JSON arrays by index, with nested object/array serialization
- **Get Dict Value**: Extract typed values (string, int, float) from dictionaries by key

**Key Capabilities:**
- Upload JSON files via browser file picker
- Auto-detect UTF-8 encoding and validate JSON syntax
- Extract array items with index clamping to valid range
- Convert nested objects/arrays to compact JSON strings
- Type-aware value extraction with automatic conversion
- Handle booleans, numbers, strings, null, and missing keys appropriately

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

### Get Dict Value

Extracts a value from a dictionary by key and outputs it as string, int, and float. Handles different data types appropriately.

**Inputs:**
- `json_dict` (DICT): Dictionary to extract value from (output from Get JSON Item)
- `key` (STRING): Key to extract from the dictionary

**Outputs:**
- `string_value` (STRING): String representation of the value
- `int_value` (INT): Integer representation of the value
- `float_value` (FLOAT): Float representation of the value

**Features:**
- **Type-aware extraction**: Automatically converts values to appropriate types
- **Boolean handling**: Converts to "true"/"false", 1/0, 1.0/0.0
- **Number handling**: Converts to string, int (rounded), and float
- **Null handling**: Returns "null", 0, 0.0
- **Missing key**: Returns "", 0, 0.0 (no exception)
- **Nested JSON strings**: Treated as regular strings

**Behavior:**

| Value Type | string_value | int_value | float_value |
|------------|--------------|-----------|-------------|
| String | The string | 0 | 0.0 |
| Number | String representation | Rounded int | Float value |
| Boolean | "true"/"false" | 1/0 | 1.0/0.0 |
| Null | "null" | 0 | 0.0 |
| Missing key | "" | 0 | 0.0 |

**Examples:**

**Example 1: String value**
```
Input dict: {"name": "Alice", "height": 1.65}
Key: "name"
Output: "Alice", 0, 0.0
```

**Example 2: Number value**
```
Input dict: {"name": "Alice", "height": 1.65}
Key: "height"
Output: "1.65", 1, 1.65
```

**Example 3: Boolean value**
```
Input dict: {"active": true, "count": 5}
Key: "active"
Output: "true", 1, 1.0
```

**Example 4: Missing key**
```
Input dict: {"name": "Alice"}
Key: "age"
Output: "", 0, 0.0
```

**Workflow Example:**
```
LoadJSON → json_string → GetJSONItem(index: 0) → json_dict → GetDictValue(key: "height") → float_value → [next node]
```

## License

MIT License - see [LICENSE](LICENSE) file for details.
