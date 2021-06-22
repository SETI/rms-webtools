####################################################################################################################################
# rules/VG_28xx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'.*/EDITDATA', re.I, ('Edited data',                   'DATADIR')),
    (r'.*/FOVMAPS',  re.I, ('Field-of-view maps',            'IMAGEDIR')),
    (r'.*/IMAGES',   re.I, ('Star reference image files',    'IMAGEDIR')),
    (r'.*/JITTER',   re.I, ('Pointing data',                 'GEOMDIR')),
    (r'.*/NOISDATA', re.I, ('Noise data',                    'DATADIR')),
    (r'.*/RAWDATA',  re.I, ('Raw data',                      'DATADIR')),
    (r'.*/TRAJECT',  re.I, ('Trajectory data',               'GEOMDIR')),
    (r'.*/VECTORS',  re.I, ('Pointing data',                 'GEOMDIR')),
    (r'.*/S_RINGS',  re.I, ('Saturn ring occultation data',  'DATADIR')),
    (r'.*/U_RINGS',  re.I, ('Uranian ring occultation data', 'DATADIR')),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

# view_options = translator.TranslatorByRegex([
#     (r'volumes/VG_28xx(|/\w+)/VG_28../IMAGES', 0, (True, False, False)),
# ])


####################################################################################################################################
# FILESPEC_TO_VOLSET
####################################################################################################################################

filespec_to_volset = translator.TranslatorByRegex([
    (r'VG_28\d{2}.*', 0, r'VG_28xx'),
])


