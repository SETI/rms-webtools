##########################################################################################
# pds-webtools/conftest.py
#
# Configuration & setup before running tests on pds4file
##########################################################################################

import os
import pdsfile.pds3file as pds3file
import pdsfile.pds4file as pds4file
from pdsfile.general_helper import (PDS4_HOLDINGS_DIR,
                                    PDS_HOLDINGS_DIR,
                                    set_logger)
import pdslogger
import pytest

##########################################################################################
# Setup before all tests
##########################################################################################
def pytest_addoption(parser):
    parser.addoption("--mode", action="store")

def turn_on_logger(filename):
    LOGGER = pdslogger.PdsLogger(filename)
    set_logger(pds3file.Pds3File, LOGGER)
    set_logger(pds4file.Pds4File, LOGGER)

@pytest.fixture(scope='session', autouse=True)
def setup(request):
    mode = request.config.option.mode
    if mode == 's':
        pds3file.Pds3File.use_shelves_only(True)
        pds4file.Pds4File.use_shelves_only(True)
    elif mode == 'ns':
        pds3file.Pds3File.use_shelves_only(False)
        pds4file.Pds4File.use_shelves_only(False)
    else: # pragma: no cover
        pds3file.Pds3File.use_shelves_only(True)
        pds4file.Pds4File.use_shelves_only(True)

    # turn_on_logger("test_log.txt")
    pds3file.Pds3File.preload(PDS_HOLDINGS_DIR)
    pds4file.Pds4File.preload(PDS4_HOLDINGS_DIR)
