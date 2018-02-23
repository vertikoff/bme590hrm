class ImportCSV:
    def __init__(self, target_csv_path):
        self.target_csv_path = target_csv_path
        self.data = None
        self.import_data()

    def import_data(self):
        import csv
        import os.path
        if(os.path.isfile(self.target_csv_path) not True):
            raise ImportError("no file at: " + self.target_csv_path)
        if(target_csv_path.endswith('.csv') not True):
            raise ImportError(self.target_csv_path + ' is not type .csv')
        # CRV - method used here found at:
        # https://stackoverflow.com/questions/24662571/python-import-csv-to-list
        with open(self.target_csv_path, 'r') as f:
            reader = csv.reader(f)
            list_data = list(reader)
        self.data = list_data
