def test_import_csv():
    import pytest
    from import_csv import ImportCSV
    with pytest.raises(ImportError):
        ImportCSV('fake_dir/not_real.csv')
    with pytest.raises(ImportError):
        ImportCSV('not_csv.txt')
