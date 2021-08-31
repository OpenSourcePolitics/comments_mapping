"""
This file aims to store utils functions
that are meant to help file manipulation,
directory cleaning etc
"""
import os
import glob
from settings.conf import ERRORS
from flask import jsonify


def clear_directory(directory_path):
    """
    This function is made to remove all files contained in a directory
    :param directory_path: directory to be cleaned
    :type directory_path: str
    """
    for file in glob.glob(directory_path + "/*"):
        os.remove(file)

def api_response(error):
    if error in ERRORS:
        return jsonify(ERRORS[error]["response"]), ERRORS[error]["code"]

    return jsonify(ERRORS["internal"]["response"]), ERRORS["internal"]["code"]