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
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

API_PATH = os.path.split(os.path.realpath(__file__))[0]

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

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
            return jsonify({'message': 'Invalid data'}), 403
        return func(*args, **kwargs)
    return wrapped

@app.route("/ping", methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})

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

    if 'sorting_attribute' in request.args:
        sorting_attribute = request.args['sorting_attribute']
    else:
        sorting_attribute = "supports"

    data = request.get_json()
    try:
        map_comments_with_proposals(data, sorting_attribute)
    except Exception as execution_error:
        print(type(execution_error))
        print(execution_error.args)
        traceback.print_exc(file=sys.stdout)
        print(execution_error)
        return jsonify(
            {'message': 'Error executing script'}
        ), 403
    parsed_file = os.path.join(API_PATH, 'dist/comments_mapping_outputs.zip')
    response = make_response(send_file(
        path_or_file=parsed_file,
        mimetype="application/zip",
        as_attachment=True,
        download_name="mapping_file"
    ))
    response.headers['Content-Disposition'] = "attachment; filename=mapping_file"
    return response


if __name__ == "__main__":
    app.run()