####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################
# (dataset name, priority (where lower comes first), type ID, description)
opus_type = translator.TranslatorByRegex([
    # (r'volumes/.*_TAU_?01KM\.(TAB|LBL)', 0, ('Cassini UVIS', 10, 'couvis_occ_01', 'Occultation Profile (1 km)',  True)),
    # (r'volumes/.*_TAU_?10KM\.(TAB|LBL)', 0, ('Cassini UVIS', 20, 'couvis_occ_10', 'Occultation Profile (10 km)', True)),
    # VG_2801
    (r'volumes/.*/VG_2801/EASYDATA/KM000_1/(.*)\.(TAB|LBL)',  0, ('Voyager PPS', 10, 'voyager_occ_0_1', 'Occultation Profile (0.1 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM000_2/(.*)\.(TAB|LBL)',  0, ('Voyager PPS', 20, 'voyager_occ_0_2', 'Occultation Profile (0.2 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM000_5/(.*)\.(TAB|LBL)',  0, ('Voyager PPS', 30, 'voyager_occ_0_5', 'Occultation Profile (0.5 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM001/(.*)\.(TAB|LBL)',    0, ('Voyager PPS', 40, 'voyager_occ_01', 'Occultation Profile (1 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM002/(.*)\.(TAB|LBL)',    0, ('Voyager PPS', 50, 'voyager_occ_02', 'Occultation Profile (2 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM005/(.*)\.(TAB|LBL)',    0, ('Voyager PPS', 60, 'voyager_occ_05', 'Occultation Profile (5 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM010/(.*)\.(TAB|LBL)',    0, ('Voyager PPS', 70, 'voyager_occ_10', 'Occultation Profile (10 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM020/(.*)\.(TAB|LBL)',    0, ('Voyager PPS', 80, 'voyager_occ_20', 'Occultation Profile (20 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM050/(.*)\.(TAB|LBL)',    0, ('Voyager PPS', 90, 'voyager_occ_50', 'Occultation Profile (50 km)',  True)),
    # VG_2802
    (r'volumes/.*/VG_2802/EASYDATA/FILTER01/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 10, 'voyager_occ_full_res', 'Occultation Profile (full resolution)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/FILTER02/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 20, 'voyager_occ_fact_of_2_res', 'Occultation Profile (a factor of 2 resolution)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/FILTER03/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 30, 'voyager_occ_fact_of_3_res', 'Occultation Profile (a factor of 3 resolution)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/FILTER04/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 40, 'voyager_occ_fact_of_4_res', 'Occultation Profile (a factor of 4 resolution)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/FILTER05/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 50, 'voyager_occ_fact_of_5_res', 'Occultation Profile (a factor of 5 resolution)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM000_2/(.*)\.(TAB|LBL)',  0, ('Voyager UVS', 60, 'voyager_occ_0_2', 'Occultation Profile (0.2 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM000_5/(.*)\.(TAB|LBL)',  0, ('Voyager UVS', 70, 'voyager_occ_0_5', 'Occultation Profile (0.5 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM001/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 80, 'voyager_occ_01', 'Occultation Profile (1 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM002/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 90, 'voyager_occ_02', 'Occultation Profile (2 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM005/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 100, 'voyager_occ_05', 'Occultation Profile (5 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM010/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 110, 'voyager_occ_10', 'Occultation Profile (10 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM020/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 120, 'voyager_occ_20', 'Occultation Profile (20 km)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM050/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 130, 'voyager_occ_50', 'Occultation Profile (50 km)',  True)),
    # VG_2803
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM000_2/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 10, 'voyager_occ_0_2', 'Occultation Profile (0.4 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM000_5/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 20, 'voyager_occ_0_5', 'Occultation Profile (1 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM001/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 30, 'voyager_occ_01', 'Occultation Profile (2 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM002/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 40, 'voyager_occ_02', 'Occultation Profile (4 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM002_5/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 50, 'voyager_occ_02_5', 'Occultation Profile (5 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM005/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 60, 'voyager_occ_05', 'Occultation Profile (10 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM010/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 70, 'voyager_occ_10', 'Occultation Profile (20 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM020/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 80, 'voyager_occ_20', 'Occultation Profile (40 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM050/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 90, 'voyager_occ_50', 'Occultation Profile (100 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM00_025/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 10, 'voyager_occ_0_025', 'Occultation Profile (0.05 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM00_05/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 20, 'voyager_occ_0_05', 'Occultation Profile (0.1 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM00_1/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 30, 'voyager_occ_0_1', 'Occultation Profile (0.2 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM00_2/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 40, 'voyager_occ_0_2', 'Occultation Profile (0.4 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM00_25/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 50, 'voyager_occ_0_25', 'Occultation Profile (0.5 km)',  True)),
    (r'volumes/.*/VG_2803/.*/EASYDATA/KM00_5/(.*)\.(TAB|LBL)',  0, ('Voyager RSS', 60, 'voyager_occ_0_5', 'Occultation Profile (1 km)',  True)),
    # VG_2810
    (r'volumes/.*/VG_2810/DATA/.*KM002\.(TAB|LBL)',  0, ('Voyager ISS', 10, 'voyager_prof_02', 'Intensity Profile (2 km)',  True)),
    (r'volumes/.*/VG_2810/DATA/.*KM004\.(TAB|LBL)',  0, ('Voyager ISS', 10, 'voyager_prof_04', 'Intensity Profile (4 km)',  True)),
    (r'volumes/.*/VG_2810/DATA/.*KM010\.(TAB|LBL)',  0, ('Voyager ISS', 10, 'voyager_prof_10', 'Intensity Profile (10 km)',  True)),
    (r'volumes/.*/VG_2810/DATA/.*KM020\.(TAB|LBL)',  0, ('Voyager ISS', 10, 'voyager_prof_20', 'Intensity Profile (20 km)',  True)),

])


####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# Use of explicit file names means we don't need to invoke glob.glob(); this goes much faster
# opus_products = translator.TranslatorByRegex([
#     (r'.*/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_....)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_(TAU.*|[a-z]+)\..*', 0,
#             [r'volumes/COUVIS_8xxx*/\2/data/\4_TAU01KM.LBL',
#              r'volumes/COUVIS_8xxx*/\2/data/\4_TAU01KM.TAB',
#              r'volumes/COUVIS_8xxx*/\2/data/\4_TAU10KM.LBL',
#              r'volumes/COUVIS_8xxx*/\2/data/\4_TAU10KM.TAB',
#              r'volumes/COUVIS_8xxx_v1/\2/DATA/EASYDATA/\4_TAU_01KM.LBL',
#              r'volumes/COUVIS_8xxx_v1/\2/DATA/EASYDATA/\4_TAU_01KM.TAB',
#              r'volumes/COUVIS_8xxx_v1/\2/DATA/EASYDATA/\4_TAU_10KM.LBL',
#              r'volumes/COUVIS_8xxx_v1/\2/DATA/EASYDATA/\4_TAU_10KM.TAB',
#              r'previews/COUVIS_8xxx/\2/data/\4_full.jpg',
#              r'previews/COUVIS_8xxx/\2/data/\4_med.jpg',
#              r'previews/COUVIS_8xxx/\2/data/\4_small.jpg',
#              r'previews/COUVIS_8xxx/\2/data/\4_thumb.jpg',
#              r'diagrams/COUVIS_8xxx/\2/data/\4_full.jpg',
#              r'diagrams/COUVIS_8xxx/\2/data/\4_med.jpg',
#              r'diagrams/COUVIS_8xxx/\2/data/\4_small.jpg',
#              r'diagrams/COUVIS_8xxx/\2/data/\4_thumb.jpg',
#              r'metadata/COUVIS_8xxx/\2/\2_index.lbl',
#              r'metadata/COUVIS_8xxx/\2/\2_index.tab',
#              r'metadata/COUVIS_8xxx/\2/\2_profile_index.lbl',
#              r'metadata/COUVIS_8xxx/\2/\2_profile_index.tab',
#              r'metadata/COUVIS_8xxx/\2/\2_supplemental_index.lbl',
#              r'metadata/COUVIS_8xxx/\2/\2_supplemental_index.tab',
#             ]),
# ])


####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    # (r'.*/VG_28xx/VG_28(\d{2})/EASYDATA/KM0(.*)/(.*{5})(\w{2})\..*', 0, r'vg-pps-occ'),
    (r'.*/VG_28xx/VG_28(\d{2})/EASYDATA/KM0(.*)/(.*)\..*', 0, r'vg-pps-occ-\1-\3'),
    (r'.*/VG_28xx/VG_28(\d{2})/EASYDATA/(FILTER.*|KM0.*)/(.*)\..*', 0, r'vg-uvs-occ-\1-\3'),
    (r'.*/VG_28xx/VG_28(\d{2})/(S|U)_RINGS/EASYDATA/KM0.*/(.*)\..*', 0, r'vg-rss-occ-\1-\2-\3'),
    (r'.*/VG_28xx/VG_28(\d{2})/DATA/(IS\d_P....).*\..*', 0, r'vg-iss-occ-\1-\2'),
])


####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################
#
# opus_id_to_primary_logical_path = translator.TranslatorByRegex([
#     (r'co-uvis-occ-(....)-(...)-(.*)-([ie])', 0,  r'volumes/COUVIS_8xxx/COUVIS_8001/data/#UPPER#UVIS_HSP_\1_\2_\3_\4_TAU01KM.TAB'),
# ])


####################################################################################################################################
# Subclass definition
####################################################################################################################################

class VG_28xx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VG_28xx', re.I, 'VG_28xx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    # DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    # VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    # SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES
    #
    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    # OPUS_PRODUCTS = opus_products
    OPUS_ID = opus_id
    # OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path
    #
    # VIEWABLES = {
    #     'default': default_viewables,
    #     'diagram': diagrams_viewables,
    # }
    #
    # ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    # ASSOCIATIONS['volumes']  += associations_to_volumes
    # ASSOCIATIONS['previews'] += associations_to_previews
    # ASSOCIATIONS['diagrams'] += associations_to_diagrams
    # ASSOCIATIONS['metadata'] += associations_to_metadata
    #
    # VERSIONS = versions + pdsfile.PdsFile.VERSIONS

pdsfile.PdsFile.FILESPEC_TO_VOLSET = filespec_to_volset + pdsfile.PdsFile.FILESPEC_TO_VOLSET

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'vg-pps-occ.*', 0, VG_28xx)]) + \
                                      translator.TranslatorByRegex([(r'vg-uvs-occ.*', 0, VG_28xx)]) + \
                                      translator.TranslatorByRegex([(r'vg-rss-occ.*', 0, VG_28xx)]) + \
                                      translator.TranslatorByRegex([(r'vg-iss-occ.*', 0, VG_28xx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS


####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VG_28xx'] = VG_28xx

####################################################################################################################################
