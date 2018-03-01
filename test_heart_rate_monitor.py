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
    import pytest
    from heart_rate_monitor import HeartRateMonitor
    a = HeartRateMonitor('test_data/test_data1.csv').duration
    assert a == 27.775

    with pytest.raises(ImportError):
        HeartRateMonitor('fake_dir/not_real.csv').duration


def test_find_beats():
    import pytest
    from heart_rate_monitor import HeartRateMonitor
    a = HeartRateMonitor('test_data/test_data1.csv').num_beats
    assert a == 35

    with pytest.raises(ImportError):
        HeartRateMonitor('fake_dir/not_real.csv').num_beats


def test_is_valid_ts():
    import pytest
    from heart_rate_monitor import HeartRateMonitor
    a = HeartRateMonitor('test_data/test_data1.csv')
    b = a.is_valid_ts(15.5)
    c = a.is_valid_ts(150000.6)
    d = a.is_valid_ts(0)
    assert b == True
    assert c == False
    assert d == True
