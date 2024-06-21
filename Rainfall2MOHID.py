import csv
import os
import sys
import re
from datetime import datetime
import time

def print_separator1():
    print("=" * 80)

def print_separator2():
    print("-" * 80)
    
def print_header():
    print_separator1()
    print("Welcome to the Rainfall2MOHID: Hourly Rainfall Data to MOHID FillMatrix Converter")
    print("Version: 1.0")
    print("Language: Python 3")
    print("Date: June 2024")
    print("Author: Dhiego da Silva Sales")
    print("Credentials: Geographer, MSc in Environmental Engineering")
    print("Affiliation: Instituto Federal Fluminense")
    print("Contact: dhiego.sales@outlook.com\n")
    print("Description: This program converts hourly rainfall data from different rain gauge stations into SRM format files compatible with the FillMatrix tool, creating an HDF5 rainfall file with spatial and temporal variation to be used in hydrological modeling with MOHID-Land.")
    print_separator1()

def get_current_directory():
    print("Identifying the current directory...")
    time.sleep(3)
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    print_separator2()
    time.sleep(2)
    return current_dir

def check_fillmatrix_exe():
    print("Locating FillMatrix.exe in the current directory...")
    time.sleep(3)

    exe_file = os.path.join(os.getcwd(), 'FillMatrix.exe')
    if not os.path.isfile(exe_file):
        print("Erro 1: FillMatrix.exe not found in the current directory.")
        print("It is mandatory that the Rainfall2MOHID executable is in the same folder as FillMatrix.exe.")
        print("The program will exit in 30 seconds if FillMatrix.exe is not located.")
        
        for remaining in range(30, 0, -1):
            sys.stdout.write(f"\rProgram will exit in {remaining} seconds...")
            sys.stdout.flush()
            time.sleep(1)
        print("\rProgram exited.")
        sys.exit(1)
    
    print("FillMatrix.exe located successfully.")
    print_separator2()
    time.sleep(2)

def check_csv_file(filename):
    print(f"Locating file '{filename}' in the current directory...")
    time.sleep(3)

    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    if not os.path.isfile(file_path):
        print(f"Erro 2: File '{filename}' not found in the current directory.")
        print(f"The program will exit in 30 seconds if '{filename}' is not located.")
        
        for remaining in range(30, 0, -1):
            sys.stdout.write(f"\rProgram will exit in {remaining} seconds...")
            sys.stdout.flush()
            time.sleep(1)
        print("\rProgram exited.")
        sys.exit(1)
    
    print(f"{filename} located successfully.")
    print_separator2()
    time.sleep(2)

def check_dat_file():
    print("Locating topography.dat in the current directory...")
    time.sleep(3)

    dat_file = os.path.join(os.getcwd(), 'topography.dat')
    if not os.path.isfile(dat_file):
        print("Erro 3: topography.dat not found in the current directory.")
        print("It is mandatory that the Rainfall2MOHID executable is in the same folder as topography.dat.")
        print("The program will exit in 30 seconds if topography.dat is not located.")
        
        for remaining in range(30, 0, -1):
            sys.stdout.write(f"\rProgram will exit in {remaining} seconds...")
            sys.stdout.flush()
            time.sleep(1)
        print("\rProgram exited.")
        sys.exit(1)
    
    print("topography.dat located successfully.")
    print_separator2()
    time.sleep(2)

def validate_coordinates_file(coordinates_file):
    print("Validating the coordinates file...")
    time.sleep(3)
    with open(coordinates_file, 'r', newline='') as coord_file:
        coord_reader = csv.reader(coord_file, delimiter=';')
        coordinates_data = list(coord_reader)
       # validate_coordinates_file(coordinates_data)
        
    headers = coordinates_data[0]
    if headers[1] != "COORD_Y" or headers[2] != "COORD_X":
        print("Erro 4: The header of the coordinates.csv file is not in the required format.")
        print("Please consult the documentation.")
        for remaining in range(30, 0, -1):
            sys.stdout.write(f"\rProgram will exit in {remaining} seconds...")
            sys.stdout.flush()
            time.sleep(1)
        print("\rProgram exited.")
        sys.exit(1)
    
    print("The second column is latitude and the third column is longitude.")
    time.sleep(2)

    for row in coordinates_data[1:]:
        if not row[1] or not row[2]:
            print("Erro 5: Found empty cells in the coordinate columns.")
            print("Missing coordinate values are not allowed.")
            for remaining in range(30, 0, -1):
                sys.stdout.write(f"\rProgram will exit in {remaining} seconds...")
                sys.stdout.flush()
                time.sleep(1)
            print("\rProgram exited.")
            sys.exit(1)
        
        try:
            float(row[1])
            float(row[2])
        except ValueError:
            print("Erro 6: Found non-numeric values in the coordinate columns.")
            print("Only integer or float values are allowed.")
            for remaining in range(30, 0, -1):
                sys.stdout.write(f"\rProgram will exit in {remaining} seconds...")
                sys.stdout.flush()
                time.sleep(1)
            print("\rProgram exited.")
            sys.exit(1)
    
    print("All coordinate values are present and valid.")
    print_separator2()
    time.sleep(2)

