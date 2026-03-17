import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Any, Dict

@dataclass
class Metadata:
    title: str
    author: str
    created: str
    modified: str
    tempo: float
    key_signature: str

class LogicProMetadataReader:
    @staticmethod
    def read(path: Path) -> Metadata:
        """
        Reads metadata from a JSON file at the given path.

        Args:
            path (Path): The path to the JSON file containing metadata.

        Returns:
            Metadata: An instance of Metadata populated with data from the file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            json.JSONDecodeError: If the file is not valid JSON.
            KeyError: If required fields are missing in the metadata.
        """
        if not path.is_file():
            raise FileNotFoundError(f"The file {path} does not exist.")

        with open(path, 'r', encoding='utf-8') as file:
            data: Dict[str, Any] = json.load(file)

        try:
            return Metadata(
                title=data['title'],
                author=data['author'],
                created=data['created'],
                modified=data['modified'],
                tempo=data['tempo'],
                key_signature=data['key_signature']
            )
        except KeyError as e:
            raise KeyError(f"Missing required metadata field: {e}")

    @staticmethod
    def write(path: Path, metadata: Metadata) -> bool:
        """
        Writes metadata to a JSON file at the given path.

        Args:
            path (Path): The path to the JSON file where metadata will be written.
            metadata (Metadata): An instance of Metadata to write to the file.

        Returns:
            bool: True if the write operation was successful, otherwise False.

        Raises:
            IOError: If there is an error writing to the file.
        """
        try:
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(asdict(metadata), file, indent=4)
            return True
        except IOError as e:
            raise IOError(f"Error writing to file {path}: {e}") from e
