
import datetime
import os
import os.path


def write_log(path, log, print_log=False):

    # check if path exists
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write('')

    try:
        # open or create new file at path
        f = open(path, 'a', errors='replace')
        # append log to file
        logmsg = str(datetime.datetime.now()) + '; ' + log + '\n'
        f.write(logmsg)
        # close
        f.close()

    except Exception as log_write_err:
        print('LOG WRITE ERROR: ' + str(log_write_err))
        raise Exception('LOG WRITE ERROR: ' + str(log_write_err))

    if print_log:
        print(logmsg)
