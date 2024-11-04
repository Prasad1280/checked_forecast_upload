import pandas as pd
from sqlalchemy import create_engine
import sys
import datetime
import os

print("Current working directory:", os.getcwd())

# Print all file names in the current working directory
print("Files in the current working directory:")
for filename in os.listdir('.'):
    print(filename)

# Assign arguments to variables
Report_Category = sys.argv[1]

if Report_Category == "Best_Case":
    # Database credentials and connection details
    # It's recommended to use environment variables or a configuration file for credentials
    username = "admin"  # Replace with your method of securely fetching the username
    password = "Fcm5KXrivyKqjo3NX3Nf"  # Replace with your method of securely fetching the password
    database_name = 'best_case_pipeline_trials'
    host = 'bankruptcy-dev.cyuqumrrkocs.ap-south-1.rds.amazonaws.com'
    port = '3306'

    # Ensure that credentials are provided
    if not username or not password:
        raise ValueError("Database credentials are not set. Please set DB_USERNAME and DB_PASSWORD environment variables.")

    # Create database engine
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}')

    # SQL queries
    query_Chapter = "SELECT * FROM Chapter_Mapping;"
    query_State = "SELECT * FROM State_Mapping;"
    query_District = "SELECT * FROM District_Mapping;"

    # Load data from the database
    try:
        Chapter_Mapping = pd.read_sql(query_Chapter, engine)
        print("Data loaded from Chapter_Mapping table:")
        print(Chapter_Mapping.head())
    except Exception as e:
        raise ValueError(f"An error occurred while loading data from Chapter_Mapping: {e}")

    try:
        State_Mapping = pd.read_sql(query_State, engine)
        print("Data loaded from State_Mapping table:")
        print(State_Mapping.head())
    except Exception as e:
        raise ValueError(f"An error occurred while loading data from State_Mapping: {e}")

    try:
        Court_Mapping = pd.read_sql(query_District, engine)
        print("Data loaded from District_Mapping table:")
        print(Court_Mapping.head())
    except Exception as e:
        raise ValueError(f"An error occurred while loading data from District_Mapping: {e}")

    # Function to load Excel data
    def load_excel_data(file_path):
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            raise ValueError(f"An error occurred while loading the Excel file: {e}")

    # Function to create mapping dictionaries
    def create_mapping_dictionaries(chapter_mapping, district_mapping, state_mapping):
        chapter_id_map = dict(zip(chapter_mapping['Chapter'], chapter_mapping['chapter_id']))
        district_id_map = dict(zip(district_mapping['Federal Court District'], district_mapping['district_id']))
        state_id_map = dict(zip(state_mapping['StateCode'], state_mapping['state_id']))
        return chapter_id_map, district_id_map, state_id_map

    # Function to transform and map data
    def transform_and_map_data(data, chapter_id_map, district_id_map, state_id_map):
        data_long = pd.melt(data, id_vars=['Chapter', 'StateCode', 'Federal Court District', 'Case Type'],
                            var_name='weekly_date', value_name='total_filings')
        
        data_long['chapter_id'] = data_long['Chapter'].map(chapter_id_map)
        data_long['district_id'] = data_long['Federal Court District'].map(district_id_map)
        data_long['state_id'] = data_long['StateCode'].map(state_id_map)
        
        data_long.drop(columns=['Chapter', 'Federal Court District', 'StateCode'], inplace=True)
        
        return data_long

    # Load data from Excel file
    file_path = "input_file.xlsx"
    data = load_excel_data(file_path)

    # Create mapping dictionaries
    chapter_mapping = Chapter_Mapping
    district_mapping = Court_Mapping
    state_mapping = State_Mapping

    chapter_id_map, district_id_map, state_id_map = create_mapping_dictionaries(chapter_mapping, district_mapping, state_mapping)

    # Transform and map data
    transformed_data = transform_and_map_data(data, chapter_id_map, district_id_map, state_id_map)

    transformed_data = transformed_data[['state_id', 'district_id', 'chapter_id', 'weekly_date', 'total_filings', 'Case Type']]
    transformed_data.rename(columns={'Case Type': 'case_type'}, inplace=True)
    print(transformed_data.head(10))

    # Extract report date
    try:
        report_date = pd.to_datetime(data.columns.to_list()[-16]).date()
    except Exception as e:
        raise ValueError(f"An error occurred while extracting the report date: {e}")

    # Save transformed data to CSV
    output_path = f'{Report_Category}_final_file_{report_date}.csv'
    transformed_data.to_csv(output_path, index=False)

    # Filter forecast data
    fcst_data = transformed_data[transformed_data["weekly_date"] >= data.columns.to_list()[-16]]

    # Merge data with mappings
    fcst_data = pd.merge(fcst_data, Chapter_Mapping, on="chapter_id", how="left")
    fcst_data = pd.merge(fcst_data, State_Mapping, on="state_id", how="left")
    fcst_data = pd.merge(fcst_data, Court_Mapping, on="district_id", how="left")

    # Get today's date and week number
    today = datetime.date.today()
    current_year = today.year
    week_number_U = int(today.strftime("%U"))

    # Adjust week number if necessary
    fcst_data["week_no"] = week_number_U - 1
    fcst_data["year"] = current_year
    fcst_data["forecast_week"] = report_date

    # Rename columns
    fcst_data.rename(columns={"weekly_date": "week", "total_filings": "value"}, inplace=True)

    # Select final columns
    fcst_data = fcst_data[['Chapter', 'StateCode', 'Federal Court District', 'chapter_id',
                        'state_id', 'district_id', 'case_type', 'week', 'week_no', 'year',
                        'value', 'forecast_week']]

    # Save forecast data to CSV
    forecast_output_path = f"{Report_Category}_forecast_{report_date}.csv"
    fcst_data.to_csv(forecast_output_path, index=False)
