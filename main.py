"""
Execution of data_manipulation.py
"""
import os
import re
from mapping.data_manipulation import init_index, init_txt, init_csv, init_docx, get_data

if __name__ == '__main__':
    main_path = os.path.realpath(__file__)
    root_path = os.path.split(main_path)[0]
    df_proposals, df_comments = get_data(os.path.join(root_path,
                                                      "test_data/comments_config1.xls"),
                                         os.path.join(root_path,
                                                      "test_data/proposals_config1.xls"))
    hsh_prop = init_index(proposals_dataframe=df_proposals, comments_dataframe=df_comments)
    init_csv(hsh_prop)
    init_txt(hsh_prop, sorting_attribute="supports")
    init_docx(hsh_prop, sorting_attribute="supports")
