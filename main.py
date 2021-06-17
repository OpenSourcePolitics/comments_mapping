"""
Execution of data_manipulation.py
"""
import os
from mapping.data_manipulation import init_index, init_txt, init_csv, get_data

if __name__ == '__main__':
    df_proposals, df_comments = get_data(os.path.join(os.getcwd(),
                                                      "test_data/comments_config1.xls"),
                                         os.path.join(os.getcwd(),
                                                      "test_data/proposals_config1.xls"))
    hsh_prop = init_index(proposals_dataframe=df_proposals, comments_dataframe=df_comments)
    init_csv(hsh_prop)
    init_txt(hsh_prop)
