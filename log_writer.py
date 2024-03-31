import datetime


class LogWriter:
    """
    Class that provides functionality to write log files
    """
    def __init__(self):
        """
        Opens a new log file corresponding to the current date and time
        """
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d-%H-%M-%S')
        logfile_name = "Logs/log_" + formatted_time + ".txt"

        self.log_file = open(logfile_name, "w")

    def write(self, message: str):
        """
        Writes to the log file

        :param message: String - Message to be written to the logfile
        """
        if not self.log_file:
            raise Exception("No log file")
        self.log_file.write(message + '\n')

    def close(self):
        """
        Closes the log file
        """
        if self.log_file:
            self.log_file.close()
            self.log_file = None
