"""
File meant to test the functionalities stored in the main.py
"""
import glob
import os
import pytest
from mapping.utils.utils_functions import clean_directory
from mapping.data_manipulation import read_local_json_data
from main import map_comments_with_proposals

TEST_MAIN_PATH = os.path.split(os.path.realpath(__file__))[0]

config_1_json_data = read_local_json_data(json_file_path=os.path.join(TEST_MAIN_PATH,
                                                                      "../test_data/test_config_1.json"))
config_2_json_data = read_local_json_data(json_file_path=os.path.join(TEST_MAIN_PATH,
                                                                      "../test_data/test_config_2.json"))
config_3_json_data = read_local_json_data(json_file_path=os.path.join(TEST_MAIN_PATH,
                                                                      "../test_data/test_config_3.json"))

JSON_OBJECTS = [config_1_json_data, config_2_json_data, config_3_json_data]


@pytest.mark.parametrize("json_data", JSON_OBJECTS)
def test_map_comments_with_proposals(json_data):
    pytest.skip("TODO: fix this test")
    """
    Checks if the correct number of files are created and that they are correctly
    compressed in a .zip archive
    :param json_data: dictionary storing the different
    :type json_data: dict
    """
    clean_directory(os.path.join(TEST_MAIN_PATH, "../dist"))
    map_comments_with_proposals(post_request_result=json_data)
    assert len(glob.glob(os.path.join(TEST_MAIN_PATH, "../dist/*"))) == 4
