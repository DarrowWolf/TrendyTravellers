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
    
    def loadDataFile(self):
        data = pd.read_csv('Int_Monthly_Visitor.csv', na_values=[' na ']) #Opens csv file and declare ' na ' under na_value
        
        data.columns = [col.strip() for col in data.columns]  #Changes all object dtypes to float
        for col in data.columns[1:]:
            if data[col].dtype == "object":
                data[col] = data[col].str.strip().str.replace(',', '').astype(float)
        
        data = data.fillna(0.0) #Replaces all the 'na' with 0.0
        data.rename(columns={'Unnamed: 0': ''}, inplace=True) #Get rid of first column name
        
        data[''] = data[''].str.strip() #trims data
    
        numerical_columns = data.columns[1:] #Getting all numerical columns after first column
        data[numerical_columns] = data[numerical_columns].apply(pd.to_numeric, errors='coerce') # make everything numeric
        
        data.set_index('', inplace=True) # set first column as the index
        
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
        
        start_year, end_year = periods[year_choice]
        
        data['year'] = data.index.to_series().apply(lambda x: int(x.split()[0])) #exract year from first column
        
        data = data[(data['year'] >= start_year) & (data['year'] <= end_year)]
        data = data[selected_region + ['year']]
        
        for column in selected_region:
            data[column] = data[column].astype('int64')
        
        print("\n*** Parsed Data (Regions) ***")
        print(data.info())
        
        print("\n*** Parsed Data (Years) ***")
        print(data['year'].describe())
        
        return data

    def getTop3Countries(self, parsed_data, year_choice, region_choice):
        selected_region = VisitorsAnalyticsUtils.regions[region_choice]

        print("\nTop 3 countries")

        # Create a new column for the sum of values across the selected region for each row
        parsed_data['Sum'] = parsed_data[selected_region].sum(axis=1)

        # Get the top 3 countries based on the sum column
        top_countries = parsed_data.nlargest(3, 'Sum')

        for index, row in top_countries.iterrows():
            print("\nCountry:",row['Sum'])

def main():
    year_choice = 0
    region_choice = 0
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
            print(ve)
            continue

    # Made it easier to read this way
    utils = VisitorsAnalyticsUtils()
    parsed_data = utils.parseData(year_choice, region_choice)
    utils.getTop3Countries(parsed_data, year_choice, region_choice)
    
if __name__ == '__main__':
    main()

