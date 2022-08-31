####################################################################################################################################
# rules/COUVIS_8xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*_TAU01KM\.TAB', 0, ('Occultation Profile (1 km)',  'SERIES')),
    (r'volumes/.*_TAU10KM\.TAB', 0, ('Occultation Profile (10 km)', 'SERIES')),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_8...)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_TAU_?\d+KM\.(TAB|LBL)', 0,
            [r'previews/COUVIS_8xxx/\2/data/\4_full.jpg',
             r'previews/COUVIS_8xxx/\2/data/\4_med.jpg',
             r'previews/COUVIS_8xxx/\2/data/\4_small.jpg',
             r'previews/COUVIS_8xxx/\2/data/\4_thumb.jpg',
            ]),
])

diagrams_viewables = translator.TranslatorByRegex([
    (r'volumes/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_8...)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_TAU_?\d+KM\.(TAB|LBL)', 0,
            [r'diagrams/COUVIS_8xxx/\2/data/\4_full.jpg',
             r'diagrams/COUVIS_8xxx/\2/data/\4_med.jpg',
             r'diagrams/COUVIS_8xxx/\2/data/\4_small.jpg',
             r'diagrams/COUVIS_8xxx/\2/data/\4_thumb.jpg',
            ]),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_8...)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_(TAU\w+KM|[a-z]+)\..*', 0,
            [r'volumes/COUVIS_8xxx\1/\2/\3/\4_TAU_01KM.LBL',
             r'volumes/COUVIS_8xxx\1/\2/\3/\4_TAU_01KM.TAB',
             r'volumes/COUVIS_8xxx\1/\2/\3/\4_TAU_10KM.LBL',
             r'volumes/COUVIS_8xxx\1/\2/\3/\4_TAU_10KM.TAB',
            ]),
    (r'documents/COUVIS_8xxx.*', 0,
             r'volumes/COUVIS_8xxx'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_8...)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_(TAU\w+KM|[a-z]+)\..*', 0,
            [r'previews/COUVIS_8xxx/\2/data/\3_full.jpg',
             r'previews/COUVIS_8xxx/\2/data/\3_med.jpg',
             r'previews/COUVIS_8xxx/\2/data/\3_small.jpg',
             r'previews/COUVIS_8xxx/\2/data/\3_thumb.jpg',
            ]),
])

associations_to_diagrams = translator.TranslatorByRegex([
    (r'.*/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_8...)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_(TAU\w+KM|[a-z]+)\..*', 0,
            [r'diagrams/COUVIS_8xxx/\2/data/\3_full.jpg',
             r'diagrams/COUVIS_8xxx/\2/data/\3_med.jpg',
             r'diagrams/COUVIS_8xxx/\2/data/\3_small.jpg',
             r'diagrams/COUVIS_8xxx/\2/data/\3_thumb.jpg',
            ]),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'volumes/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_8...)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_(TAU\w+KM)\..*', 0,
            [r'metadata/COUVIS_8xxx/\2/\2_index.tab/\4_\5',
             r'metadata/COUVIS_8xxx/\2/\2_profile_index.tab/\4_TAU01',
             r'metadata/COUVIS_8xxx/\2/\2_supplemental_index.tab/\4_TAU01',
            ]),
])

associations_to_documents = translator.TranslatorByRegex([
    (r'volumes/COUVIS_8xxx/COUVIS_0\d\d\d', 0,
            r'documents/COUVIS_8xxx/*'),
])

####################################################################################################################################
# VERSIONS
####################################################################################################################################

# _v1 had upper case file names and used "DATA/EASYDATA" in place of "data"
# _v1 data files had an underscore after "TAU".
# Case conversions are inconsistent, sometimes mixed case file names are unchanged

