import json
import csv
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

class DataExporter:
    """A class to export data in various formats for Logic Pro toolkit."""

    @staticmethod
    def to_json(data: List[Dict[str, Any]], path: Path) -> Path:
        """Export data to a JSON file.

        Args:
            data (List[Dict[str, Any]]): The data to export.
            path (Path): The path where the JSON file will be saved.

        Returns:
            Path: The path to the saved JSON file.
        """
        try:
            with open(path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            return path
        except Exception as e:
            raise RuntimeError(f"Failed to export data to JSON: {e}")

    @staticmethod
    def to_csv(data: List[Dict[str, Any]], path: Path) -> Path:
        """Export data to a CSV file.

        Args:
            data (List[Dict[str, Any]]): The data to export.
            path (Path): The path where the CSV file will be saved.

        Returns:
            Path: The path to the saved CSV file.
        """
        try:
            with open(path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return path
        except Exception as e:
            raise RuntimeError(f"Failed to export data to CSV: {e}")

    @staticmethod
    def to_excel(data: List[Dict[str, Any]], path: Path) -> Path:
        """Export data to an Excel file.

        Args:
            data (List[Dict[str, Any]]): The data to export.
            path (Path): The path where the Excel file will be saved.

        Returns:
            Path: The path to the saved Excel file.
        """
        try:
            df = pd.DataFrame(data)
            df.to_excel(path, index=False)
            return path
        except ImportError:
            raise RuntimeError("openpyxl is required for exporting to Excel. Please install it.")
        except Exception as e:
            raise RuntimeError(f"Failed to export data to Excel: {e}")

    @staticmethod
    def to_txt(data: List[Dict[str, Any]], path: Path) -> Path:
        """Export data to a TXT file.

        Args:
            data (List[Dict[str, Any]]): The data to export.
            path (Path): The path where the TXT file will be saved.

        Returns:
            Path: The path to the saved TXT file.
        """
        try:
            with open(path, 'w', encoding='utf-8') as txt_file:
                for entry in data:
                    txt_file.write(f"{entry}\n")
            return path
        except Exception as e:
            raise RuntimeError(f"Failed to export data to TXT: {e}")
