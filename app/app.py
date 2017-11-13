"""
App boilerplate
"""

import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource
from logzero import logger

DEFAULT_PORT = 8000

TASKS = {  # Collection of Models
    'task1': {'task': 'build an API'},
    'task2': {'task': '?????'},
    'task3': {'task': 'profit!'},
}

PARSER = reqparse.RequestParser()
PARSER.add_argument('task')  # task is now always required in a request


def abort_if_task_doesnt_exist(task_id):
    """_Abort request and raise 404 HTTPException if Task ID not found_.
        ### Arguments
           -  __task_id__ : Integer, id for Task item.

        ### Returns
           - __None__

        ### Raises
           - __HTTPException__: 404 when Task ID not found
    """
    if task_id not in TASKS:
        abort(404, message="Task {} doesn't exist".format(task_id))


def create_app(config=None):
    """Create the app"""
    app = Flask(__name__)
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})
    CORS(app)
    api = Api(app)

    class TasksAPI(Resource):
        """APIs for a single Tasks"""
        def get(self, task_id):
            """GET a task"""
            abort_if_task_doesnt_exist(task_id)
            return TASKS[task_id]

        def delete(self, task_id):
            """Delete a task"""
            abort_if_task_doesnt_exist(task_id)
            del TASKS[task_id]
            return '', 204

        def put(self, task_id):
            """Update a task"""
            args = PARSER.parse_args()
            task = {'task': args['task']}
            TASKS[task_id] = task
            return task, 201

    class TasksListAPI(Resource):
        """APIs for a list of Tasks"""
        def get(self):
            """Get a list of all Tasks"""
            return TASKS

        def post(self):
            """Create a new Task"""
            args = PARSER.parse_args()
            task_id = int(max(TASKS.keys()).lstrip('task')) + 1
            task_id = 'task{}'.format(task_id)
            TASKS[task_id] = {'task': args['task']}
            return TASKS[task_id], 201

    api.add_resource(TasksListAPI, '/tasks')
    api.add_resource(TasksAPI, '/tasks/<todo_id>')

    @app.route("/")
    def hello_world():
        """Say hi"""
        logger.info("/")
        return "Yolk AI Server"

    return app


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", DEFAULT_PORT))
    app = create_app()
    app.run(host="0.0.0.0", port=PORT)
