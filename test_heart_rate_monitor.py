def test_import_csv():
    import pytest
    from import_csv import ImportCSV
    with pytest.raises(ImportError):
        ImportCSV('fake_dir/not_real.csv')
    with pytest.raises(ImportError):
        ImportCSV('not_csv.txt')


def test_voltage_extremes():
    import pytest
    from heart_rate_monitor import HeartRateMonitor
    a = HeartRateMonitor('test_data/test_data1.csv').voltage_extremes
    assert a == (-0.68, 1.05)

    with pytest.raises(ImportError):
        HeartRateMonitor('fake_dir/not_real.csv').voltage_extremes


def test_duration():
    pass
    # import pytest
    # from heart_rate_monitor import HeartRateMonitor
    # a = HeartRateMonitor('test_data/test_data1.csv').duration
    # assert a == 27.775
    #
    # with pytest.raises(ImportError):
    #     HeartRateMonitor('fake_dir/not_real.csv').duration
