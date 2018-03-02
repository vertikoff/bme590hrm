class ImportCSV:
    """

    Imports .csv data

    :param target_csv_path: path for .csv data
    :attr target_csv_path: path imported .csv data came from
    :attr timestamps: list of timestamps pulled from .csv data
    :attr voltages: list of voltages pulled from .csv data
    """
    def __init__(self, target_csv_path):
        self.target_csv_path = target_csv_path
        self.timestamps = None
        self.voltages = None
        self.import_data()

    def import_data(self):
        """

        Imports .csv data (worker function)
        
        :sets timestamps: list of timestamps pulled from .csv data
        :sets voltages: list of voltages pulled from .csv data
        :raises ImportError: [.csv] is not a valid csv
        """
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