def validate_hourly_rainfall_file(data):
    print("Validating the hourly rainfall file...")
    time.sleep(3)

    date_pattern = re.compile(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}")
    
    for row in data[1:]:
        date_str = row[0]
        if not date_pattern.match(date_str):
            print(f"Erro 7: Date format is incorrect for entry: {date_str}")
            for remaining in range(30, 0, -1):
                sys.stdout.write(f"\rProgram will exit in {remaining} seconds...")
                sys.stdout.flush()
                time.sleep(1)
            print("\rProgram exited.")
            sys.exit(1)

    print("All dates are in the correct format.")
    time.sleep(2)

    for row in data[1:]:
        for value in row[1:]:
            if value == "":
                print("Erro 8: Found empty cells in the rainfall data columns.")
                print("Missing rainfall values are not allowed.")
                for remaining in range(30, 0, -1):
                    sys.stdout.write(f"\rProgram will exit in {remaining} seconds...")
                    sys.stdout.flush()
                    time.sleep(1)
                print("\rProgram exited.")
                sys.exit(1)
            
            try:
                num_value = float(value)
                if num_value < 0:
                    print("Erro 9: Found negative values in the rainfall data columns.")
                    print("Only positive values are allowed.")
                    for remaining in range(30, 0, -1):
                        sys.stdout.write(f"\rProgram will exit in {remaining} seconds...")
                        sys.stdout.flush()
                        time.sleep(1)
                    print("\rProgram exited.")
                    sys.exit(1)
            except ValueError:
                print("Erro 10: Found non-numeric values in the rainfall data columns.")
                print("Only integer or float values are allowed.")
                for remaining in range(30, 0, -1):
                    sys.stdout.write(f"\rProgram will exit in {remaining} seconds...")
                    sys.stdout.flush()
                    time.sleep(1)
                print("\rProgram exited.")
                sys.exit(1)

    print("All rainfall values are present, valid, and positive.")
    print_separator2()
    time.sleep(2)

def validate_cross_data(coordinates_data, headers):
    print("Executing the cross-validation between coordinates.csv and hourly_rainfall.csv files...")
    time.sleep(3)

    print("Number of stations in the coordinates file:", len(coordinates_data))
    print("Number of columns in the hourly rainfall file:", len(headers))
    print_separator2()
    time.sleep(3)

    if len(coordinates_data) != len(headers):
        print("Erro 11: Number of stations in the coordinates file does not match the number of columns in the hourly rainfall file.")
        print(f"Stations in coordinates file: {len(coordinates_data)}")
        print(f"Columns in hourly rainfall file: {len(headers)}")
        
        for remaining in range(30, 0, -1):
            sys.stdout.write(f"\rProgram will exit in {remaining} seconds...")
            sys.stdout.flush()
            time.sleep(1)
        print("\rProgram exited.")
        sys.exit(1)

# Function to convert date from 'dd/mm/yyyy hh:min' to 'YYYY MM DD HOUR MINUTE SECOND'
def convert_date_format(date_str):
    print(f"Converting date {date_str}...")
    time.sleep(3)
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        hour = date_obj.hour
        minute = date_obj.minute
        second = date_obj.second  # Defined as 0 to match the requested format
        print_separator2()
        return f"{year} {month:02} {day:02} {hour} {minute} {second}"
    except ValueError:
        print("Erro 12: Date format conversion failed.")
        print("Please check the date format in the input file.")
        for remaining in range(30, 0, -1):
            sys.stdout.write(f"\rProgram will exit in {remaining} seconds...")
            sys.stdout.flush()
            time.sleep(1)
        print("\rProgram exited.")
        sys.exit(1)

