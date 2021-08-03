"""
Project API
"""
import os
from functools import wraps
from flask import Flask, jsonify, request, send_file
from main import map_comments_with_proposals


API_PATH = os.path.split(os.path.realpath(__file__))[0]
app = Flask(__name__)


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
    sorting_attribute = request.args['sorting_attribute']
    data = request.get_json()

    try:
        map_comments_with_proposals(data, sorting_attribute)
    except Exception:
        return jsonify(
            {'message': 'Error executing script'}
        ), 403
    parsed_file = open('./dist/mapping_proposals_comments.csv', 'rb')
    return send_file(
        parsed_file,
        "application/zip",
        as_attachment=True,
        attachment_filename="mapping_file"
    )


if __name__ == "__main__":
    app.run()
