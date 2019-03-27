import os
import logging
import socket
import time
import datetime
import atexit
import signal
import sys
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

time = datetime.now()
HOST_NAME = os.environ.get('OPENSHIFT_APP_DNS', 'localhost')
APP_NAME = os.environ.get('OPENSHIFT_APP_NAME', 'flask')
IP = os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 5080))
HOME_DIR = os.environ.get('OPENSHIFT_HOMEDIR', os.getcwd())

log = logging.getLogger(__name__)
app = Flask(__name__)

if len(sys.argv[1]) >= 2:
    fileName = sys.argv[1]
else:
    fileName = "/tmp/test.txt"

def print_date_time():

    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    try:
        ts = str(int(time.time()))
        f = open(fileName, "a")
        f.write(ts + " Hello World!" + "\n")
        f.close();
    
    except IOError: 
        print ("Error: File " + fileName + " does not appear to exist.")

scheduler = BackgroundScheduler()
    
scheduler.add_job(func=print_date_time, trigger="interval", seconds=10)
    
scheduler.start()

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
    
atexit.register(lambda: scheduler.shutdown())