"""
Execution of data_manipulation.py
"""
import os
import zipfile
from zipfile import ZipFile
from mapping.data_manipulation import init_index, init_txt, init_csv, init_docx, get_data

MAIN_PATH = os.path.split(os.path.realpath(__file__))[0]


def prepare_archive():
    """
    This function creates an archive storing all the outputs generated by
    map_comments_with_proposals
    """
    dir_path = os.path.join(MAIN_PATH, "dist")
    files = os.listdir(dir_path)
    files.remove('.gitkeep')
    with ZipFile(os.path.join(MAIN_PATH, "dist/comments_mapping_outputs.zip"), "w", zipfile.ZIP_DEFLATED) as new_zip:
        for file in files:
            new_zip.write(os.path.relpath(os.path.join(dir_path, file)))


def map_comments_with_proposals(post_request_result=None, local_json_data_path=None, sorting_attribute=None):
    """
    Main execution function : initialize all the outputs and generate an archive (.zip) containing
    the three generated formats
    :param post_request_result: dictionary containing the data transmitted to the API with a request POST.
    :type post_request_result: dict
    :param local_json_data_path: path to the json file saved locally that contains the data.
    :type local_json_data_path: str
    :param sorting_attribute: parameter passed either with the POST request or manually to indicates how the data
    must be sorted in the output either by number of comments or by number of supports.
    :type sorting_attribute: str
    """
    df_proposals, df_comments = get_data(post_request_json_object=post_request_result, local_json_file_path=local_json_data_path)
    hsh_prop = init_index(proposals_dataframe=df_proposals, comments_dataframe=df_comments)
    init_csv(hsh_prop)
    init_txt(hsh_prop, sorting_attribute=sorting_attribute)
    init_docx(hsh_prop, sorting_attribute=sorting_attribute)
    prepare_archive()
