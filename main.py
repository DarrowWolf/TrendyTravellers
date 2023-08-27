import pandas as pd

class VisitorsAnalyticsUtils:
    regions = {
            1: ['Brunei Darussalam', 'Indonesia', 'Malaysia', 'Philippines', 'Thailand', 
                'Viet Nam', 'Myanmar', 'Japan', 'Hong Kong', 'China', 'Taiwan', 
                'Korea, Republic Of', 'India', 'Pakistan', 'Sri Lanka', 'Saudi Arabia', 
                'Kuwait', 'UAE'],
            2: ['United Kingdom', 'Germany', 'France', 'Italy', 'Netherlands', 
                'Greece', 'Belgium & Luxembourg', 'Switzerland', 'Austria', 'Scandinavia', 
                'CIS & Eastern Europe'],
            3: ['USA', 'Canada', 'Australia', 'New Zealand', 'Africa']
        }
    
    def loadDataFile(self, file_path='Int_Monthly_Visitor.csv', print_data=True): # added file path and print_data for unit test
        data = pd.read_csv('Int_Monthly_Visitor.csv', na_values=[' na ']) # Opens csv file and declare ' na ' under na_value
        
        data.columns = [col.strip() for col in data.columns]  # Changes all object dtypes to float
        for col in data.columns[1:]:
            if data[col].dtype == "object":
                data[col] = data[col].str.strip().str.replace(',', '').astype(float)
        
        data = data.fillna(0.0) # Replaces all the 'na' with 0.0
        data.rename(columns={'Unnamed: 0': ''}, inplace=True) # Get rid of first column name
        
        data[''] = data[''].str.strip() # trims data
    
        numerical_columns = data.columns[1:] # Getting all numerical columns after first column
        data[numerical_columns] = data[numerical_columns].apply(pd.to_numeric, errors='coerce') # make everything numeric
        
        data.set_index('', inplace=True) # set first column as the index
        
        if print_data: # if print_data=True it will print this. if False it wont.
            print("*** first 5 rows of data loaded ***")
            print(data.head())
        
        return data
      
    def parseData(self, year_choice, region_choice):
        data = self.loadDataFile()
        
        selected_region = VisitorsAnalyticsUtils.regions[region_choice]
        
        periods = {
            1: (1978, 1987),
            2: (1988, 1997),
            3: (1998, 2007),
            4: (2008, 2017)
        }
        
        # getting start of year and end of year from the selected
        start_year, end_year = periods[year_choice]
        
        data['year'] = data.index.to_series().apply(lambda x: int(x.split()[0])) #exract year from first column
        
        data = data[(data['year'] >= start_year) & (data['year'] <= end_year)]
        data = data[selected_region + ['year']]
        
        for column in selected_region: 
            data[column] = data[column].astype('int64') # converting all columns to int64 type
        
        print("\n*** Parsed Data (Regions) ***")
        print(data.info())
        
        print("\n*** Parsed Data (Years) ***")
        print(data['year'].describe())
        
        return data

    def getTop3Countries(self, data):
        # drop the 'year' column, sum each column, sort the values in descending order,
        # and select the top 3 countries
        top_countries = data.drop(columns=['year']).sum().sort_values(ascending=False).head(3)
        
        print("\n*** Top 3 Countries ***")
        print(top_countries)
        return top_countries

if __name__ == '__main__':
    while True:
        try:
            year_choice = int(input("Enter year period (1: 1978-1987, 2: 1988-1997, 3: 1998-2007, 4: 2008-2017): "))
            if year_choice not in {1, 2, 3, 4}: # Checks if year_choice input is not 1, 2, 3, 4
                raise ValueError("Invalid year choice, please choose the number representing the year period!")

            region_choice = int(input("Enter region (1: Asia, 2: Europe, 3: Others): "))
            if region_choice not in {1, 2, 3}:  # If the year_choice input is 1, 2, 3, 4. It will go to this line to check if the input is not 1, 2, 3
                raise ValueError("Invalid region choice, please choose the number representing the region!")

            break
        except ValueError as ve:
            print(ve) # accuratly prints the error
            continue

    utils = VisitorsAnalyticsUtils()
    parsed_data = utils.parseData(year_choice, region_choice)
    utils.getTop3Countries(parsed_data)

