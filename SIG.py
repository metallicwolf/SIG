import csv
import os

"""
The program searches for *.sql and *.csv files in the specified folder. Looks in the SQL files for the name 
of the table and columns. Looks for data for tables in CSV files. Then the data is converted in the correct format. 
Next, the program generates files with ready-made queries for insertion into tables. 
If there are no SQL files, then the program generates only data files.
"""

folder_with_files = 'example/'


def search_files(folder):
    """Searches for *sql and *.csv files in the specified folder. Returns two lists."""

    sql_files = []
    csv_files = []

    if not os.path.exists(folder):
        print('Error: Folder not found!')
    else:
        for root, dirs, files in os.walk(folder):
            dirs[:] = []
            if not files:
                print('Error: CSV or SQL-script files not found! Canceled!')
                break
            for filename in files:
                if filename.endswith('.sql'):
                    sql_files.append(filename)
                elif filename.endswith('.csv'):
                    csv_files.append(filename)

    return sql_files, csv_files


def load_tables_structure(folder, sql_files_list):
    """Returns a dictionary with nested lists from the SQL script files,
    where key is the name of the table, value is the list of columns."""
    table_str_dict = {}

    for filename in sql_files_list:
        with open(folder + filename, newline='') as File:
            reader = csv.reader(File)
            for row in reader:
                if not row:
                    continue
                field = row[0].strip().upper()
                if field.isspace() or field == '':
                    continue
                if field.find('PRIMARY') > -1:
                    continue
                if field.find('CREATE') > -1:
                    start = field.find('TABLE') + 6
                    end = field[start:].find(' ', 2) + start
                    new_table_name = field[start:end]
                    table_str_dict[new_table_name] = []
                else:
                    field = field[:field.find(' ')]
                    table_str_dict[new_table_name].append(field)
    return table_str_dict


def load_values(folder, csv_files_list):
    """Searches the specified folder for CSV files with a list of values. The file name matches the table name.
    Returns a dictionary with nested lists, where key is the table name, value is a list of table values."""
    new_dict_files_values = {}

    for filename in csv_files_list:
        table_name = filename[:-4].upper()
        new_dict_files_values[table_name] = []
        with open(folder + filename, newline='') as File:
            reader = csv.reader(File)
            for row in reader:
                new_dict_files_values[table_name].append(values_checker(row))
    return new_dict_files_values


def values_checker(row):
    """Receives a list of values, returns a new list, with the correct format of values"""
    new_row = []
    for field in row:
        if field.isspace():
            continue
        if field == '':
            continue

        # date format converter
        if field.find('/') > -1:
            field = field[6:] + '-' + field[:2] + '-' + field[3:5]

        if field.find('"') > -1 or field.find("'") > -1:
            field = field[1:-1]

        # if string add ' '
        if not field.isdigit():
            field = "'" + field + "'"
        new_row.append(field)
    return new_row


def generate_full_query_files():
    """Creates a files named [TABLE_NAME]_new.csv.
    The file contains a ready-made request for inserting data into table."""

    if not os.path.exists('created'):
        os.mkdir('created')
    for table_name in tables.keys():
        if table_name in values.keys():
            table_columns = '(' + ', '.join(tables[table_name]) + ')'
            generated_file = table_name.title() + '_new.csv'
            with open('created/' + generated_file, 'w') as File:
                File.write('INSERT INTO ' + table_name.upper() + '\n' + table_columns + '\nVALUES\n')
                for row_list in values[table_name]:
                    if row_list == values[table_name][-1]:
                        File.write('(' + ', '.join(row_list) + ')' + ';')
                    else:
                        File.write('(' + ', '.join(row_list) + ')' + ',\n')
    print('OK. See files in folder "created".')


def generate_values_files():
    """Creates a file named [TABLE_NAME]_new with onlu values."""

    if not os.path.exists('created'):
        os.mkdir('created')
    for table_name in values.keys():
        generated_file = table_name.title() + '_new.csv'
        with open('created/' + generated_file, 'w') as File:
            for row_list in values[table_name]:
                if row_list == values[table_name][-1]:
                    File.write('(' + ', '.join(row_list) + ')' + ';')
                else:
                    File.write('(' + ', '.join(row_list) + ')' + ',\n')


sql_list, csv_list = search_files(folder_with_files)
# print(sql_list, csv_list)

if sql_list and csv_list:
    tables = load_tables_structure(folder_with_files, sql_list)
    # print(tables)

    values = load_values(folder_with_files, csv_list)
    # print(values)

    generate_full_query_files()
elif not sql_list and csv_list:
    values = load_values(folder_with_files, csv_list)
    # print(values)
    generate_values_files()
else:
    pass
