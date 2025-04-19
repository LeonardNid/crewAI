import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class FileWriterToolInput(BaseModel):
    filename: str = Field(..., description="Name of the file to write, including path if needed.")
    content: str = Field(..., description="Full content of the file as a string.")

class FileWriterTool(BaseTool):
    name: str = "file_writer"
    description: str = (
        "A tool to write file contents. Takes a filename and file content."
    )
    args_schema: Type[BaseModel] = FileWriterToolInput

    def _run(self, filename: str, content: str):
        print("Using Tool: file_writer")
        # 1) Root-Verzeichnis erzwingen (z.B. 'Output')
        base_output_dir = "Output"
        # -> Pfad 'Output/<filename>'
        if filename.startswith(base_output_dir):
            full_path = filename
        else:
            full_path = os.path.join(base_output_dir, filename)

        # 2) Verzeichnis-Anteil ermitteln, damit wir ggf. verschachtelte Ordner unterhalb von 'Output' unterstützen
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # 3) Datei schreiben
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{full_path}' has been written."


class FileReaderToolInput(BaseModel):
    filename: str = Field(
        ...,
        description="Name of the file to read from the 'templates' folder, including path if needed."
    )

class FileReaderTool(BaseTool):
    name: str = "file_reader"
    description: str = (
        "Returns the entire file content as a string."
    )
    args_schema: Type[BaseModel] = FileReaderToolInput

    def _run(self, filename: str):
        """
        Reads the specified file (filename) and returns its content.
        """

        if not os.path.exists(filename):
            return f"Error: The file '{filename}' does not exist."

        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error reading file '{filename}': {str(e)}"
