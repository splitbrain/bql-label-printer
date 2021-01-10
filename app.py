#!/usr/bin/env python

"""
Simple Web Interface to create labels on a Brother Printer
"""

import sys
from glob import glob
from os.path import basename

from PIL import Image
from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends import backend_factory, guess_backend
from brother_ql.devicedependent import models, label_type_specs, label_sizes
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

DEBUG = False
MODEL = None
BACKEND_CLASS = None
BACKEND_STRING_DESCR = None
LABEL_SIZES = [(name, label_type_specs[name]['name']) for name in label_sizes]


@app.route('/')
def do_editor():
    """
    The main editor view
    :return:
    """
    return render_template(
        'index.html',
        labels=get_labels()
    )

@app.route('/expiry')
def do_expiry():
    """
    The expiry label view
    :return:
    """
    return render_template(
        'expiry.html'
    )


@app.route('/print', methods=['POST'])
def do_print():
    """
    Receive the image from the frontend and print it
    :return: string a simple 'ok' when no exception was thrown
    """
    im = Image.open(request.files['data'])
    qlr = BrotherQLRaster(MODEL)
    create_label(qlr, im, request.form['size'], threshold=70, cut=False, rotate=0)

    # noinspection PyCallingNonCallable
    be = BACKEND_CLASS(BACKEND_STRING_DESCR)
    be.write(qlr.data)
    be.dispose()
    del be

    return 'ok'


def get_labels():
    """
    List the available label templates
    :return:
    """
    filenames = glob(sys.path[0] + '/static/labels/*.html')
    filenames.sort()
    return [basename(x[:-5]) for x in filenames]


def main():
    """
    Initializes the webserver
    :return:
    """
    global DEBUG, MODEL, BACKEND_CLASS, BACKEND_STRING_DESCR
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1', help='The IP the webserver should bind to. Use 0.0.0.0 for all')
    parser.add_argument('--port', default=8013, help='The port the webserver should start on')
    parser.add_argument('--debug', action='store_true', default=False, help='Activate flask debugging support')
    parser.add_argument('--model', default='QL-500', choices=models, help='The model of your printer (default: QL-500)')
    parser.add_argument('printer',
                        help='String descriptor for the printer to use (like tcp://192.168.0.23:9100 or '
                             'file:///dev/usb/lp0)')
    args = parser.parse_args()

    DEBUG = args.debug
    MODEL = args.model

    try:
        selected_backend = guess_backend(args.printer)
        BACKEND_CLASS = backend_factory(selected_backend)['backend_class']
        BACKEND_STRING_DESCR = args.printer
    except:
        parser.error("Couldn't guess the backend to use from the printer string descriptor")

    app.run(host=args.host, port=args.port, debug=DEBUG)


if __name__ == "__main__":
    main()
