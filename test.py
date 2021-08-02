import csv
import os

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


def get_table_name(line):
    start = line.upper().find('TABLE') + 6
    end = line[start:].find(' ', 2) + start
    name = line[start:end]
    return name.strip()


def line_check(new_line: str):
    if new_line.rfind(',') > -1:
        new_line = new_line[:new_line.rfind(',')]
    if new_line.count('(') < new_line.count(')'):
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
                    # if NOT in find new table
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


sql_list, csv_list = search_files(folder_with_files)
tab_full, tab_fields = load_tables(folder_with_files, sql_list)
print('full: ', tab_full, 'fields', tab_fields, sep='\n')