def create_srm_files(hourly_rainfall_file, coordinates_file):
    validate_coordinates_file(coordinates_file)
    
    with open(coordinates_file, 'r', newline='') as coord_file:
        coord_reader = csv.reader(coord_file, delimiter=';')
        next(coord_reader)  # Skip the header   
        coordinates_data = list(coord_reader)

    with open(hourly_rainfall_file, 'r', newline='') as infile:
        reader = csv.reader(infile, delimiter=';')
        data = list(reader)

    validate_hourly_rainfall_file(data)

    headers = data[0][1:]  # Ignore the first column (date) and get the remaining column headers
    
    print("Converting initial date from 'hourly_rainfall.csv'")
    initial_data = convert_date_format(data[1][0])  # Convert the initial date to the desired format
    print("Converting final date from 'hourly_rainfall.csv'")
    end_date = convert_date_format(data[-1][0])  # Convert the end date to the desired format

    validate_cross_data(coordinates_data, headers)

    print("Creating .srm files...")
    time.sleep(3)
    srm_files = []
    for col_idx, header in enumerate(headers):
        srm_filename = f"{header}.srm"
        with open(srm_filename, 'w') as outfile:
            name = header  # The name of the .srm file is the column header
            coord_x = coordinates_data[col_idx][2]  # Correction: COORD_X is in the third column
            coord_y = coordinates_data[col_idx][1]  # Correction: COORD_Y is in the second column

            outfile.write(f"TIME_UNITS                : HOURS\n")
            outfile.write(f"SERIE_INITIAL_DATA        : {initial_data}\n")
            outfile.write(f"NAME                      : {name}\n")
            outfile.write(f"COORD_X                   : {coord_x}\n")
            outfile.write(f"COORD_Y                   : {coord_y}\n\n")
            outfile.write(f"!Date rainfall\n")
            outfile.write(f"<BeginTimeSerie>\n")

            for index, value in enumerate(data[1:], start=0):
                precipitation = float(value[col_idx + 1])
                outfile.write(f"{index}\t{precipitation:.4f}\n")

            outfile.write(f"<EndTimeSerie>\n")
        
        srm_files.append((srm_filename, coord_x, coord_y))

    print(f"Files created in directory: {os.getcwd()}")
    print("SRM files have been successfully generated.")
    print_separator2()
    time.sleep(3)

    create_fillmatrix_file(initial_data, end_date, srm_files)

def create_fillmatrix_file(initial_data, end_date, srm_files):
    print("Creating 'FillMatrix.dat' file...")
    time.sleep(3)
    
    output_hdf5 = "output.hdf5"
    grid_data_file = "topography.dat"

    with open("FillMatrix.dat", 'w') as file:
        file.write("PROPERTY_NAME             : precipitation\n")
        file.write("PROPERTY_UNITS            : mm\n")
        file.write(f"OUTPUT_FILE               : {output_hdf5}\n")
        file.write("VARIABLE_IN_TIME          : 1\n")
        file.write(f"GRID_DATA_FILE            : {grid_data_file}\n\n")
        file.write(f"START                     : {initial_data}\n")
        file.write(f"END                       : {end_date}\n")
        file.write("MAX_TIME_SPAN             : 86400\n")
        file.write("OUTPUT_TIME               : 0 3600\n")
        file.write("SKIP_NULLVALUES           : 0\n\n")
        file.write("INTERPOLATION_METHOD      : 2\n")
        file.write("MAX_DISTANCE              : 50000\n")
        file.write("IWD_N                     : 2.0\n\n")
        
        for filename, coord_x, coord_y in srm_files:
            file.write("<begin_station>\n")
            file.write(f"NAME                      : {filename.split('.')[0]}\n")
            file.write(f"X                         : {coord_x}\n")
            file.write(f"Y                         : {coord_y}\n")
            file.write("VALUE_TYPE                : TIMESERIE\n")
            file.write(f"FILENAME                  : {filename}\n")
            file.write("DATA_COLUMN               : 2\n")
            file.write("<end_station>\n\n")

    print("FillMatrix.dat file has been successfully generated.")
    print_separator2()
    time.sleep(3)

def execute_fillmatrix():
    print("Starting 'FillMatrix.exe'...")
    time.sleep(3)
    exe_file = 'FillMatrix.exe'
    if os.path.isfile(exe_file):
        os.system(exe_file)
        print(f"{exe_file} executed successfully.")
        print_separator2()
        time.sleep(2)

    output_file = 'output.hdf5'
    if os.path.isfile(output_file):
        print(f"{output_file} created successfully in directory: {os.getcwd()}")
        print("Program will exit in 30 seconds...")
        print_separator1()
        for remaining in range(30, 0, -1):
            sys.stdout.write(f"\rProgram will exit in {remaining} seconds...")
            sys.stdout.flush()
            time.sleep(1)
        print("\rProgram exited.")
    else:
        print(f"Erro 13: {output_file} was not created.")
        sys.exit(1)

def main():
    print_header()
    current_dir = get_current_directory()

    check_fillmatrix_exe()
    check_dat_file()
    check_csv_file('coordinates.csv')
    check_csv_file('hourly_rainfall.csv')

    create_srm_files('hourly_rainfall.csv', 'coordinates.csv')
    execute_fillmatrix()

if __name__ == "__main__":
    main()
