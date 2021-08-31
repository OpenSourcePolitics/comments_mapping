"""
Project API
"""
import os
import sys
import traceback
from functools import wraps
from flask import Flask, jsonify, request, send_file, make_response
from mapping.utils.utils_functions import clean_directory
from main import map_comments_with_proposals
import settings.settings as settings

API_PATH = os.path.split(os.path.realpath(__file__))[0]
app = Flask(__name__)


@app.teardown_request
def empty_dist_directory(response):
    """
    Function that will be called after the request
    to clean the dist directory
    :param response:
    :return:
    """
    clean_directory(os.path.join(API_PATH, "dist"))
    return response


def check_data(func):
    """
    decorator function used to check that the data is not null or invalid
    :param func: function on which the decorator is called
    :return:
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        data = request.get_json()
        if data is None:
            return api_response("invalid_data")

        return func(*args, **kwargs)
    return wrapped


@app.route('/', methods=["POST"])
@check_data
def index():
    """
    This function get a json file transmitted by the
    client with a POST request.
    It then returns an archive containing the outputs of the script
    :return: Send the contents of a file to the client. see send_file documentation
    for further information
    """

    try:
        if 'sorting_attribute' in request.args:
            sorting_attribute = request.args['sorting_attribute']
        else:
            sorting_attribute = "supports"

        data = request.get_json()
        map_comments_with_proposals(data, sorting_attribute)

        parsed_file = os.path.join(API_PATH, 'dist/comments_mapping_outputs.zip')
        response = make_response(send_file(
            path_or_file=parsed_file,
            mimetype="application/zip",
            as_attachment=True,
            download_name="mapping_file"
        ))
        response.headers['Content-Disposition'] = "attachment; filename=mapping_file"

        return response
    except Exception as execution_error:
        print(type(execution_error))
        traceback.print_exc(file=sys.stdout)
        print(execution_error)

        return api_response("internal")


if __name__ == "__main__":
    app.run()


def api_response(error):
    if error in settings.ERRORS:
        return jsonify(settings.ERRORS[error]["response"]), settings.ERRORS[error]["code"]

    return jsonify(settings.ERRORS["internal"]["response"]), settings.ERRORS["internal"]["code"]