def test_load_raw_data():
    """Test loading raw data"""
    # Example: Check that the function returns a non-empty result
    data = load_raw_data()
    assert data is not None
def test_save_processed_data(tmp_path):
    """Test saving processed data"""
    import pandas as pd

    # Create sample processed data
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    file_path = tmp_path / "processed.csv"

    # Save the processed data
    save_processed_data(df, file_path)

    # Load the data back and check
    loaded_df = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(df, loaded_df)
