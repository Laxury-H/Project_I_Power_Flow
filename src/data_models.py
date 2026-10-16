"""CSV schema: separate generation and demand, all powers on one MVA base."""
from pathlib import Path
import pandas as pd
from .validation import validate

def load_case(name='3bus', data_dir=None):
    root = Path(data_dir) if data_dir else Path(__file__).resolve().parents[1]/'data'
    return read_csv(root/f'buses_{name}.csv', root/f'lines_{name}.csv')

def read_csv(bus_file, line_file):
    buses, lines = pd.read_csv(bus_file), pd.read_csv(line_file)
    validate(buses, lines)
    return buses, lines
