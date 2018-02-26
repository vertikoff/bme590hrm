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
        self.import_data()
        self.set_voltage_extremes()
        # self.set_duration()

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
        min_ts = None
        max_ts = None
        for reading in self.list_data:
            ts = float(reading[0])
            if(max_ts is None or ts > max_ts):
                max_ts = ts
            if(min_ts is None or ts < min_ts):
                min_ts = ts
        # CRV - calculating the diff here just incase there is an offset error
        # (earliest ts in data set NOT 0)
        self.duration = max_ts - min_ts
