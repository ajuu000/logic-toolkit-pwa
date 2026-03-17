import ctypes
import subprocess
import winreg
from typing import Optional, List

def get_registry_value(key: str, value: str) -> Optional[str]:
    """Retrieve a value from the Windows registry.

    Args:
        key (str): The registry key path.
        value (str): The value name to retrieve.

    Returns:
        Optional[str]: The value associated with the key, or None if not found.
    """
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as registry_key:
            value, _ = winreg.QueryValueEx(registry_key, value)
            return str(value)
    except FileNotFoundError:
        print(f"Registry key not found: {key}")
        return None
    except Exception as e:
        print(f"Error accessing registry: {e}")
        return None

def list_running_processes() -> List[str]:
    """List all currently running processes.

    Returns:
        List[str]: A list of names of running processes.
    """
    try:
        tasks = subprocess.check_output(['tasklist']).decode().splitlines()
        process_names = [task.split()[0] for task in tasks[3:]]  # Skip header lines
        return process_names
    except Exception as e:
        print(f"Error listing processes: {e}")
        return []

def kill_process(name: str) -> bool:
    """Kill a running process by name.

    Args:
        name (str): The name of the process to kill.

    Returns:
        bool: True if the process was killed successfully, False otherwise.
    """
    try:
        subprocess.run(['taskkill', '/F', '/IM', name], check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to kill process: {name}")
        return False
    except Exception as e:
        print(f"Error killing process: {e}")
        return False

def is_admin() -> bool:
    """Check if the current user has administrative privileges.

    Returns:
        bool: True if the user is an administrator, False otherwise.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False

def run_as_admin(cmd: str) -> int:
    """Run a command as an administrator.

    Args:
        cmd (str): The command to run.

    Returns:
        int: The return code of the executed command.
    """
    try:
        result = subprocess.run(['runas', '/user:Administrator', cmd], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Failed to run as admin: {e}")
        return e.returncode
    except Exception as e:
        print(f"Error running command as admin: {e}")
        return -1