versions = translator.TranslatorByRegex([

    # Associate erroneous file names found in early versions
    (r'volumes/COUVIS_8xxx(|_v[0-9\.]+)/COUVIS_8001/data/UVIS_HSP_(2005_139|2009_062)_THEHYA_E_TAU(.*)', 0,
            [r'volumes/COUVIS_8xxx*/COUVIS_8001/data/UVIS_HSP_2009_062_THEHYA_E_TAU\3',
             r'volumes/COUVIS_8xxx*/COUVIS_8001/data/UVIS_HSP_2005_139_THEHYA_E_TAU\3',
            ]),
    (r'volumes/COUVIS_8xxx(|_v[0-9\.]+)/COUVIS_8001/data/UVIS_HSP_(2007_038|2008_026)_SAO205839_I_TAU(.*)', 0,
            [r'volumes/COUVIS_8xxx*/COUVIS_8001/data/UVIS_HSP_2008_026_SAO205839_I_TAU\3',
             r'volumes/COUVIS_8xxx*/COUVIS_8001/data/UVIS_HSP_2007_038_SAO205839_I_TAU\3',
            ]),
    (r'volumes/COUVIS_8xxx(|_v[0-9\.]+)/COUVIS_8001/data/UVIS_HSP_2010_14[89]_LAMAQL_E_TAU(.*)', 0,
            [r'volumes/COUVIS_8xxx*/COUVIS_8001/data/UVIS_HSP_2010_148_LAMAQL_E_TAU\2',
             r'volumes/COUVIS_8xxx*/COUVIS_8001/data/UVIS_HSP_2010_149_LAMAQL_E_TAU\2',
            ]),

    # General corrections...
    (r'volumes/COUVIS_8xxx(|_v[0-9\.]+)/COUVIS_8001/(data|DATA/EASYDATA)/(.*_TAU)_?(.*)', 0,
            [r'volumes/COUVIS_8xxx*/COUVIS_8001/data/\3\4',
             r'volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA/\3_\4',
            ]),
    (r'volumes/COUVIS_8xxx(|_v[0-9\.]+)/COUVIS_8001/(data|DATA/EASYDATA)', 0,
            [r'volumes/COUVIS_8xxx*/COUVIS_8001/data',
             r'volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA',
            ]),
    (r'volumes/COVIMS_8xxx(|_v[0-9\.]+)/COUVIS_8001/(\w+[^aA])(|/.*)', 0,   # don't match "data" directory
            [r'volumes/COUVIS_8xxx*/COUVIS_8001/#LOWER#\2\3',
             r'volumes/COUVIS_8xxx*/COUVIS_8001/#LOWER#\2#MIXED#\3',
             r'volumes/COUVIS_8xxx_v1/COUVIS_8001/#UPPER#\2\3',
             r'volumes/COUVIS_8xxx_v1/COUVIS_8001/#UPPER#\2#MIXED#\3',
            ]),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews|diagrams)/COUVIS_8xxx.*/COUVIS_8.../data', 0, (True, True, False)),
    (r'volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA',           0, (True, True, False)),
])

####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    (r'(UVIS_HSP_...._..._\w+_[IE])_(\w+)\.(.*)', 0, (r'\1', r'_\2', r'.\3')),

    # Group atlas files and their label
    (r'(.*atlas.*)\.(pdf|lbl)', re.I, ('atlas', r'\1', r'.\2')),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*_TAU_?01KM\.(TAB|LBL)', 0, ('Cassini UVIS', 10, 'couvis_occ_01', 'Occultation Profile (1 km)',  True)),
    (r'volumes/.*_TAU_?10KM\.(TAB|LBL)', 0, ('Cassini UVIS', 20, 'couvis_occ_10', 'Occultation Profile (10 km)', True)),
    # Documentation
    (r'documents/COUVIS_8xxx/.*',        0, ('Cassini UVIS', 30, 'couvis_documentation', 'Documentation', False)),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# Use of explicit file names means we don't need to invoke glob.glob(); this goes much faster
