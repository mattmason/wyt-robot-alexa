from flask import Flask, json, send_from_directory
from flask_ask import Ask, audio, current_stream, statement, convert_errors
import logging
import mesh

app = Flask(__name__)
ask = Ask(app, "/")
network = mesh.mesh()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@app.route("/<path:path>")
def send(path):
    return send_from_directory('', path)

@ask.intent("Dance")
def dance():
    stream_url = 'https://1a359321.ngrok.io/uptownfunk.mp3'
    return audio("OK").play(stream_url, offset=16000)

@ask.intent("Autopilot")
def autopilot(value):
    network.broadcast("autopilot%s" % value)
    return statement("Autopilot is %s" % value)

@ask.intent('AMAZON.StopIntent')
def stop():
    network.broadcast("stop")
    return audio('stopping').clear_queue(stop=True)

# optional callbacks
@ask.on_playback_started()
def started(offset, token):
    network.broadcast("dance")
    _infodump('STARTED Audio Stream at {} ms'.format(offset))
    _infodump('Stream holds the token {}'.format(token))
    _infodump('STARTED Audio stream from {}'.format(current_stream.url))

@ask.on_playback_stopped()
def stopped(offset, token):
    network.broadcast("stop")
    _infodump('STOPPED Audio Stream at {} ms'.format(offset))
    _infodump('Stream holds the token {}'.format(token))
    _infodump('Stream stopped playing from {}'.format(current_stream.url))

@ask.on_playback_nearly_finished()
def nearly_finished():
    _infodump('Stream nearly finished from {}'.format(current_stream.url))

@ask.on_playback_finished()
def stream_finished(token):
    network.broadcast("stop")
    _infodump('Playback has finished for stream with token {}'.format(token))

@ask.session_ended
def session_ended():
    return "{}", 200

def _infodump(obj, indent=2):
    msg = json.dumps(obj, indent=indent)
    logger.info(msg)

if __name__ == "__main__":
    app.run(debug=True)

