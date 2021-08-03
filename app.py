from flask import Flask, jsonify, request, send_file
from functools import wraps
import os

from main import main

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    args = request.args
    sorting_attribute = request.args['sorting_attribute']
    output_format = request.args['output_format']

    data = request.data
    try:
        
        main(sorting_attribute)
    except Exception:
        return jsonify(
            {'message': 'Error executing script'}
        ), 403
    parsed_file = open('./dist/mapping_proposals_comments.csv', 'rb')
    return send_file(
        parsed_file,
        f"application/{output_format}",
        as_attachment=True,
        attachment_filename="mapping_file"
    )


# if __name__ == "__main__":
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=os.environ["PORT"])
