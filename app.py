from flask import Flask, jsonify, request, send_file
from functools import wraps

from main import main

app = Flask(__name__)


def check_data(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        data = request.get_json(),
        if data is None:
            return jsonify({'message': 'Invalid data'}), 403
        return func(*args, **kwargs)
    return wrapped


@app.route('/', methods=["POST"])
@check_data
def index():
    sorting_attribute = request.args['sorting_attribute']
    data = request.get_json()

    try:
        import pdb; pdb.set_trace()
        main(data, sorting_attribute)
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
