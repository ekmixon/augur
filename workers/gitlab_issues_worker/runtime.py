#SPDX-License-Identifier: MIT
from flask import Flask, jsonify, request, Response
import click, os, json, requests, logging
from workers.gitlab_issues_worker.gitlab_issues_worker import GitLabIssuesWorker
from workers.util import WorkerGunicornApplication, create_server

def main():
    """ Declares singular worker and creates the server and flask app that it will be running on
    """
    app = Flask(__name__)
    app.worker = GitLabIssuesWorker()

    create_server(app)
    WorkerGunicornApplication(app).run()

    if app.worker._child is not None:
        app.worker._child.terminate()
    try:
        requests.post(
            f'http://{broker_host}:{broker_port}/api/unstable/workers/remove',
            json={"id": config['id']},
        )

    except:
        pass

    os.kill(os.getpid(), 9)