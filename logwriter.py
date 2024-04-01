import util
import os

logfile = None


def open_log():
    """
    Opens a log file and sets the global parameter to this new log file
    """
    if not os.path.exists("./Logs"):
        os.makedirs("./Logs")
    close_log()
    current_datetime = util.get_current_datetime()
    logfile_name = "Logs/log_" + current_datetime + ".log"
    global logfile
    logfile = open(logfile_name, "w")


def write_to_log(message: str):
    """
    Writes to the log file

    :param message: String - Message to be written to the logfile
    """
    global logfile
    if not logfile:
        raise Exception("No open log file")
    else:
        logfile.write(message + '\n')


def close_log():
    """
    Closes the log file
    """
    global logfile
    if logfile:
        logfile.close()
        logfile = None
