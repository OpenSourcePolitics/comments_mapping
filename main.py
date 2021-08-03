"""
Execution of data_manipulation.py
"""
import os
from mapping.data_manipulation import init_index, init_txt, init_csv, init_docx, get_data


def main(json_object, sorting_attribute=None):
    df_proposals, df_comments = get_data(json_object)
    hsh_prop = init_index(proposals_dataframe=df_proposals, comments_dataframe=df_comments)
    init_csv(hsh_prop)
    init_txt(hsh_prop, sorting_attribute=sorting_attribute)
    init_docx(hsh_prop, sorting_attribute=sorting_attribute)
