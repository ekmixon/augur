from flask import Flask, jsonify, request, Response
import click, os, json, requests, logging
from workers.clustering_worker.clustering_worker import ClusteringWorker
from workers.util import create_server, WorkerGunicornApplication


def main():
    """
    Creates the Flask app and data collection worker, then starts the Gunicorn server
    """
    app = Flask(__name__)
    app.worker = ClusteringWorker()

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
