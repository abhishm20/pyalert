import os
import subprocess
from datetime import datetime, timedelta

# minutes interval
MINUTES_INTERVAL_TO_CHECK = 1

# email to which logs will be sent
TO_EMAIL = "abhishek.sharma@daybox.in"

# Your app name
APP_NAME = "mojo"

# Time stamp at the start of line to compare
TIME_STAMP_FORMAT = '[%d/%b/%Y %H:%M:%S]'

# Fully qualified path
ERROR_LOG_FILE = ""

PYMAILER_PATH = os.path.join(os.path.expanduser('~'), 'pymailer', 'pymailer.py')
GITHUB_LINK = "https://github.com/abhishm20/pymailer"


def main():
    if not os.path.exists(ERROR_LOG_FILE):
        print "Error: log file does not exists (%s)" % ERROR_LOG_FILE
        exit(-1)
    if not os.path.exists(PYMAILER_PATH):
        print "Error: pymailer not found (please visit %s)" % GITHUB_LINK
        exit(-1)
    added_lines = []
    last_minute = datetime.now() - timedelta(minutes=MINUTES_INTERVAL_TO_CHECK)
    last_line = subprocess.check_output(['tail', '-1', ERROR_LOG_FILE])
    last_time = datetime.strptime(last_line[:22], TIME_STAMP_FORMAT)
    if last_minute < last_time:
        for line in open(ERROR_LOG_FILE):
            line_time = datetime.strptime(line[:22], TIME_STAMP_FORMAT)
            if line_time > last_minute:
                added_lines.append(line)

    if added_lines:
        subprocess.call(["python", PYMAILER_PATH,
                         '-e', TO_EMAIL,
                         '-s', 'Error alert :: %s' % (APP_NAME),
                         '-b', '<br>'.join(added_lines)])


if __name__ == '__main__':
    main()
