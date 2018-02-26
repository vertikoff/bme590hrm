class ImportCSV:
    def __init__(self, target_csv_path):
        self.target_csv_path = target_csv_path
        self.timestamps = None
        self.voltages = None
        self.import_data()

    def import_data(self):
        import os.path
        import numpy as np
        if(os.path.isfile(self.target_csv_path) and
           self.target_csv_path.endswith('.csv')):
            # CRV - method used here found at:
            data = np.genfromtxt(self.target_csv_path,
                                 delimiter=',',
                                 names=['time', 'voltage'])
            self.timestamps = data['time']
            self.voltages = data['voltage']
        else:
            raise ImportError(self.target_csv_path + ' is not a valid csv')
