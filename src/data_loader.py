import pandas as pd
import os

def load_data(filename: str = "train.csv") -> pd.DataFrame:
    """
    Loads housing data using an absolute path strategy to prevent FileNotFoundError.
    """
    # 1. Getting the directory where data_loader.py is located (the 'src' folder)
    current_dir = os.path.dirname(__file__)
    # This translates to: project_root/data/filename
    #path = os.path.join(current_dir, "..", "data", filename)
    path = os.path.normpath(os.path.join(current_dir, "..", "data", filename))
    
    # 3. Checking if file exists before trying to read 
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Error: The file {filename} was not found at {os.path.abspath(path)}")
    
    print(f"✅ Successfully loaded: {filename}")
    return pd.read_csv(path)