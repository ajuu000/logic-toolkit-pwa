import logging
import json
from pathlib import Path
from typing import Optional
import win32com.client


class LogicProClient:
    """
    A client interface for interacting with Logic Pro using Windows COM.

    Attributes:
        config_path (Path): The path to the configuration file.
        logic_pro (object): The Logic Pro COM object.
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initializes the LogicProClient with an optional configuration path.

        Args:
            config_path (Optional[Path]): Path to the JSON configuration file.
        """
        self.config_path = config_path or Path("config.json")
        self.logic_pro = None
        self.logger = self.setup_logging()

    def setup_logging(self) -> logging.Logger:
        """
        Sets up the logging configuration.

        Returns:
            Logger: Configured logger instance.
        """
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        return logging.getLogger(__name__)

    def connect(self) -> bool:
        """
        Connects to the Logic Pro application using COM.

        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            self.logic_pro = win32com.client.Dispatch("LogicPro.Application")
            self.logger.info("Connected to Logic Pro successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to Logic Pro: {e}")
            return False

    def disconnect(self):
        """
        Disconnects from the Logic Pro application.
        """
        if self.logic_pro:
            self.logic_pro = None
            self.logger.info("Disconnected from Logic Pro.")

    def get_version(self) -> str:
        """
        Retrieves the version of the Logic Pro application.

        Returns:
            str: The version of Logic Pro.

        Raises:
            RuntimeError: If not connected to Logic Pro.
        """
        if not self.logic_pro:
            raise RuntimeError("Not connected to Logic Pro.")
        version = self.logic_pro.Version
        self.logger.info(f"Logic Pro version retrieved: {version}")
        return version

    def is_installed(self) -> bool:
        """
        Checks if Logic Pro is installed on the system.

        Returns:
            bool: True if Logic Pro is installed, False otherwise.
        """
        try:
            # Attempt to create a COM object to check installation
            win32com.client.Dispatch("LogicPro.Application")
            self.logger.info("Logic Pro is installed.")
            return True
        except Exception:
            self.logger.warning("Logic Pro is not installed.")
            return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Logic Pro Toolkit Client")
    parser.add_argument('--config', type=Path, help='Path to the configuration file', default=None)
    args = parser.parse_args()

    client = LogicProClient(config_path=args.config)
    if client.is_installed():
        if client.connect():
            print(f"Logic Pro Version: {client.get_version()}")
            client.disconnect()
    else:
        print("Logic Pro is not installed.")
