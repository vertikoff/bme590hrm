class HeartRateMonitor:
    def __init__(self, target_csv_path):
        self.target_csv_path = target_csv_path
        self.list_data = None
        self.mean_hr_bpm = None
        self.voltage_extremes = None
        self.duration = None
        self.num_beats = None
        self.beats = None
        self.import_data()
        self.set_voltage_extremes()

    def import_data(self):
        from import_csv import ImportCSV
        self.list_data = ImportCSV(self.target_csv_path).data

    def set_voltage_extremes(self):
        # CRV init max and min voltage tuple
        min_voltage = None
        max_voltage = None
        for reading in self.list_data:
            if(max_voltage == None or reading[1] > max_voltage):
                max_voltage = reading[1]
            if(min_voltage == None or reading[1] < min_voltage):
                min_voltage = reading[1]
        self.voltage_extremes = (min_voltage, max_voltage)
