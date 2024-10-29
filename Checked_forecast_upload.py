# import pandas as pd
# from sqlalchemy import create_engine
# import sys

# Report_Category = sys.argv[1] 
# input_file = sys.argv[2]  # Add this line to get the file path from Jenkins

# # Report_Category = "Best_Case"
# if Report_Category == "Best_Case":

#     username = 'admin'
#     password = 'Fcm5KXrivyKqjo3NX3Nf'
#     database_name = 'best_case_pipeline_trials'
#     host = 'bankruptcy-dev.cyuqumrrkocs.ap-south-1.rds.amazonaws.com' 
#     port = '3306'

#     # Create database engine
#     engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}')

#     query_Chapter = """
#     SELECT * FROM Chapter_Mapping;
#     """
#     query_State = """
#     SELECT * FROM State_Mapping;
#     """
#     query_District = """
#     SELECT * FROM District_Mapping;
#     """

#     try:
#         Chapter_Mapping = pd.read_sql(query_Chapter, engine)
#         print("Data loaded from weekly_data_for_trials table:")
#         print(Chapter_Mapping.head())
#     except Exception as e:
#         raise ValueError(f"An error occurred while loading data from weekly_data_for_trials: {e}")

#     try:
#         State_Mapping = pd.read_sql(query_State, engine)
#         print("Data loaded from weekly_data_for_trials table:")
#         print(State_Mapping.head())
#     except Exception as e:
#         raise ValueError(f"An error occurred while loading data from weekly_data_for_trials: {e}")

#     try:
#         Court_Mapping = pd.read_sql(query_District, engine)
#         print("Data loaded from weekly_data_for_trials table:")
#         print(Court_Mapping.head())
#     except Exception as e:
#         raise ValueError(f"An error occurred while loading data from weekly_data_for_trials: {e}")
    
#     def load_excel_data(file_path):
#         return pd.read_excel(file_path)

#     def create_mapping_dictionaries(chapter_mapping, district_mapping, state_mapping):
#         chapter_id_map = dict(zip(chapter_mapping['Chapter'], chapter_mapping['chapter_id']))
#         district_id_map = dict(zip(district_mapping['Federal Court District'], district_mapping['district_id']))
#         state_id_map = dict(zip(state_mapping['StateCode'], state_mapping['state_id']))
#         return chapter_id_map, district_id_map, state_id_map

#     def transform_and_map_data(data, chapter_id_map, district_id_map, state_id_map):
#         data_long = pd.melt(data, id_vars=['Chapter', 'StateCode', 'Federal Court District','Case Type'],
#                             var_name='weekly_date', value_name='total_filings')
        
#         data_long['chapter_id'] = data_long['Chapter'].map(chapter_id_map)
#         data_long['district_id'] = data_long['Federal Court District'].map(district_id_map)
#         data_long['state_id'] = data_long['StateCode'].map(state_id_map)
        
#         data_long.drop(columns=['Chapter', 'Federal Court District', 'StateCode'], inplace=True)
        
#         return data_long

#     # Replace hardcoded file path with input_file parameter
#     # file_path = 'Best_Case_Forecast_Report_101924_UI_Raw.xlsx'  # Remove this line
#     data = load_excel_data(input_file)  # Use input_file instead

#     chapter_mapping = Chapter_Mapping
#     district_mapping = Court_Mapping
#     state_mapping = State_Mapping

#     chapter_id_map, district_id_map, state_id_map = create_mapping_dictionaries(chapter_mapping, district_mapping, state_mapping)

#     transformed_data = transform_and_map_data(data, chapter_id_map, district_id_map, state_id_map)

#     transformed_data = transformed_data[['state_id', 'district_id', 'chapter_id', 'weekly_date', 'total_filings','Case Type']]
#     transformed_data.rename(columns={'Case Type':'case_type'},inplace=True)
#     print(transformed_data.head(10))

#     report_date = data.columns.to_list()[-16].date()

#     output_path = f'Best_Case_final_file_{report_date}.csv'
#     transformed_data.to_csv(output_path, index=False)

#     fcst_data = transformed_data[transformed_data["weekly_date"]>=data.columns.to_list()[-16]]

#     fcst_data = pd.merge(fcst_data,Chapter_Mapping,on="chapter_id",how="left")

#     fcst_data = pd.merge(fcst_data,State_Mapping,on="state_id",how="left")
#     fcst_data = pd.merge(fcst_data,Court_Mapping,on="district_id",how="left")

#     import datetime

#     # Get today's date
#     today = datetime.date.today()

#     # Get the current year
#     current_year = today.year

#     # Week number with Sunday as the first day of the week
#     week_number_U = int(today.strftime("%U"))

#     # Week number with Monday as the first day of the week
#     week_number_W = today.strftime("%W")

#     fcst_data["week_no"] = week_number_U -1
#     fcst_data["year"] = current_year
#     fcst_data["forecast_week"] = report_date

#     fcst_data.rename(columns = {"weekly_date":"week","total_filings":"value"},inplace=True)

#     fcst_data = fcst_data[['Chapter', 'StateCode', 'Federal Court District', 'chapter_id',
#        'state_id', 'district_id', 'case_type', 'week', 'week_no', 'year',
#        'value', 'forecast_week']]
    
#     fcst_data.to_csv(f"Best_Case_forecast_{report_date}.csv")

import os
import sys
import pandas as pd
from sqlalchemy import create_engine
import datetime

