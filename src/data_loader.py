import pandas as pd
import logging

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
    
    def load_data(self):
        """Loads data from CSV/TXT with error handling."""
        try:
            # Note: Insurance data often uses '|' or ',' delimiters
            df = pd.read_csv(self.file_path, sep='|',low_memory=False) 
            self.logger.info("Data loaded successfully.")
            return df
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            return None