import json
from pathlib import Path
from typing import Dict, Any, List, Callable
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogicProProcessor:
    def __init__(self, client: 'LogicProClient'):
        """
        Initialize the LogicProProcessor with a LogicProClient instance.

        Args:
            client (LogicProClient): An instance of LogicProClient for interacting with Logic Pro.
        """
        self.client = client

    def process_file(self, path: Path) -> Dict[str, Any]:
        """
        Process a single file and extract relevant information.

        Args:
            path (Path): The path to the file to be processed.

        Returns:
            Dict[str, Any]: A dictionary containing extracted data from the file.
        """
        logger.info(f"Processing file: {path}")
        try:
            text = self.extract_text(path)
            metadata = self.extract_metadata(path)
            return {
                'text': text,
                'metadata': metadata
            }
        except Exception as e:
            logger.error(f"Error processing file {path}: {e}")
            return {}

    def extract_text(self, path: Path) -> str:
        """
        Extract text content from the specified file.

        Args:
            path (Path): The path to the file.

        Returns:
            str: The extracted text content.

        Raises:
            ValueError: If the file format is unsupported.
        """
        if not path.suffix in ['.txt', '.json']:
            raise ValueError(f"Unsupported file format: {path.suffix}")
        
        try:
            if path.suffix == '.txt':
                with open(path, 'r', encoding='utf-8') as file:
                    return file.read()
            elif path.suffix == '.json':
                with open(path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    return json.dumps(data)  # Convert dict to JSON string
        except Exception as e:
            logger.error(f"Error extracting text from {path}: {e}")
            raise

    def extract_metadata(self, path: Path) -> Dict:
        """
        Extract metadata from the specified file.

        Args:
            path (Path): The path to the file.

        Returns:
            Dict: A dictionary containing metadata.

        Raises:
            ValueError: If the file format is unsupported.
        """
        if not path.suffix in ['.txt', '.json']:
            raise ValueError(f"Unsupported file format: {path.suffix}")

        metadata = {
            'filename': path.name,
            'size': path.stat().st_size,
            'modified_time': path.stat().st_mtime
        }
        logger.info(f"Extracted metadata for {path}: {metadata}")
        return metadata

    def batch_process(self, paths: List[Path], progress_callback: Callable[[int, int], None] = None) -> List[Dict]:
        """
        Process multiple files in batch.

        Args:
            paths (List[Path]): A list of paths to the files to be processed.
            progress_callback (Callable[[int, int], None], optional): A callback function to report progress.

        Returns:
            List[Dict]: A list of dictionaries containing extracted data from each file.
        """
        results = []
        total_files = len(paths)
        logger.info(f"Starting batch processing of {total_files} files.")

        for index, path in enumerate(paths):
            result = self.process_file(path)
            results.append(result)
            if progress_callback:
                progress_callback(index + 1, total_files)

        logger.info("Batch processing completed.")
        return results
