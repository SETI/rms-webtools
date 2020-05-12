import pdsfile
import pdsviewable
import pytest
import settings

from tests.helper import instantiate_target_pdsfile

PDS_DATA_DIR = settings.PDS_DATA_DIR
TESTFILE_PATH = settings.TESTFILE_PATH

################################################################################
# PdsViewSet Blackbox test
################################################################################
class TestPdsViewSetBlackBox:
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/' \
            'EUV2004_274_01_39_thumb.png', 'EUV2004_274_01_39_thumb.png'),

        ]
    )
    def test_thumbnail(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        pdsviewset = pdsviewable.PdsViewSet.from_pdsfiles(target_pdsfile)
        # print(getattr(pdsviewset, 'thumbnail'))
        assert expected in pdsviewset.thumbnail.url

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/' \
            'EUV2004_274_09_50_small.png', 'EUV2004_274_09_50_small.png'),

        ]
    )
    def test_small(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        pdsviewset = pdsviewable.PdsViewSet.from_pdsfiles(target_pdsfile)
        assert expected in pdsviewset.small.url

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/' \
            'EUV2004_274_02_25_med.png', 'EUV2004_274_02_25_med.png'),

        ]
    )
    def test_medium(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        pdsviewset = pdsviewable.PdsViewSet.from_pdsfiles(target_pdsfile)
        assert expected in pdsviewset.medium.url

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/' \
            'EUV2004_274_07_10_full.png', 'EUV2004_274_07_10_full.png'),

        ]
    )
    def test_full_size(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        pdsviewset = pdsviewable.PdsViewSet.from_pdsfiles(target_pdsfile)
        assert expected in pdsviewset.full_size.url
