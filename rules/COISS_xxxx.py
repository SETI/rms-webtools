####################################################################################################################################
# rules/COISS_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data/.*/N[0-9_]+\.img',                       0, ('Narrow-angle image, VICAR',     'IMAGE'   )),
    (r'volumes/.*/data/.*/W[0-9_]+\.img',                       0, ('Wide-angle image, VICAR',       'IMAGE'   )),
    (r'volumes/.*/data/.*/extras(/\w+)*(|/)',                   0, ('Preview image collection',      'BROWDIR' )),
    (r'volumes/.*/data/.*/extras/.*\.(jpeg|jpeg_small|tiff)',   0, ('Preview image',                 'BROWSE'  )),
    (r'volumes/.*/COISS_0011/document/.*/[0-9]+\.[0-9]+(|/)',   0, ('Calibration report',            'INFODIR' )),
    (r'volumes/.*/data(|/\w*)',                                 0, ('Images grouped by SC clock',    'IMAGEDIR')),
    (r'calibrated/.*_calib\.img',                               0, ('Calibrated image, VICAR',       'IMAGE'   )),
    (r'calibrated/.*/data(|/\w+)',                              0, ('Calibrated images by SC clock', 'IMAGEDIR')),
    (r'calibrated/\w+(|/\w+)',                                  0, ('Calibrated image collection',   'IMAGEDIR')),
    (r'.*/thumbnail(/\w+)*',                                    0, ('Small browse images',           'BROWDIR' )),
    (r'.*/thumbnail/.*\.(gif|jpg|jpeg|jpeg_small|tif|tiff|png)',
                                                                0, ('Small browse image',            'BROWSE'  )),
    (r'.*/(tiff|full)(/\w+)*',                                  0, ('Full-size browse images',       'BROWDIR' )),
    (r'.*/(tiff|full)/.*\.(tif|tiff|png)',                      0, ('Full-size browse image',        'BROWSE'  )),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl', re.I, ''),
    (r'.*/(COISS_[12]xxx)(|_v[0-9\.]+)/(COISS_[12].../data/\w+/[NW][0-9]{10}_[0-9]+).*', 0,  r'previews/\1/\3_*'),
    (r'.*/(COISS_3xxx.*/COISS_3.../data)/(images|maps)/(\w+)\..*',                       0,  r'previews/\1/\2/\3_*'),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([

    # COISS_1xxx and COISS_2xxx
    (r'.*/(COISS_[12]xxx.*/COISS_....)/(data|extras/\w+)/(\w+/[NW][0-9]{10}_[0-9]+).*',
                            0,  [r'volumes/\1/data/\3.IMG',
                                 r'volumes/\1/data/\3.LBL',
                                 r'volumes/\1/extras/thumbnail/\3.IMG.jpeg_small',
                                 r'volumes/\1/extras/browse/\3.IMG.jpeg',
                                 r'volumes/\1/extras/full/\3.IMG.png',
                                 r'volumes/\1/extras/tiff/\3.IMG.tiff']),
    (r'.*/(COISS_[12]xxx.*/COISS_....)/(data|extras/\w+)(|\w+)',
                            0,  [r'volumes/\1/data\3',
                                 r'volumes/\1/extras/thumbnail\3',
                                 r'volumes/\1/extras/browse\3',
                                 r'volumes/\1/extras/full\3']),
    (r'.*/(COISS_[12]xxx.*/COISS_....)/extras',
                            0,  r'volumes/\1/data'),
    (r'.*/(COISS_[12])999.*',
                            0,  r'volumes/\1xxx'),

    # COISS_3xxx
    (r'.*/(COISS_3xxx.*/COISS_3...)/(data|extras/\w+)/(images/\w+[A-Z]+)(|_[a-z]+)\..*',
                            0,  [r'volumes/\1/data/\3.IMG',
                                 r'volumes/\1/extras/browse/\3.IMG.jpeg',
                                 r'volumes/\1/extras/thumbnail/\3.IMG.jpeg_small',
                                 r'volumes/\1/extras/full/\3.IMG.png']),
    (r'.*/(COISS_3xxx.*/COISS_3...)/(data|extras/\w+)/(maps/\w+_SMN).*',
                            0,  [r'volumes/\1/data/\3.lbl',
                                 r'volumes/\1/data/\3.PDF',
                                 r'volumes/\1/extras/browse/\3.jpg',
                                 r'volumes/\1/extras/browse/\3_browse.jpg',
                                 r'volumes/\1/extras/browse/\3.PDF.jpeg',
                                 r'volumes/\1/extras/thumbnail/\3.jpg',
                                 r'volumes/\1/extras/thumbnail/\3_thumb.jpg',
                                 r'volumes/\1/extras/thumbnail/\3.PDF.jpeg',
                                 r'volumes/\1/extras/full/\3.PDF.png']),
    (r'.*/(COISS_3xxx.*/COISS_3...)/(data|extras/\w+)(|/images|/maps)',
                            0,  [r'volumes/\1/data/\3',
                                 r'volumes/\1/extras/browse/\3',
                                 r'volumes/\1/extras/thumbnail/\3',
                                 r'volumes/\1/extras/full/\3']),
    (r'.*/(COISS_3xxx.*/COISS_3...)/extras',
                            0,   r'volumes/\1/data'),
])

