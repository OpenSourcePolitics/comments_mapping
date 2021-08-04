"""
This file aims to store utils functions
that are meant to help file manipulation,
directory cleaning etc
"""
import os
import glob


def clean_directory(directory_path):
    """
    This function is made to remove all the file contained in a directory
    :param directory_path: directory to be cleaned
    :type directory_path: str
    """
    former_files = glob.glob(directory_path + "/*")
    for file in former_files:
        os.remove(file)
