import _logger_base as loggerBase

class LogReader:
    def __init__(self, log_package_path):
        """
        Initializes a LogReader to read logs from a specified log package path.

        :param log_package_path: The path to the log package to be read.
        """
        self.reader = loggerBase._LogReader(log_package_path)

    def get_log_info(self):
        """
        Retrieves and prints information about the logs in the package, such as name, count, start timestamp, and end timestamp.

        :return: Information about the logs in the package.
        """
        return self.reader.get_log_info()

    def read_logs(self):
        """
        Generator function to read logs from the opened log package.

        Usage Example:
        ```
        logger = Logger()
        log = logger.open()
        logs = log.read_logs()
        for log in logs:
            print(log)
        ```
        :return: Generator yielding log entries.
        """
        return self.reader.read_logs()

    def get_msg_count(self):
        """
        Retrieves the total count of messages in the log package.

        :return: The count of messages in the log package.
        """
        return self.reader.get_msg_count()

    def select_msg(self, timestamp):
        """
        Selects a message based on a timestamp and returns an iterator for it.

        Usage Example:
        ```
        logger = Logger()
        log = logger.open()
        now_msg = log.select_msg(time.time() * 1e9)
        print(now_msg.msg())
        print(now_msg.next(step=1))
        print(now_msg.prev(step=1))
        ```
        :param timestamp: The timestamp to select the message by.
        :return: A message iterator for the selected message.
        """
        return self.reader.select_msg(timestamp)

    def filter(self, message_tag=None, timestamp=None, index=None, count=None):
        """
        Filters the logs based on the provided criteria.

        Usage Example:
        ```
        logger = Logger()
        log = logger.open()
        log.filter(message_tag="vision", timestamp=0, index=0, count=10)
        log.filter(timestamp=[0, 99999999999999])
        ```
        :param message_tag: List of message tags to filter by (e.g., ["vision", "debug"]).
        :param timestamp: Either a specific timestamp or a range [start, end] to filter by.
        :param index: Either a specific index or a range [start, end] to filter by.
        :param count: Number of messages to return starting from the index.
        :return: List of filtered messages.
        """
        return self.reader.filter(message_tag, timestamp, index, count)

class Logger:
    def __init__(self, log_dir="logs"):
        """
        Logger class for managing log recording and reading, including UDP messages.

        :param log_dir: The directory to store logs.
        """
        self.logger = loggerBase._Logger(log_dir)

    def record_udp(self, udp_dict):
        """
        Records UDP messages based on a dictionary of UDP configurations.

        Usage Example:
        ```
        udp_dict = {
            "event": ["233.233.233.233", 1670],
            "vision": ["233.233.233.233", 41001],
            "debug": ["233.233.233.233", 20001],
        }

        logger = Logger()
        logger.record_udp(udp_dict)
        while True:
            pass
        ```
        :param udp_dict: A dictionary with configurations for each UDP message.
        """
        self.logger.record_udp(udp_dict)

    def stop(self):
        """
        Stops recording UDP messages and clears the receiver list.
        """
        self.logger.stop()

    def record(self, message, tag, source=""):
        """
        Records a message to the log with a specified tag and source.

        Usage Example:
        ```
        udp_dict = {
            # msg_tag:["ip", port],
            "event": ["233.233.233.233", 1670],
            "vision": ["233.233.233.233", 41001],
            "debug": ["233.233.233.233", 20001],
        }

        logger = Logger()

        while True:
            message = "msg"
            logger.record(message, tag="vision")
        ```
        :param message: The message content to record.
        :param tag: The tag associated with the message.
        :param source: The source of the message.
        """
        self.logger.record(message, tag, source)

    def list_log_packages(self):
        """
        Lists all available log packages in the log directory and prints them.

        :return: A list of log packages.
        """
        packge = self.logger.list_log_packge()
        print(packge)
        return packge

    def open(self, log_package_path=None):
        """
        Opens a log package for reading. If no path is specified, opens the latest package.

        :param log_package_path: The path to the log package. If None, the latest package is opened.
        :return: An instance of LogReader for the opened log package.
        """
        if log_package_path is None:
            log_package_path = self.logger.list_log_packge()
            if log_package_path:
                log_package_path = log_package_path[0][0]
            else:
                print("No log package found.")
                return None
        return LogReader(f"{self.logger.log_dir}/{log_package_path}")

if __name__ == "__main__":

    udp_dict = {
        "event": ["233.233.233.233", 1670],
        "vision": ["233.233.233.233", 41001],
        "debug": ["233.233.233.233", 20001],
    }

    logger = Logger()

    # while True:
    #     pass