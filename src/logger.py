import os
import datetime
import threading
import configparser

class Logger:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.log_dir = self.config.get('Logging', 'log_dir')
        self.lock = threading.Lock()

    def get_log_file(self, log_type):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        folder_path = os.path.join(self.log_dir, today)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return os.path.join(folder_path, f"{log_type}.log")

    def log(self, log_type, message, log_level="INFO"):
        with self.lock:
            try:
                log_file_path = self.get_log_file(log_type)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"{timestamp} [{log_level}] - {message}"
                # Write log entry to file with UTF-8 encoding
                with open(log_file_path, "a", encoding="utf-8") as log_file:
                    log_file.write(log_entry + "\n")
            except Exception as e:
                # If an error occurs during logging, print the error
                print(f"Error logging message: {e}")

if __name__ == "__main__":
    logger = Logger()
    logger.log("RawData", "This is a sample raw data log message.", log_level="INFO")
