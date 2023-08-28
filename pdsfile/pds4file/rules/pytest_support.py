################################################################################
# pds4file/ruless/pytest_support.py
################################################################################

import pdsfile.pds4file as pds4file
from pdsfile.cfg import PDS4_BUNDLES_DIR
from pdsfile.general_helper import (instantiate_target_pdsfile_for_class,
                                    get_pdsfiles_for_class,
                                    get_pdsgroups_for_class,
                                    opus_products_test_for_class,
                                    versions_test_for_class,
                                    translate_first_for_class,
                                    translate_all_for_class,
                                    unmatched_patterns_for_class)



import translator
import re
import os

def translate_first(trans, path):
    """Logical paths of "first" files found using given translator on path."""

    return translate_first_for_class(trans, path, pds4file.Pds4File)

def translate_all(trans, path):
    """Logical paths of all files found using given translator on path."""

    return translate_all_for_class(trans, path, pds4file.Pds4File)

def unmatched_patterns(trans, path):
    """List all translated patterns that did not find a matching path in the
    file system."""

    return unmatched_patterns_for_class(trans, path, pds4file.Pds4File)

################################################################################
# Dave's test suite helpers
################################################################################

def instantiate_target_pdsfile(path, is_abspath=True):
    return instantiate_target_pdsfile_for_class(path, pds4file.Pds4File,
                                                PDS4_BUNDLES_DIR, is_abspath)

def get_pdsfiles(paths, is_abspath=True):
    return get_pdsfiles_for_class(paths, pds4file.Pds4File, PDS4_BUNDLES_DIR, is_abspath)

def get_pdsgroups(paths_group, is_abspath=True):
    return get_pdsgroups_for_class(paths_group, pds4file.Pds4File,
                                   PDS4_BUNDLES_DIR, is_abspath)

def opus_products_test(input_path, expected):
    opus_products_test_for_class(input_path, pds4file.Pds4File,
                                 PDS4_BUNDLES_DIR, expected)

def versions_test(input_path, expected):
    versions_test_for_class(input_path, pds4file.Pds4File,
                            PDS4_BUNDLES_DIR, expected)