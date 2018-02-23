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

    def import_data(self):
        from import_csv import ImportCSV
        self.list_data = ImportCSV(self.target_csv_path).data
