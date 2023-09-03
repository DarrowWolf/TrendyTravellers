import unittest
import pandas as pd
from main import DataLoader # import the DataLoader class from main.py

class TestDataLoader(unittest.TestCase):
    # test the loadDataFile function
    def test_loadDataFile(self):
        data_loader = DataLoader()
        data = data_loader.loadDataFile(print_data=False)
        
        # expected data
        expected_data = pd.read_csv('Int_Monthly_Visitor.csv')
        expected_rows, expected_columns = expected_data.shape[0], expected_data.shape[1] - 1 # subtract 1 for the index column because the first column header is empty.
        
        # actual data from the loadDataFile func in main.py
        actual_rows, actual_columns = data.shape
        
        self.assertEqual(actual_rows, expected_rows) # compares the rows taken using the loadDataFile func with the rows directly from the CSV
        self.assertEqual(actual_columns, expected_columns) # does the same as above
        
        print("\nExpected Number of Columns:", expected_columns)
        print("Actual Number of Columns:", actual_columns)
        
        print("\nExpected Number of Rows:", expected_rows)
        print("Actual Number of Rows:", actual_rows)

if __name__ == '__main__':
    unittest.main()
