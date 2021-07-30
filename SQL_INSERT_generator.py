import csv
import os

"""
The program finds the structure of tables (table names, column names), then finds all files with values. 
Processes values to match the correct format. 
Generates ready-made database queries to add large numbers of values to tables. Queries with values are saved to 
files like <TABLENAME_new.csv>.
"""

folder_with_values_files = 'example/'
table_structure_file = 'example/Script_Create_Tables.sql'


def load_table_structure(filename):
    """Returns a dictionary with nested lists from the SQL script file,
    where key is the name of the table, value is the list of columns."""
    table_str_dict = {}

    if not os.path.isfile(table_structure_file):
        print('Error: SQL script file not found!')
    else:
        with open(filename, newline='') as File:
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
            print('Table structure loaded...')
    return table_str_dict


def load_files_with_values(folder):
    """Searches the specified folder for CSV files with a list of values. The file name matches the table name.
    Returns a dictionary with nested lists, where key is the table name, value is a list of table values."""
    new_dict_files_values = {}

    if not os.path.exists(folder_with_values_files):
        print('Error: Folder not found!')
    else:
        for root, dirs, files in os.walk(folder):
            dirs[:] = []
            if not files:
                print('Error: CSV files with values not found! Canceled!')
                break
            for filename in files:
                if filename.endswith('.csv'):
                    table_name = filename[:-4].upper()
                    new_dict_files_values[table_name] = []
                    with open(folder + filename, newline='') as File:
                        reader = csv.reader(File)
                        for row in reader:
                            new_dict_files_values[table_name].append(values_checker(row))
            print('Values loaded...')
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


def generate_file():
    """Creates a file named [TABLE_NAME]_new.
    The file contains a ready-made request for entering data into the database table."""
    if not os.path.exists('created'):
        os.mkdir('created')
    for table_name in table_structure.keys():
        if table_name in table_values:
            table_columns = '(' + ', '.join(table_structure[table_name]) + ')'
            generated_file = table_name + '_new.csv'
            with open('created/' + generated_file.title(), 'w') as File:
                File.write('INSERT INTO ' + table_name.upper() + '\n' + table_columns + '\nVALUES\n')
                for row_list in table_values[table_name]:
                    if row_list == table_values[table_name][-1]:
                        File.write('(' + ', '.join(row_list) + ')' + ';')
                    else:
                        File.write('(' + ', '.join(row_list) + ')' + ',\n')
    print('OK. See files in folder "created".')


table_structure = load_table_structure(table_structure_file)
# print(table_structure)
table_values = load_files_with_values(folder_with_values_files)
# print(table_values)
# print('---------')
generate_file()
