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
    assert b is True
    assert c is False
    assert d is True


def test_calc_mean_hr_bpm():
    import pytest
    from heart_rate_monitor import HeartRateMonitor
    a = HeartRateMonitor('test_data/test_data1.csv').mean_hr_bpm
    assert a == 75.60756075607561

    with pytest.raises(ImportError):
        HeartRateMonitor('fake_dir/not_real.csv').num_beats


def test_calc_percentage_of_min():
    import pytest
    from heart_rate_monitor import HeartRateMonitor
    a = HeartRateMonitor('test_data/test_data1.csv')
    b = a.calc_percentage_of_min(0, 60)
    c = a.calc_percentage_of_min(15, 30)
    d = a.calc_percentage_of_min(15, 90)
    assert b == 1.0
    assert c == 0.25
    assert d == 1.25

    with pytest.raises(TypeError):
        a.calc_percentage_of_min('start', 45)


def test_calc_bpm():
    import pytest
    from heart_rate_monitor import HeartRateMonitor
    a = HeartRateMonitor('test_data/test_data1.csv')
    b = a.calc_bpm(10, 1.0)
    c = a.calc_bpm(15, 0.5)
    d = a.calc_bpm(90, 1.5)
    assert b == 10
    assert c == 30
    assert d == 60

    with pytest.raises(TypeError):
        a.calc_bpm('start', 45)


def test_build_json():
    import pytest
    import os
    from heart_rate_monitor import HeartRateMonitor
    json_results_path = 'output_json_files/test_data1.json'
    if(os.path.isfile(json_results_path)):
        os.remove(json_results_path) 
    json_present_at_start = os.path.isfile(json_results_path)
    a = HeartRateMonitor('test_data/test_data1.csv')
    json_present_after_init = os.path.isfile(json_results_path)
    assert json_present_at_start is False
    assert json_present_after_init is True
