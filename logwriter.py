import datetime

logfile = None


def open_log():
    """
    Opens a log file and sets the global parameter to this new log file
    """
    close_log()
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d-%H-%M-%S')
    logfile_name = "Logs/log_" + formatted_time + ".log"
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