# Get command-line arguments
Report_Category = sys.argv[1]
input_file = sys.argv[2]

# Print input parameters for debugging
print(f"Report_Category: {Report_Category}")
print(f"Input file path received: {input_file}")
print(f"Current working directory: {os.getcwd()}")

# Check if the input file exists
if not os.path.isfile(input_file):
    raise FileNotFoundError(f"The input file was not found: {input_file}")

# Report_Category Processing
if Report_Category == "Best_Case":
    # Database credentials (replace with your actual credentials or use environment variables)
    username = 'admin'
    password = 'YOUR_PASSWORD_HERE'  # Masked for security
    database_name = 'best_case_pipeline_trials'
    host = 'bankruptcy-dev.cyuqumrrkocs.ap-south-1.rds.amazonaws.com'
    port = '3306'

    # Create database engine
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}')

    # SQL queries
    query_Chapter = "SELECT * FROM Chapter_Mapping;"
    query_State = "SELECT * FROM State_Mapping;"
    query_District = "SELECT * FROM District_Mapping;"

    # Load mapping tables with error handling
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
            data = pd.read_excel(file_path)
            print("Excel data loaded successfully.")
            return data
        except Exception as e:
            raise ValueError(f"An error occurred while loading the Excel file: {e}")

    # Create mapping dictionaries
    def create_mapping_dictionaries(chapter_mapping, district_mapping, state_mapping):
        chapter_id_map = dict(zip(chapter_mapping['Chapter'], chapter_mapping['chapter_id']))
        district_id_map = dict(zip(district_mapping['Federal Court District'], district_mapping['district_id']))
        state_id_map = dict(zip(state_mapping['StateCode'], state_mapping['state_id']))
        return chapter_id_map, district_id_map, state_id_map

    # Transform and map data
    def transform_and_map_data(data, chapter_id_map, district_id_map, state_id_map):
        data_long = pd.melt(
            data,
            id_vars=['Chapter', 'StateCode', 'Federal Court District', 'Case Type'],
            var_name='weekly_date',
            value_name='total_filings'
        )

        data_long['chapter_id'] = data_long['Chapter'].map(chapter_id_map)
        data_long['district_id'] = data_long['Federal Court District'].map(district_id_map)
        data_long['state_id'] = data_long['StateCode'].map(state_id_map)

        data_long.drop(columns=['Chapter', 'Federal Court District', 'StateCode'], inplace=True)

        return data_long

    # Load and process the Excel data
    data = load_excel_data(input_file)

    # Ensure required columns are present
    required_columns = ['Chapter', 'StateCode', 'Federal Court District', 'Case Type']
    if not all(column in data.columns for column in required_columns):
        missing_cols = set(required_columns) - set(data.columns)
        raise ValueError(f"Missing required columns in the input file: {missing_cols}")

    chapter_id_map, district_id_map, state_id_map = create_mapping_dictionaries(
        Chapter_Mapping, Court_Mapping, State_Mapping
    )

    transformed_data = transform_and_map_data(data, chapter_id_map, district_id_map, state_id_map)

    transformed_data = transformed_data[['state_id', 'district_id', 'chapter_id', 'weekly_date', 'total_filings', 'Case Type']]
    transformed_data.rename(columns={'Case Type': 'case_type'}, inplace=True)
    print("Transformed data preview:")
    print(transformed_data.head(10))

    # Extract report date from the data columns
    try:
        # Assuming the 16th column from the end contains the date in datetime format
        report_date_column = data.columns.to_list()[-16]
        if isinstance(report_date_column, datetime.datetime):
            report_date = report_date_column.date()
        else:
            # If the column name is a string, parse it into a date
            report_date = datetime.datetime.strptime(str(report_date_column), '%Y-%m-%d').date()
    except Exception as e:
        raise ValueError(f"An error occurred while extracting the report date: {e}")

    output_path = f'Best_Case_final_file_{report_date}.csv'
    transformed_data.to_csv(output_path, index=False)
    print(f"Transformed data saved to {output_path}")

    # Filter forecast data
    fcst_data = transformed_data[transformed_data["weekly_date"] >= data.columns.to_list()[-16]]

    # Merge mapping data
    fcst_data = pd.merge(fcst_data, Chapter_Mapping, on="chapter_id", how="left")
    fcst_data = pd.merge(fcst_data, State_Mapping, on="state_id", how="left")
    fcst_data = pd.merge(fcst_data, Court_Mapping, on="district_id", how="left")

    # Get current date and week number
    today = datetime.date.today()
    current_year = today.year
    week_number_U = int(today.strftime("%U"))
    fcst_data["week_no"] = week_number_U - 1
    fcst_data["year"] = current_year
    fcst_data["forecast_week"] = report_date

    fcst_data.rename(columns={"weekly_date": "week", "total_filings": "value"}, inplace=True)

    fcst_data = fcst_data[['Chapter', 'StateCode', 'Federal Court District', 'chapter_id',
                           'state_id', 'district_id', 'case_type', 'week', 'week_no', 'year',
                           'value', 'forecast_week']]

    forecast_output_path = f"Best_Case_forecast_{report_date}.csv"
    fcst_data.to_csv(forecast_output_path, index=False)
    print(f"Forecast data saved to {forecast_output_path}")

else:
    raise ValueError(f"Unsupported Report_Category: {Report_Category}")
