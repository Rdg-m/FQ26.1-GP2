import pandas as pd
import datetime
import json
from pathlib import Path

def read_b3(path:Path, comeco:datetime.datetime, tempo:int, fim=None)->pd.DataFrame:
    pass




print(json.load(open(r'src/dataprocessing/.json', 'r')).keys())