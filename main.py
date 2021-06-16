"""
Execution of data_manipulation.py
"""
import os
import pandas as pd
from mapping.data_manipulation import init_index, init_txt, init_csv

if __name__ == '__main__':
    df_comments = pd.read_excel(os.path.join(os.getcwd(), "test_data/comments_custom.xls"))
    df_proposals = pd.read_excel(os.path.join(os.getcwd(), "test_data/proposals_custom.xls"))
    hsh_prop = init_index(proposals_dataframe=df_proposals, comments_dataframe=df_comments)
    init_csv(hsh_prop)
    init_txt(hsh_prop)
