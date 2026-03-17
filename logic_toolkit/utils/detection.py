import os
import platform
from pathlib import Path
from typing import Optional


def find_installation() -> Optional[Path]:
    """
    Check common installation paths for Logic Pro and return the installation path if found.

    Returns:
        Optional[Path]: The path to the Logic Pro installation, or None if not found.
    """
    if platform.system() == "Windows":
        common_paths = [
            Path("C:/Program Files/Logic Pro"),
            Path("C:/Program Files (x86)/Logic Pro"),
            Path("C:/Logic Pro"),
        ]
        
        for path in common_paths:
            if path.exists() and path.is_dir():
                return path
    return None


def get_version() -> Optional[str]:
    """
    Get the version of Logic Pro if it is installed.

    Returns:
        Optional[str]: The version of Logic Pro, or None if it cannot be determined.
    """
    installation_path = find_installation()
    if installation_path:
        version_file = installation_path / "version.txt"  # Assuming version info is stored here
        if version_file.exists():
            try:
                with version_file.open("r") as file:
                    return file.read().strip()
            except Exception as e:
                print(f"Error reading version file: {e}")
    return None


def is_installed() -> bool:
    """
    Check if Logic Pro is installed.

    Returns:
        bool: True if Logic Pro is installed, False otherwise.
    """
    return find_installation() is not None


def get_executable_path() -> Optional[Path]:
    """
    Get the path to the Logic Pro executable.

    Returns:
        Optional[Path]: The path to the Logic Pro executable, or None if not found.
    """
    installation_path = find_installation()
    if installation_path:
        executable_path = installation_path / "LogicPro.exe"  # Assuming the executable file is named this
        if executable_path.exists():
            return executable_path
    return None
