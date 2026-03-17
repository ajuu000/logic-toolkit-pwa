import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Callable, Optional
import concurrent.futures
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

@dataclass
class Result:
    path: Path
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

class BatchProcessor:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def process_directory(self, path: Path, pattern: str = "*") -> List[Result]:
        """
        Process all files in the specified directory that match the given pattern.

        :param path: Path to the directory to process.
        :param pattern: Pattern to match files.
        :return: A list of Result dataclasses containing the outcome of each file processing.
        """
        results = []
        files = list(path.glob(pattern))
        logging.info(f"Found {len(files)} files in {path} matching pattern {pattern}.")

        results = self.process_files(files)
        return results

    def process_files(self, paths: List[Path], callback: Optional[Callable] = None) -> List[Result]:
        """
        Process a list of files concurrently.

        :param paths: List of file paths to process.
        :param callback: Optional callback function to process each file's data.
        :return: A list of Result dataclasses containing the outcome of each file processing.
        """
        results = []

        def process_file(file_path: Path) -> Result:
            try:
                logging.info(f"Processing file: {file_path}")
                with file_path.open('r') as file:
                    data = json.load(file)
                if callback:
                    data = callback(data)
                return Result(path=file_path, success=True, data=data)
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")
                return Result(path=file_path, success=False, error=str(e))

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {executor.submit(process_file, path): path for path in paths}
            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logging.error(f"Exception occurred for file {file_path}: {e}")
                    results.append(Result(path=file_path, success=False, error=str(e)))

        return results
