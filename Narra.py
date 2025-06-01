from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from openai import OpenAI
import json
import re
import time

# Initialize OpenAI client (will use OPENAI_API_KEY from environment)
client = OpenAI()

# Define paths and API key
BASE_DRIVE_PATH = '.'  # Current directory

class DriveStorageManager:
    def __init__(self, base_drive_path):
        self.base_drive_path = base_drive_path

    def save_to_drive(self, label, data):
        # Modify the label to ensure correct naming
        if label.endswith("_schema"):
            label = label.replace("_schema", "_content")
        else:
            label += "_content"

        file_path = os.path.join(self.base_drive_path, "content", f"{label}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f)

    def read_from_drive(self, label, folder="content"):
        # Correct the filename based on the folder
        extension = "json" if folder == "content" else "txt"
        file_path = os.path.join(self.base_drive_path, folder, f"{label}.{extension}")

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        else:
            return None


class SchemaManager:
    def __init__(self, base_drive_path):
        self.base_drive_path = base_drive_path
        self.schemas = {}

    def get_schema(self, label):
        if label not in self.schemas:
            self.load_schema(label)
        return self.schemas[label]

    def load_schema(self, label):
        content, metadata = self.read_schema(label)
        self.schemas[label] = {"definition": content, **metadata}

    def read_schema(self, label):
        file_path = os.path.join(self.base_drive_path, "schemas", f"{label}.txt")
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Parse metadata lines
        metadata = {}
        is_metadata_section = False  # Initially, we're not in the metadata section
        while lines:
            line = lines.pop(0).strip()
            print(f"Processing line: '{line}'")  # Print each line being processed

            # Detect start of metadata section
            if line == "# Metadata":
                is_metadata_section = True
                continue  # Skip this line and proceed to next

            # Process metadata lines while in the metadata section
            if is_metadata_section:
                if line.startswith("Max tokens:"):
                    metadata["max_tokens"] = int(line.split(":")[1].strip())
                    print(f"Extracted max_tokens: {metadata['max_tokens']}")
                elif line.startswith("Temperature:"):
                    metadata["temperature"] = float(line.split(":")[1].strip())
                    print(f"Extracted temperature: {metadata['temperature']}")
                elif line.startswith("Model:"):
                    metadata["model"] = line.split(":")[1].strip()
                    print(f"Extracted model: {metadata['model']}")
                elif line.startswith("#"):  # Another section starts, so exit metadata section
                    is_metadata_section = False
                    lines.insert(0, line)  # Put the line back for further processing
                    break
                elif not line:  # Empty line or any other content ends the metadata section
                    is_metadata_section = False
                    break

        content = "".join(lines)  # The rest of the file is the schema content
        return content, metadata


class ErrorManager:
    @staticmethod
    def handle_error(error_type, additional_info=""):
        error_messages = {
            "schema_not_found": f"Schema not found. {additional_info}",
            "file_not_found": f"File not found. {additional_info}",
            "api_error": f"API call failed. {additional_info}"
        }
        return error_messages.get(error_type, "An unknown error occurred.")


class SchemaExecutor:
    def __init__(self, storage_manager, schema_manager):
        self.storage_manager = storage_manager
        self.schema_manager = schema_manager

    def process_include(self, schema):
        # Updated regex pattern to correctly capture underscores in labels
        for directive_match in re.finditer(r"@include {([\w_]+)}", schema):
            label = directive_match.group(1)
            directive = directive_match.group(0)

            # Read the content from the appropriate folder based on the label
            folder = "content" if "_content" in label else "schemas"
            included_content = self.storage_manager.read_from_drive(label, folder=folder)

            if included_content:
                # Properly include content read from JSON files
                if folder == "content":
                    try:
                        content_json = json.loads(included_content)
                        if "content" in content_json:
                            included_content = content_json["content"]
                    except json.JSONDecodeError:
                        print(f"Warning: Could not decode JSON for {label}")
                # If the included file is a schema, extract only the desired portion
                elif folder == "schemas":
                    match = re.search(r"## Use this schema:\s*~~~(.*?)~~~", included_content, re.DOTALL)
                    if match:
                        included_content = match.group(1).strip()

                # Replace the @include directive with the actual content
                schema = schema.replace(directive, included_content)
            else:
                print(f"Error: No content found for @include {label}")

        return schema


    def execute_schema(self, schema_label, max_tokens=512, temperature=0.7, model="gpt-4o"):
        schema_data = self.schema_manager.get_schema(schema_label)['definition']
        processed_schema = self.process_include(schema_data)

        # Print the model being used to the console
        print(f"Using model: {model}")

        MAX_RETRIES = 3
        RETRY_DELAY = 5  # in seconds

        for _ in range(MAX_RETRIES):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are writing a daily murder mystery using self-contained tokenized evidence elements."},
                        {"role": "user", "content": processed_schema}
                    ],
                    model=model,
                    temperature=temperature
                )

                generated_content = chat_completion.choices[0].message.content
                self.storage_manager.save_to_drive(schema_label, {"content": generated_content})
                return generated_content
            except Exception as e:
                print(f"API call failed. Retrying in {RETRY_DELAY} seconds. Error: {e}")
                time.sleep(RETRY_DELAY)
        print("Failed to get a response from the API after max retries.")

        return None


class ContentGenerationTool:
    def __init__(self, base_drive_path):
        self.storage_manager = DriveStorageManager(base_drive_path)
        self.schema_manager = SchemaManager(base_drive_path)
        self.executor = SchemaExecutor(self.storage_manager, self.schema_manager)
        self.execution_order = ["setting_schema","characters_schema","reports_schema","locations_schema","evidence_schema","thecrime_schema","newevidence_schema", "overview_schema","interrogate_schema","solve1_schema","twist1_schema","all_evidence_schema","solve2_schema","solve3_schema"]


    def run_from_schema(self, start_label):
        start_index = self.execution_order.index(start_label)
        schemas_to_execute = self.execution_order[start_index:]
        for schema_label in schemas_to_execute:
            schema_data = self.schema_manager.get_schema(schema_label)

            # Extracting only metadata for printout
            metadata_for_print = {k: v for k, v in schema_data.items() if k != 'definition'}

            print(f"Metadata for {schema_label}: {metadata_for_print}")  # Print just the metadata

            max_tokens = schema_data.get('max_tokens', 0)
            temperature = schema_data.get('temperature', 0.7)
            model_from_metadata = schema_data.get('model', "gpt-4o")
            self.executor.execute_schema(schema_label, max_tokens=max_tokens, temperature=temperature, model=model_from_metadata)


# Initialize the tool

tool = ContentGenerationTool(BASE_DRIVE_PATH)

# Run the tool from a specific schema
tool.run_from_schema('setting_schema')