opus_products = translator.TranslatorByRegex([
    (r'.*/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_....)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_(TAU.*|[a-z]+)\..*', 0,
            [r'volumes/COUVIS_8xxx*/\2/data/\4_TAU01KM.LBL',
             r'volumes/COUVIS_8xxx*/\2/data/\4_TAU01KM.TAB',
             r'volumes/COUVIS_8xxx*/\2/data/\4_TAU10KM.LBL',
             r'volumes/COUVIS_8xxx*/\2/data/\4_TAU10KM.TAB',
             r'volumes/COUVIS_8xxx_v1/\2/DATA/EASYDATA/\4_TAU_01KM.LBL',
             r'volumes/COUVIS_8xxx_v1/\2/DATA/EASYDATA/\4_TAU_01KM.TAB',
             r'volumes/COUVIS_8xxx_v1/\2/DATA/EASYDATA/\4_TAU_10KM.LBL',
             r'volumes/COUVIS_8xxx_v1/\2/DATA/EASYDATA/\4_TAU_10KM.TAB',
             r'previews/COUVIS_8xxx/\2/data/\4_full.jpg',
             r'previews/COUVIS_8xxx/\2/data/\4_med.jpg',
             r'previews/COUVIS_8xxx/\2/data/\4_small.jpg',
             r'previews/COUVIS_8xxx/\2/data/\4_thumb.jpg',
             r'diagrams/COUVIS_8xxx/\2/data/\4_full.jpg',
             r'diagrams/COUVIS_8xxx/\2/data/\4_med.jpg',
             r'diagrams/COUVIS_8xxx/\2/data/\4_small.jpg',
             r'diagrams/COUVIS_8xxx/\2/data/\4_thumb.jpg',
             r'metadata/COUVIS_8xxx/\2/\2_index.lbl',
             r'metadata/COUVIS_8xxx/\2/\2_index.tab',
             r'metadata/COUVIS_8xxx/\2/\2_profile_index.lbl',
             r'metadata/COUVIS_8xxx/\2/\2_profile_index.tab',
             r'metadata/COUVIS_8xxx/\2/\2_supplemental_index.lbl',
             r'metadata/COUVIS_8xxx/\2/\2_supplemental_index.tab',
            ]),
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/COUVIS_8xxx.*/(data|DATA/EASYDATA)/UVIS_HSP_(\d{4})_(\d{3})_(\w+)_([IE]).*', 0, r'co-uvis-occ-#LOWER#\2-\3-\4-\5'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    (r'co-uvis-occ-(....)-(...)-(.*)-([ie])', 0,  r'volumes/COUVIS_8xxx/COUVIS_8001/data/#UPPER#UVIS_HSP_\1_\2_\3_\4_TAU01KM.TAB'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COUVIS_8xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COUVIS_8xxx', re.I, 'COUVIS_8xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products + pdsfile.PdsFile.OPUS_PRODUCTS
    OPUS_ID = opus_id
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    VIEWABLES = {
        'default': default_viewables,
        'diagram': diagrams_viewables,
    }

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  += associations_to_volumes
    ASSOCIATIONS['previews'] += associations_to_previews
    ASSOCIATIONS['diagrams'] += associations_to_diagrams
    ASSOCIATIONS['metadata'] += associations_to_metadata
    ASSOCIATIONS['documents'] += associations_to_documents

    VERSIONS = versions + pdsfile.PdsFile.VERSIONS

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'co-uvis-occ.*', 0, COUVIS_8xxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COUVIS_8xxx'] = COUVIS_8xxx

####################################################################################################################################
# Unit tests
####################################################################################################################################

import pytest
from .pytest_support import *

@pytest.mark.parametrize(
    'input_path,expected',
    [
        ('volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.TAB',
          {('Cassini UVIS',
            10,
            'couvis_occ_01',
            'Occultation Profile (1 km)',
            True): ['volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.TAB',
                    'volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.LBL',
                    'volumes/COUVIS_8xxx_v2.1/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.TAB',
                    'volumes/COUVIS_8xxx_v2.1/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.LBL',
                    'volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.TAB',
                    'volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.LBL',
                    'volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA/UVIS_HSP_2005_139_126TAU_E_TAU_01KM.TAB',
                    'volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA/UVIS_HSP_2005_139_126TAU_E_TAU_01KM.LBL'],
           ('Cassini UVIS',
            20,
            'couvis_occ_10',
            'Occultation Profile (10 km)',
            True): ['volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU10KM.TAB',
                    'volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU10KM.LBL',
                    'volumes/COUVIS_8xxx_v2.1/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU10KM.TAB',
                    'volumes/COUVIS_8xxx_v2.1/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU10KM.LBL',
                    'volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU10KM.TAB',
                    'volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU10KM.LBL',
                    'volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA/UVIS_HSP_2005_139_126TAU_E_TAU_10KM.TAB',
                    'volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA/UVIS_HSP_2005_139_126TAU_E_TAU_10KM.LBL'],
           ('browse',
            40,
            'browse_full',
            'Browse Image (full)',
            True): ['previews/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_full.jpg'],
           ('browse',
            30,
            'browse_medium',
            'Browse Image (medium)',
            False): ['previews/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_med.jpg'],
           ('browse',
            20,
            'browse_small',
            'Browse Image (small)',
            False): ['previews/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_small.jpg'],
           ('browse',
            10,
            'browse_thumb',
            'Browse Image (thumbnail)',
            False): ['previews/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_thumb.jpg'],
           ('diagram',
            40,
            'diagram_full',
            'Browse Diagram (full)',
            True): ['diagrams/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_full.jpg'],
           ('diagram',
            30,
            'diagram_medium',
            'Browse Diagram (medium)',
            False): ['diagrams/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_med.jpg'],
           ('diagram',
            20,
            'diagram_small',
            'Browse Diagram (small)',
            False): ['diagrams/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_small.jpg'],
           ('diagram',
            10,
            'diagram_thumb',
            'Browse Diagram (thumbnail)',
            False): ['diagrams/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_thumb.jpg'],
           ('metadata',
            5,
            'rms_index',
            'RMS Node Augmented Index',
            False): ['metadata/COUVIS_8xxx/COUVIS_8001/COUVIS_8001_index.tab',
             'metadata/COUVIS_8xxx/COUVIS_8001/COUVIS_8001_index.lbl'],
           ('metadata',
            8,
            'profile_index',
            'Profile Index',
            False): ['metadata/COUVIS_8xxx/COUVIS_8001/COUVIS_8001_profile_index.tab',
             'metadata/COUVIS_8xxx/COUVIS_8001/COUVIS_8001_profile_index.lbl'],
           ('metadata',
            9,
            'supplemental_index',
            'Supplemental Index',
            False): ['metadata/COUVIS_8xxx/COUVIS_8001/COUVIS_8001_supplemental_index.tab',
                     'metadata/COUVIS_8xxx/COUVIS_8001/COUVIS_8001_supplemental_index.lbl']}
        )
    ]
)
def test_opus_products(input_path, expected):
    opus_products_test(input_path, expected)

def test_opus_id_to_primary_logical_path():
    TESTS = [
        'volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_139_126TAU_E_TAU01KM.TAB',
    ]

    for logical_path in TESTS:
        test_pdsf = pdsfile.PdsFile.from_logical_path(logical_path)
        opus_id = test_pdsf.opus_id
        opus_id_pdsf = pdsfile.PdsFile.from_opus_id(opus_id)
        assert opus_id_pdsf.logical_path == logical_path

        # Gather all the associated OPUS products
        product_dict = test_pdsf.opus_products()
        product_pdsfiles = []
        for pdsf_lists in product_dict.values():
            for pdsf_list in pdsf_lists:
                product_pdsfiles += pdsf_list

        # Filter out the metadata products and format files
        product_pdsfiles = [pdsf for pdsf in product_pdsfiles
                                 if pdsf.voltype_ != 'metadata/']
        product_pdsfiles = [pdsf for pdsf in product_pdsfiles
                                 if pdsf.extension.lower() != '.fmt']

        # Gather the set of absolute paths
        opus_id_abspaths = set()
        for pdsf in product_pdsfiles:
            opus_id_abspaths.add(pdsf.abspath)

        for pdsf in product_pdsfiles:
            # Every version is in the product set
            for version_pdsf in pdsf.all_versions().values():
                assert version_pdsf.abspath in opus_id_abspaths

            # Every viewset is in the product set
            for viewset in pdsf.all_viewsets.values():
                for viewable in viewset.viewables:
                    assert viewable.abspath in opus_id_abspaths

            # Every associated product is in the product set except metadata
            for category in ('volumes', 'previews'):
                for abspath in pdsf.associated_abspaths(category):
                    if '.' not in os.path.basename(abspath): continue   # skip dirs
                    assert abspath in opus_id_abspaths

@pytest.mark.parametrize(
    'input_path,expected',
    [
        ('volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2009_062_THEHYA_E_TAU10KM.LBL',
            {999999: 'volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2009_062_THEHYA_E_TAU10KM.LBL',
              20100: 'volumes/COUVIS_8xxx_v2.1/COUVIS_8001/data/UVIS_HSP_2005_139_THEHYA_E_TAU10KM.LBL',
              20000: 'volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2005_139_THEHYA_E_TAU10KM.LBL'
            }),
        ('volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2007_038_SAO205839_I_TAU10KM.TAB',
            {999999: 'volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2008_026_SAO205839_I_TAU10KM.TAB',
              20100: 'volumes/COUVIS_8xxx_v2.1/COUVIS_8001/data/UVIS_HSP_2007_038_SAO205839_I_TAU10KM.TAB',
              20000: 'volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2007_038_SAO205839_I_TAU10KM.TAB',
            }),
        ('volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2010_149_LAMAQL_E_TAU01KM.TAB',
            {999999: 'volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2010_149_LAMAQL_E_TAU01KM.TAB',
              20100: 'volumes/COUVIS_8xxx_v2.1/COUVIS_8001/data/UVIS_HSP_2010_148_LAMAQL_E_TAU01KM.TAB',
              20000: 'volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2010_148_LAMAQL_E_TAU01KM.TAB',
            }),
        ('volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_141_ALPVIR_E_TAU01KM.LBL',
            {999999: 'volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_141_ALPVIR_E_TAU01KM.LBL',
              20100: 'volumes/COUVIS_8xxx_v2.1/COUVIS_8001/data/UVIS_HSP_2005_141_ALPVIR_E_TAU01KM.LBL',
              20000: 'volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2005_141_ALPVIR_E_TAU01KM.LBL',
              10000: 'volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA/UVIS_HSP_2005_141_ALPVIR_E_TAU_01KM.LBL',
            }),
        ('volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA/UVIS_HSP_2005_141_ALPVIR_E_TAU_01KM.LBL',
            {999999: 'volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2005_141_ALPVIR_E_TAU01KM.LBL',
              20100: 'volumes/COUVIS_8xxx_v2.1/COUVIS_8001/data/UVIS_HSP_2005_141_ALPVIR_E_TAU01KM.LBL',
              20000: 'volumes/COUVIS_8xxx_v2.0/COUVIS_8001/data/UVIS_HSP_2005_141_ALPVIR_E_TAU01KM.LBL',
              10000: 'volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA/UVIS_HSP_2005_141_ALPVIR_E_TAU_01KM.LBL',
            }),
    ])
def test_versions(input_path, expected):
    versions_test(input_path, expected)

####################################################################################################################################
