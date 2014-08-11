#!/usr/bin/env python

from flask import current_app, Flask, request
from subprocess import Popen
import argparse
import logging
import sys


def create_app(commands_file, log_file=None):
    """ Create the WSGI app and load configuration from file.

    Logging to log_file and sysout.
    """
    app = Flask('remosh')
    _init_logging(app, log_file)
    commands = {}
    with open(commands_file) as fh:
        for line in fh:
            if line.strip():
                command_id, command = [s.strip() for s in line.split(': ', 1)]
                commands[command_id] = command
                app.logger.debug('Intialized command: %s -> %s', command_id, command)
    app.config['commands'] = commands

    app.add_url_rule('/', 'exec_command', exec_command, methods=['POST'])
    app.config['OUTPUT_FILE'] = open('/tmp/remoshoutput', 'w')

    return app


def exec_command():
    """ Handle incoming requests. """
    command_id = request.args.get('id')
    current_app.logger.debug('Got request with id %s', command_id)
    command = current_app.config['commands'].get(command_id)
    if command:
        current_app.logger.info('Executing command: %s', command)
        output_handler = current_app.config['OUTPUT_FILE']
        Popen(command, shell=True, bufsize=-1, stdout=output_handler, stderr=output_handler)
        return 'Goodie, goodie, will do!'
    else:
        current_app.logger.info('Command not found with id: %s', command_id)
        return 'Err, unknown id.', 400


def _init_logging(app, log_file=None):
    """ Configure loggers. """
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s')
    sysout_handler = logging.StreamHandler(sys.stdout)
    sysout_handler.setFormatter(formatter)
    app.logger.addHandler(sysout_handler)
    if log_file:
        print("logging to file: %s" % log_file)
        logfile_handler = logging.FileHandler(log_file)
        logfile_handler.setFormatter(formatter)
        app.logger.addHandler(logfile_handler)
    app.logger.setLevel(logging.INFO)


def main():
    parser = argparse.ArgumentParser(prog='remosh')
    parser.add_argument('commands_file', help='Configuration file to use')
    parser.add_argument('-l', '--log-file', help='File to log to')
    args = parser.parse_args()
    app = create_app(args.commands_file, args.log_file)
    app.run(port=8787)


if __name__ == '__main__':
    main()
