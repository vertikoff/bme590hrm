class HeartRateMonitor:
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

    def import_data(self):
        from import_csv import ImportCSV
        imported_data = ImportCSV(self.target_csv_path)
        self.timestamps = imported_data.timestamps
        self.voltages = imported_data.voltages

    def set_voltage_extremes(self):
        # CRV init max and min voltage tuple
        min_voltage = min(self.voltages)
        max_voltage = max(self.voltages)
        self.voltage_extremes = (min_voltage, max_voltage)

    def set_duration(self):
        # CRV init the max and min timestamp
        min_ts = min(self.timestamps)
        max_ts = max(self.timestamps)
        # CRV - calculating the diff here just incase there is an offset error
        # (earliest ts in data set NOT 0)
        self.duration = max_ts - min_ts

    def find_beats(self):
        import numpy as np
        import peakutils
        threshold = 2 * abs(np.median(self.voltages))
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
        # CRV convert list to numpy array
        self.beats = np.array(self.beats)
    #
    # def mean_hr_bpm(start_ts = None, end_ts = None):
    #     if(start_ts is None):
    #         start_ts = self.timestamps[0]
    #

    def is_valid_ts(self, timestamp):
        min_ts = self.timestamps[0]
        max_ts = self.timestamps[-1]
        if(min_ts <= timestamp <= max_ts):
            return(True)
        else:
            return(False)
