class HeartRateMonitor:
    """

    Analyzes ECG data from input .csv file
    :param target_csv_path: location of .csv ECG data
    :attr timstamps: list of timestamps for every data point imported from .csv
    :attr voltages: list of voltages for every data point imported from .csv
    :attr mean_hr_bpm: mean heart rate (bpm). Default: mean over whole data set
    :attr voltage_extremes: tuple (min_voltage, max_voltage)
    :attr duration: length (time) of .csv ECG data
    :attr num_beats: number of beats detected in ECG data
    :attr beats: numpy array of the timestamps when beats occurred
    :attr heart_beat_voltage: array of voltages when beats occurred
    """
    def __init__(self, target_csv_path):
        self.target_csv_path = target_csv_path
        self.timestamps = None
        self.voltages = None
        self.mean_hr_bpm = None
        self.voltage_extremes = None
        self.duration = None
        self.num_beats = None
        self.beats = None
        self.heart_beat_voltage = None
        self.import_data()
        self.set_voltage_extremes()
        self.set_duration()
        self.find_beats()
        self.calc_mean_hr_bpm()
        self.build_json()

    def import_data(self):
        """

        Utilizes the import_csv module to import .csv data
        :sets timestamps: list of all timestamps in .csv data
        :sets voltages: list of all voltages in .csv data
        """
        from import_csv import ImportCSV
        import logging
        logging.basicConfig(filename="logs/heart_rate_monitor_logs.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
        imported_data = ImportCSV(self.target_csv_path)
        self.timestamps = imported_data.timestamps
        self.voltages = imported_data.voltages
        logging.info(self.target_csv_path + ' imported')

    def set_voltage_extremes(self):
        """

        Utilizes the self.voltages data to determine min/max voltages
        :sets voltage_extremes: tuple (min_voltage, max_voltage)
        """
        import logging
        logging.basicConfig(filename="logs/heart_rate_monitor_logs.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
        # CRV init max and min voltage tuple
        min_voltage = min(self.voltages)
        max_voltage = max(self.voltages)
        self.voltage_extremes = (min_voltage, max_voltage)
        logging.info('voltage_extremes tuple set: ' + str(self.voltage_extremes))

    def set_duration(self):
        """

        Utilizes the self.timestamps data to determine data duration
        :sets duration: length (time) of data read
        """
        import logging
        logging.basicConfig(filename="logs/heart_rate_monitor_logs.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
        # CRV init the max and min timestamp
        min_ts = min(self.timestamps)
        max_ts = max(self.timestamps)
        # CRV - calculating the diff here just incase there is an offset error
        # (earliest ts in data set NOT 0)
        self.duration = max_ts - min_ts
        logging.info('duration set: ' + str(self.duration))

    def find_beats(self):
        """

        Identifies beats (as peaks) in the ECG data
        :sets num_beats: number of detected beats in ECG data
        :sets beats: numpy array of timestamps when beats occurred
        """
        import numpy as np
        import peakutils
        import logging
        logging.basicConfig(filename="logs/heart_rate_monitor_logs.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
        threshold = 2 * abs(np.median(self.voltages))
        logging.info('setting threshold to: ' + str(threshold))
        data = np.array(self.voltages)
        # CRV using peakutils lib for peak detection
        # http://peakutils.readthedocs.io/en/latest/index.html
        indexes = peakutils.indexes(data, thres=threshold)
        self.beats = []
        self.heart_beat_voltages = []
        for index in indexes:
            self.beats.append(self.timestamps[index])
            self.heart_beat_voltages.append(self.voltages[index])
        self.num_beats = len(self.beats)
        logging.info('num_beats: ' + str(self.num_beats))
        if(self.num_beats == 0):
            logging.warning('NO BEATS DETECTED')
        # CRV convert list to numpy array
        self.beats = np.array(self.beats)
        logging.info('beats numpy array created')

    def calc_mean_hr_bpm(self, start_ts=None, end_ts=None):
        """

        Calculates the mean heart rate (BPM) over a specified time range
        :param start_ts: start range (seconds)
        :param end_ts: end range (seconds)
        :sets mean_hr_bpm: mean heart rate (BPM) over specified time range
        """
        import logging
        logging.basicConfig(filename="logs/heart_rate_monitor_logs.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
        if(start_ts is None or not self.is_valid_ts(start_ts)):
            start_ts = self.timestamps[0]
            logging.warning('invalid start_ts passed in calc_mean_hr_bpm')
        if(end_ts is None or not self.is_valid_ts(end_ts)):
            end_ts = self.timestamps[-1]
            logging.warning('invalid end_ts passed in calc_mean_hr_bpm')
        num_beats_in_range = 0
        for beat_ts in self.beats:
            if(start_ts <= beat_ts <= end_ts):
                num_beats_in_range += 1
        percentage_of_min = self.calc_percentage_of_min(start_ts, end_ts)
        self.mean_hr_bpm = self.calc_bpm(num_beats_in_range, percentage_of_min)
        logging.info('mean_hr_bpm: ' + str(mean_hr_bpm))

    def is_valid_ts(self, timestamp):
        """

        Determines if the submitted timestamp is within the range of ECG data
        :param timestamp: float or int (seconds)
        :returns Bool: True/False
        """
        min_ts = self.timestamps[0]
        max_ts = self.timestamps[-1]
        if(min_ts <= timestamp <= max_ts):
            return(True)
        else:
            return(False)

    def calc_percentage_of_min(self, start_ts, end_ts):
        """

        Determines percentage of minute for given time range
        :param start_ts: start range (seconds)
        :param end_ts: end range (seconds)
        :returns percentage_of_minute: what percentage of a minute is the range
        :raises TypeError: start_ts and end_ts must be float or int
        """
        import logging
        logging.basicConfig(filename="logs/heart_rate_monitor_logs.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
        if((isinstance(start_ts, int) or isinstance(start_ts, float)) and
           (isinstance(end_ts, int) or isinstance(end_ts, float))):
            return((end_ts - start_ts)/60)
        else:
            logging.warning('invalid ts passed in calc_percentage_of_min')
            raise TypeError('start_ts and end_ts must be float or int')

    def calc_bpm(self, beats, percentage_of_min):
        """

        Determines beats per minute (BPM)
        :param beats: number of beats
        :param percentage_of_min: percentage of min over range beats occurred
        :returns bpm: heart rate BPM
        :raises TypeError: beats and percentage_of_min must be float or int
        """
        import logging
        logging.basicConfig(filename="logs/heart_rate_monitor_logs.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
        if((isinstance(beats, int) or isinstance(beats, float)) and
           (isinstance(percentage_of_min, int) or
           isinstance(percentage_of_min, float))):
            return(beats/percentage_of_min)
        else:
            logging.warning('invalid beats or perc. of min passed in calc_bpm')
            raise TypeError('beats and percentage_of_min must be float or int')

    def build_json(self):
        """

        Creates and outputs .json file with ECG analysis
        """
        import json
        import os
        data = {}
        data['mean_hr_bpm'] = self.mean_hr_bpm
        data['voltage_extremes'] = self.voltage_extremes
        data['duration'] = self.duration
        data['num_beats'] = self.num_beats
        data['beats'] = self.beats.tolist()
        json_data = json.dumps(data)
        csv_filename = os.path.basename(self.target_csv_path)
        json_filename = self.swap_csv_for_json_file_extension(csv_filename)
        self.create_and_write_json_file(json_filename, json_data)

    def create_and_write_json_file(self, filename, contents):
        """

        Creates json file
        :param filename: target filename
        :contents: file contents to be written
        """
        import logging
        logging.basicConfig(filename="logs/heart_rate_monitor_logs.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
        import json
        path_for_json_output = 'output_json_files/'
        new_file_dest = path_for_json_output + filename
        self.remove_file_from_dir_before_creating(new_file_dest)
        with open(new_file_dest, 'w') as new_json_file:
            json.dump(contents, new_json_file)
        logging.info('json file written to: ' + path_for_json_output)

    def remove_file_from_dir_before_creating(self, filename):
        """

        Removes file if it exists
        :param filename: target filename
        """
        import logging
        logging.basicConfig(filename="logs/heart_rate_monitor_logs.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
        import os
        if(os.path.isfile(filename)):
            os.remove(filename)
            logging.info('removing ' + filename)

    def swap_csv_for_json_file_extension(self, filename):
        """

        Creates new file name with .json extension
        :param filename: target filename (expects .csv)
        :returns json_filename: target_filename (.json)
        """
        return(filename.replace('.csv', '.json'))
