"""
App boilerplate
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from logzero import logger

DEFAULT_PORT = 8000

TASKS = [  # Collection of models
    {'id': 1, 'task': 'build an API', 'other': 'hi'},
    {'id': 2, 'task': '?????'},
    {'id': 3, 'task': 'profit!'}
]

TASK_FIELDS = {
    'task': fields.String,
    'id': fields.Integer
}


def abort_if_task_doesnt_exist(task_id):
    """_Abort request and raise 404 HTTPException if Task ID not found_.
        ### Arguments
           -  __task_id__ : Integer, id for Task item.

        ### Returns
           - __None__

        ### Raises
           - __HTTPException__: 404 when Task ID not found
    """
    if any(task['id'] == task_id for task in TASKS):
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
        def __init__(self):
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument('task', type=str, required=True,
                                       help='No `task` provided', location='json')
            super(TasksAPI, self).__init__()

        def _get_task(self, task_id):
            """Find a task from the collection based on ID else return None"""
            for task in TASKS:
                if str(task['id']) == str(task_id):
                    return task
            return None

        @marshal_with(TASK_FIELDS)
        def get(self, task_id):
            """GET a task"""
            abort_if_task_doesnt_exist(task_id)
            return self._get_task(task_id)

        @marshal_with(TASK_FIELDS)
        def delete(self, task_id):
            """Delete a task"""
            abort_if_task_doesnt_exist(task_id)
            task = self._get_task(task_id)
            TASKS.remove(task)
            return '', 204

        @marshal_with(TASK_FIELDS)
        def put(self, task_id):
            """Update a task"""
            args = self.reqparse.parse_args()
            for i in range(len(TASKS)):
                if TASKS[i]['id'] == task_id:
                    TASKS[i]['task'] = args['task']
                    return TASKS[i], 201

            abort_if_task_doesnt_exist(task_id)

    class TasksListAPI(Resource):
        """APIs for a list of Tasks"""
        def __init__(self):
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument('task', type=str, required=True,
                                       help='No `task` provided', location='json')
            super(TasksListAPI, self).__init__()

        @marshal_with(TASK_FIELDS)
        def get(self):
            """Get a list of all Tasks"""
            return TASKS

        @marshal_with(TASK_FIELDS)
        def post(self):
            """Create a new Task"""
            args = self.reqparse.parse_args()
            task_id = len(TASKS)
            TASKS.append({'id': task_id, 'task': args['task']})
            return TASKS[task_id], 201

    api.add_resource(TasksListAPI, '/tasks')
    api.add_resource(TasksAPI, '/tasks/<task_id>')

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
