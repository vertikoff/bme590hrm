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
        self.calc_mean_hr_bpm()

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

    def calc_mean_hr_bpm(self, start_ts=None, end_ts=None):
        if(start_ts is None or not self.is_valid_ts(start_ts)):
            start_ts = self.timestamps[0]
        if(end_ts is None or not self.is_valid_ts(end_ts)):
            end_ts = self.timestamps[-1]
        num_beats_in_range = 0
        for beat_ts in self.beats:
            if(start_ts <= beat_ts <= end_ts):
                num_beats_in_range += 1
        percentage_of_min = self.calc_percentage_of_min(start_ts, end_ts)
        self.mean_hr_bpm = self.calc_bpm(num_beats_in_range, percentage_of_min)

    def is_valid_ts(self, timestamp):
        min_ts = self.timestamps[0]
        max_ts = self.timestamps[-1]
        if(min_ts <= timestamp <= max_ts):
            return(True)
        else:
            return(False)

    def calc_percentage_of_min(self, start_ts, end_ts):
        if((isinstance(start_ts, int) or isinstance(start_ts, float)) and
           (isinstance(end_ts, int) or isinstance(end_ts, float))):
            return((end_ts - start_ts)/60)
        else:
            raise TypeError('start_ts and end_ts must be float or int')

    def calc_bpm(self, beats, percentage_of_min):
        if((isinstance(beats, int) or isinstance(beats, float)) and
           (isinstance(percentage_of_min, int) or
            isinstance(percentage_of_min, float))):
            return(beats/percentage_of_min)
        else:
            raise TypeError('beats and percentage_of_min must be float or int')
