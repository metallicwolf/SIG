import csv
import os

"""
The program searches for *.sql and *.csv files in the specified folder. Looks in the SQL files for the name 
of the table and columns. Looks for data for tables in CSV files. Then the data is converted in the correct format. 
Next, the program generates SQL files with ready-made queries for insertion into tables. 
If there are no SQL files, then the program generates only data files.
"""

folder_with_files = 'example/'

# DROP old tables, CREATE new tables, INSERT values
cr_new_table = True


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


def get_table_name(line):
    """Get and return table name from table structure SQL file"""

    start = line.upper().find('TABLE') + 6
    end = line[start:].find(' ', 2) + start
    name = line[start:end]
    return name.strip()


def line_check(new_line: str):
    """String check for fields in tables_full_structure"""

    if new_line.rfind(',') > -1:
        # remove ','
        new_line = new_line[:new_line.rfind(',')]
    if new_line.count('(') < new_line.count(')'):
        # remove excess ')'
        new_line = new_line[:new_line.rfind(')')]

    return new_line


def load_tables(folder, sql_files_list):
    """Returns a dictionary with nested lists from the SQL script files,
    where key is the name of the table, value is the list of columns."""

    tables_full_structure = {}
    tables_name_and_fields = {}
    find_new_table = False

    for filename in sql_files_list:
        with open(folder + filename, newline='') as File:

            for line in File.readlines():
                line = line.strip()

                if '--' in line[:4]:
                    # skip comments
                    continue

                elif not find_new_table and 'CREATE' in line.upper() and 'TABLE' in line.upper():
                    # if finds new table, changes flag

                    find_new_table = True
                    table_name = get_table_name(line)

                    # when find table name, adding key
                    tables_name_and_fields[table_name] = []

                    # when find table name, adding key in full structure dict
                    tables_full_structure[table_name] = []

                elif find_new_table:
                    # if in current table, then add fields
                    field = line.upper()

                    if len(field) > 1:
                        field = field[:field.find(' ')]
                        if field != 'PRIMARY':
                            tables_name_and_fields[table_name].append(field)

                    # adding to full tables with chech end of the lines
                    if len(field) > 1:
                        full_field = line_check(line)
                        tables_full_structure[table_name].append(full_field)

                if find_new_table and ';' in line:
                    # if flag TRUE and find ending
                    find_new_table = False

    return tables_full_structure, tables_name_and_fields


def load_values(folder, csv_files_list):
    """Searches the specified folder for CSV files with a list of values. The file name matches the table name.
    Returns a dictionary with nested lists, where key is the table name, value is a list of table values."""

    new_dict_files_values = {}

    for filename in csv_files_list:
        # get table name from filename without endswith
        table_name = filename[:-4].upper()

        # add key TABLENAME and empty list
        new_dict_files_values[table_name] = []

        with open(folder + filename, newline='') as File:
            reader = csv.reader(File)
            for row in reader:
                # adding values with values_checker
                new_dict_files_values[table_name].append(values_checker(row))
    return new_dict_files_values


def values_checker(row):
    """Receives a list of values, returns a new list, with the correct format of values"""
    # FIXME - REMAKE

    new_row = []

    for field in row:
        if field.isspace():
            # skip, if space
            continue
        if field == '':
            # skip, if empty
            continue

        # date format converter
        if field.find('/') > -1:
            field = field[6:] + '-' + field[:2] + '-' + field[3:5]

        if field.find('"') > -1 or field.find("'") > -1:
            field = field[1:-1]

        # if string, then add's ' '
        if not field.isdigit():
            field = "'" + field + "'"

        new_row.append(field)
    return new_row


def generate_full_query_files():
    """Creates a files named [TABLE_NAME]_new.sql.
    The file contains a ready-made request for inserting data into table."""

    if not os.path.exists('created'):
        os.mkdir('created')
    for table_name in tab_fields.keys():
        if table_name in values.keys():
            table_columns = '(' + ', '.join(tab_fields[table_name]) + ')'
            generated_file_name = table_name.title() + '_new.sql'
            with open('created/' + generated_file_name, 'w') as File:
                File.write('INSERT INTO ' + table_name.upper() + '\n' + table_columns + '\nVALUES\n')
                for row_list in values[table_name]:
                    if row_list == values[table_name][-1]:
                        File.write('(' + ', '.join(row_list) + ')' + ';')
                    else:
                        File.write('(' + ', '.join(row_list) + ')' + ',\n')
    print('OK. See files in folder "created".')


def generate_values_files():
    """Creates a file named [TABLE_NAME]_new.sql with onlu values."""

    if not os.path.exists('created'):
        os.mkdir('created')

    for table_name in values.keys():
        generated_file_name = table_name.title() + '_new.sql'
        with open('created/' + generated_file_name, 'w') as File:
            for row_list in values[table_name]:
                if row_list == values[table_name][-1]:
                    File.write('(' + ', '.join(row_list) + ')' + ';')
                else:
                    File.write('(' + ', '.join(row_list) + ')' + ',\n')


sql_list, csv_list = search_files(folder_with_files)
print(sql_list, csv_list)

if sql_list and csv_list:
    tab_full, tab_fields = load_tables(folder_with_files, sql_list)
    values = load_values(folder_with_files, csv_list)
    print(values)
    generate_full_query_files()

elif not sql_list and csv_list:
    values = load_values(folder_with_files, csv_list)
    print(values)
    generate_values_files()
else:
    pass
