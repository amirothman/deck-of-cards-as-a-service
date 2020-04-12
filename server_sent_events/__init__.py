from time import sleep

from flask import Blueprint, Response

server_sent_events = Blueprint("server_sent_events", __name__)


def dummy_stream():
    for i in range(10):
        msg = f"event: table\ndata: something{i}\n\n"
        print(msg)
        yield msg
        sleep(5)


@server_sent_events.route("/sse/table/user/")
def current_user_stream():
    return Response(dummy_stream(), mimetype="text/event-stream")
