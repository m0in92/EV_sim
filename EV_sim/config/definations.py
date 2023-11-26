import os


ROOT_DIR = os.path.relpath(os.path.join(os.path.dirname(__file__), '..'))
PROJ_DIR = os.path.relpath(os.path.join(os.path.dirname(__file__), '../..'))
EV_DATA_DIR = os.path.join(ROOT_DIR, 'data', 'EV', 'EV_dataset.csv')