associations_to_calibrated = translator.TranslatorByRegex([
    (r'.*/(COISS_[12]xxx)(|_v[0-9\.]+)/(COISS_..../data/\w+/[NW][0-9]{10}_[0-9]+).*',
                            0,  [r'calibrated/\1/\3_CALIB.IMG',
                                 r'calibrated/\1/\3_CALIB.LBL']),
    (r'.*/(COISS_[12])999.*',
                            0,  r'calibrated/\1xxx'),
])

associations_to_previews = translator.TranslatorByRegex([

    # COISS_1xxx and COISS_2xxx
    (r'.*/(COISS_[12]xxx)(|_v[0-9\.]+)/(COISS_....)/(data|extras/\w+)/(\w+/[NW][0-9]{10}_[0-9]+).*',
                            0,  [r'previews/\1/\3/data/\4_full.png',
                                 r'previews/\1/\3/data/\4_*.jpg']),
    (r'.*/(COISS_[12])999.*',
                            0,  r'previews/\1xxx'),

    # COISS_3xxx
    (r'.*/(COISS_3xxx.*/COISS_3...)/(data|extras/\w+)/(images/\w+[A-Z]+)(|_[a-z]+)\..*',
                            0,  [r'previews/\1/data/\3_full.jpg',
                                 r'previews/\1/data/\3_*.jpg']),
    (r'.*/(COISS_3xxx.*/COISS_3...)/(data|extras/\w+)/(maps/\w+_SMN).*',
                            0,  [r'previews/\1/data/\3_*.png']),
    (r'.*/(COISS_3xxx.*/COISS_3...)/(data|extras/\w+)(|/images|/maps)',
                            0,  [r'previews/\1/data/\3',
                                 r'previews/\1/extras/browse/\3',
                                 r'previews/\1/extras/thumbnail/\3',
                                 r'previews/\1/extras/full/\3']),
    (r'.*/(COISS_3xxx.*/COISS_3...)/extras',
                            0,   r'previews/\1/data'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'.*/(COISS_[12]xxx)(|_v[0-9\.]+)/(COISS_....)/(data|extras/w+)/\w+/([NW][0-9]{10}_[0-9]+).*',
                            0,  [r'metadata/\1/\3/\3_index.tab/\5',
                                 r'metadata/\1/\3/\3_ring_summary.tab/\5',
                                 r'metadata/\1/\3/\3_moon_summary.tab/\5',
                                 r'metadata/\1/\3/\3_saturn_summary.tab/\5',
                                 r'metadata/\1/\3/\3_jupiter_summary.tab/\5']),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'.*/COISS_[12].../(data|extras/w+)(|/\w+)', 0, (True, True, True )),
    (r'.*/COISS_3.../(data|extras/w+)/(images|maps)', 0, (True, False, False)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(.*/COISS_[12]xxx.*)/COISS_..../(data|extras/w+)/\w+', 0, r'\1/*/\2/*'),
    (r'(.*/COISS_[12]xxx.*)/COISS_..../(data|extras/w+)',     0, r'\1/*/\2'),

    (r'volumes/COISS_0xxx(|_v[0-9\.]+)/COISS_..../data',               0, r'volumes/COISS_0xxx\1/*/data'),
    (r'volumes/COISS_0xxx(|_v[0-9\.]+)/COISS_..../data/(\w+)',         0, r'volumes/COISS_0xxx\1/*/data/\2'),
    (r'volumes/COISS_0xxx(|_v[0-9\.]+)/COISS_..../data/(\w+/\w+)',     0, r'volumes/COISS_0xxx\1/*/data/\2'),
    (r'volumes/COISS_0xxx(|_v[0-9\.]+)/COISS_..../data/(\w+/\w+)/\w+', 0, r'volumes/COISS_0xxx\1/*/data/\2/*'),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([

    # Skips over N or W, placing files into chronological order
    (r'([NW])([0-9]{10})(.*)_full.png', 0, r'\2\1\3_1full.jpg'),
    (r'([NW])([0-9]{10})(.*)_med.jpg', 0, r'\2\1\3_2med.jpg'),
    (r'([NW])([0-9]{10})(.*)_small.jpg', 0, r'\2\1\3_3small.jpg'),
    (r'([NW])([0-9]{10})(.*)_thumb.jpg', 0, r'\2\1\3_4thumb.jpg'),
    (r'([NW])([0-9]{10})(.*)', 0, r'\2\1\3'),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*\.(IMG|LBL)',                      0, ('Cassini ISS',  0,  'coiss_raw',    'Raw image',                 True)),
    (r'calibrated/.*_CALIB\.(IMG|LBL)',             0, ('Cassini ISS', 10,  'coiss_calib',  'Calibrated image',          True)),
    (r'volumes/.*/extras/thumbnail/.*\.jpeg_small', 0, ('Cassini ISS', 110, 'coiss_thumb',  'Extra preview (thumbnail)', False)),
    (r'volumes/.*/extras/browse/.*\.jpeg',          0, ('Cassini ISS', 120, 'coiss_medium', 'Extra preview (medium)',    False)),
    (r'volumes/.*/extras/(tiff|full)/.*\.\w+',      0, ('Cassini ISS', 130, 'coiss_full',   'Extra preview (full)',      True)),
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.IMG',        0, ('Binary', 'VICAR')),
    (r'.*\.jpeg_small', 0, ('Binary', 'JPEG')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*/(COISS_[12]xxx)(|_v[0-9\.]+)/(COISS_[12]...)/data/(\w+/[NW][0-9]{10}_[0-9]+).*', 0,
                    [r'volumes/\1\2/\3/data/\4.*',
                     r'volumes/\1\2/\3/extras/thumbnail/\4.IMG.jpeg_small',
                     r'volumes/\1\2/\3/extras/browse/\4.IMG.jpeg',
                     r'volumes/\1\2/\3/extras/full/\4.IMG.png',
                     r'volumes/\1\2/\3/extras/tiff/\4.IMG.tiff',
                     r'calibrated/\1/\3/data/\4_CALIB.*',
                     r'previews/\1/\3/data/\4_*',
                     r'metadata/\1/\3/\3_*summary.*',
                     r'metadata/\1/\3/\3_inventory.*',
                     r'metadata/\1/\3/\3_*index.*',
                     ]),
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/COISS_[12]xxx.*/([NW][0-9]{10})_[0-9]+.*', 0, r'co-iss-#LOWER#\1'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

# By identifying the first three digits of the spacecraft clock with a range of volumes, we speed things up quite a bit
opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    (r'co-iss-([nw]188.*)',     0,  r'volumes/COISS_2xxx/COISS_211[5-6]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]187.*)',     0,  r'volumes/COISS_2xxx/COISS_211[2-5]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]186.*)',     0, [r'volumes/COISS_2xxx/COISS_2109/data/*/#UPPER#\1_*.IMG',
                                    r'volumes/COISS_2xxx/COISS_211[0-2]/data/*/#UPPER#\1_*.IMG']),
    (r'co-iss-([nw]185.*)',     0,  r'volumes/COISS_2xxx/COISS_210[6-9]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]184.*)',     0,  r'volumes/COISS_2xxx/COISS_210[4-6]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]183.*)',     0,  r'volumes/COISS_2xxx/COISS_210[1-4]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]182.*)',     0, [r'volumes/COISS_2xxx/COISS_209[8-9]/data/*/#UPPER#\1_*.IMG',
                                    r'volumes/COISS_2xxx/COISS_210[0-1]/data/*/#UPPER#1_*.IMG']),
    (r'co-iss-([nw]181.*)',     0,  r'volumes/COISS_2xxx/COISS_209[6-8]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]180.*)',     0,  r'volumes/COISS_2xxx/COISS_209[4-6]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]179.*)',     0,  r'volumes/COISS_2xxx/COISS_209[1-4]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]178.*)',     0,  r'volumes/COISS_2xxx/COISS_209[0-1]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]177.*)',     0, [r'volumes/COISS_2xxx/COISS_208[8-9]/data/*/#UPPER#\1_*.IMG',
                                    r'volumes/COISS_2xxx/COISS_2090/data/*/#UPPER#\1_*.IMG']),
    (r'co-iss-([nw]176.*)',     0,  r'volumes/COISS_2xxx/COISS_208[6-8]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]175.*)',     0,  r'volumes/COISS_2xxx/COISS_208[3-6]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]174.*)',     0,  r'volumes/COISS_2xxx/COISS_208[0-3]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]173.*)',     0, [r'volumes/COISS_2xxx/COISS_207[8-9]/data/*/#UPPER#\1_*.IMG', 
                                    r'volumes/COISS_2xxx/COISS_2080/data/*/#UPPER#\1_*.IMG']),
    (r'co-iss-([nw]172.*)',     0,  r'volumes/COISS_2xxx/COISS_207[6-8]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]171.*)',     0,  r'volumes/COISS_2xxx/COISS_207[2-6]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]170.*)',     0,  r'volumes/COISS_2xxx/COISS_207[1-2]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]169.*)',     0, [r'volumes/COISS_2xxx/COISS_2069/data/*/#UPPER#\1_*.IMG',
                                    r'volumes/COISS_2xxx/COISS_207[0-1]/data/*/#UPPER#\1_*.IMG']),
    (r'co-iss-([nw]168.*)',     0,  r'volumes/COISS_2xxx/COISS_206[7-9]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]167.*)',     0,  r'volumes/COISS_2xxx/COISS_206[6-7]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]166.*)',     0,  r'volumes/COISS_2xxx/COISS_206[4-6]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]165.*)',     0,  r'volumes/COISS_2xxx/COISS_206[2-4]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]164.*)',     0, [r'volumes/COISS_2xxx/COISS_2059/data/*/#UPPER#\1_*.IMG',
                                    r'volumes/COISS_2xxx/COISS_206[0-2]/data/*/#UPPER#\1_*.IMG']),
    (r'co-iss-([nw]163.*)',     0,  r'volumes/COISS_2xxx/COISS_205[7-9]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]162.*)',     0,  r'volumes/COISS_2xxx/COISS_205[4-7]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]161.*)',     0,  r'volumes/COISS_2xxx/COISS_205[2-4]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]160.*)',     0, [r'volumes/COISS_2xxx/COISS_204[8-9]/data/*/#UPPER#\1_*.IMG',
                                    r'volumes/COISS_2xxx/COISS_205[0-2]/data/*/#UPPER#\1_*.IMG']),
    (r'co-iss-([nw]159.*)',     0,  r'volumes/COISS_2xxx/COISS_204[5-8]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]158.*)',     0,  r'volumes/COISS_2xxx/COISS_204[1-5]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]157.*)',     0, [r'volumes/COISS_2xxx/COISS_204[8-9]/data/*/#UPPER#\1_*.IMG', 
                                    r'volumes/COISS_2xxx/COISS_204[0-1]/data/*/#UPPER#\1_*.IMG']),
    (r'co-iss-([nw]156.*)',     0,  r'volumes/COISS_2xxx/COISS_203[2-8]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]155.*)',     0, [r'volumes/COISS_2xxx/COISS_2029/data/*/#UPPER#\1_*.IMG',
                                    r'volumes/COISS_2xxx/COISS_203[0-2]/data/*/#UPPER#\1_*.IMG']),
    (r'co-iss-([nw]154.*)',     0,  r'volumes/COISS_2xxx/COISS_202[6-9]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]153.*)',     0,  r'volumes/COISS_2xxx/COISS_202[3-6]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]152.*)',     0,  r'volumes/COISS_2xxx/COISS_202[0-3]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]151.*)',     0, [r'volumes/COISS_2xxx/COISS_201[7-9]/data/*/#UPPER#\1_*.IMG',
                                    r'volumes/COISS_2xxx/COISS_2020/data/*/#UPPER#\1_*.IMG']),
    (r'co-iss-([nw]150.*)',     0,  r'volumes/COISS_2xxx/COISS_201[4-7]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]149.*)',     0,  r'volumes/COISS_2xxx/COISS_201[0-4]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]148.*)',     0, [r'volumes/COISS_2xxx/COISS_200[8-9]/data/*/#UPPER#\1_*.IMG',
                                    r'volumes/COISS_2xxx/COISS_2010/data/*/#UPPER#\1_*.IMG']),
    (r'co-iss-([nw]147.*)',     0,  r'volumes/COISS_2xxx/COISS_200[5-8]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]146.*)',     0,  r'volumes/COISS_2xxx/COISS_200[1-5]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]145.*)',     0, [r'volumes/COISS_1xxx/COISS_1009/data/*/#UPPER#\1_*.IMG',
                                    r'volumes/COISS_2xxx/COISS_2001/data/*/#UPPER#\1_*.IMG']),
    (r'co-iss-([nw]144.*)',     0,  r'volumes/COISS_1xxx/COISS_100[8-9]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]14[123].*)', 0,  r'volumes/COISS_1xxx/COISS_1008/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]140.*)',     0,  r'volumes/COISS_1xxx/COISS_100[7-8]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]13[789].*)', 0,  r'volumes/COISS_1xxx/COISS_1007/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]136.*)',     0,  r'volumes/COISS_1xxx/COISS_100[6-7]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]135.*)',     0,  r'volumes/COISS_1xxx/COISS_100[1-6]/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]13[0-4].*)', 0,  r'volumes/COISS_1xxx/COISS_1001/data/*/#UPPER#\1_*.IMG'),
    (r'co-iss-([nw]12.*)',      0,  r'volumes/COISS_1xxx/COISS_1001/data/*/#UPPER#\1_*.IMG'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COISS_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COISS_[0123]xxx', re.I, 'COISS_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_FORMAT = opus_format + pdsfile.PdsFile.OPUS_FORMAT
    OPUS_PRODUCTS = opus_products
    OPUS_ID = opus_id
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    VIEWABLES = {'default': default_viewables}

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']    = associations_to_volumes
    ASSOCIATIONS['calibrated'] = associations_to_calibrated
    ASSOCIATIONS['previews']   = associations_to_previews
    ASSOCIATIONS['metadata']   = associations_to_metadata

    def FILENAME_KEYLEN(self):
        if self.volset[:10] == 'COISS_3xxx':
            return 0
        else:
            return 11   # trim off suffixes

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'co-iss-.*', 0, COISS_xxxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COISS_xxxx'] = COISS_xxxx

####################################################################################################################################
