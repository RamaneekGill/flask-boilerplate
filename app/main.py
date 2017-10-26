"""
App boilerplate
"""

import os

from flask import Flask, jsonify
from flask_cors import CORS
from logzero import logger

DEFAULT_PORT = 8000


def create_app(config=None):
    """Create the app"""
    app = Flask(__name__)
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})
    CORS(app)

    @app.route("/")
    def hello_world():
        """Summary.
        # Arguments
            arg1 : Integer, description of what it is.
        # Returns
            String, description of what it is
        # Raises
            ValueError: when it raises an error
        """
        logger.info("/")
        return "Hello World"

    @app.route("/foo/<someId>")
    def foo_url_arg(someId):
        """Summary.
        # Arguments
            arg1 : Integer, description of what it is.
        # Returns
            String, description of what it is
        # Raises
            ValueError: when it raises an error
        """
        logger.info("/foo/%s", someId)
        return jsonify({"echo": someId})

    return app


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", DEFAULT_PORT))
    app = create_app()
    app.run(host="0.0.0.0", port=PORT)
