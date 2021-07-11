import logging
from pathlib import Path
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

LOG = logging.getLogger(__file__)



directory = Path(__file__).parent

with directory.joinpath('settings.yaml').open() as f:
    
    CONFIGURATION = load(f, Loader=Loader)

    LOG.debug(f"Configuration:{directory}")
    LOG.debug(CONFIGURATION)
