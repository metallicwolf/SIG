# SQL INSERT generator
The program finds the structure of tables (table names, column names), then finds all files with values. 
Processes values to match the correct format. Generates files <TABLE_NAME_new.csv> that query to 
database to INSERT values into the table.

For example. 
1) The <folder_with_values_files> contains files named <TABLE_NAME>.CSV containing a list of values to be INSERTED 
into the database table. Below is an example of the contents of the file.

Employees.csv:
E1001,John,Thomas,123456,01/09/1976,M,"5631 Rice, OakPark,IL",100,100000,30001,2
E1002,Alice,James,123457,07/31/1972,F,"980 Berry ln, Elgin,IL",200,80000,30002,5
E1003,Steve,Wells,123458,08/10/1980,M,"291 Springs, Gary,IL",300,50000,30002,5
E1004,Santosh,Kumar,123459,07/20/1985,M,"511 Aurora Av, Aurora,IL",400,60000,30004,5


2) <table_structure_file> is a script file that creates a database table with the specified 
columns. Below is an example of the contents of the file.

Script_Create_Tables.sql:

CREATE TABLE EMPLOYEES (
                            EMP_ID CHAR(9) NOT NULL, 
                            F_NAME VARCHAR(15) NOT NULL,
                            L_NAME VARCHAR(15) NOT NULL,
                            SSN CHAR(9),
                            B_DATE DATE,
                            SEX CHAR,
                            ADDRESS VARCHAR(30),
                            JOB_ID CHAR(9),
                            SALARY DECIMAL(10,2),
                            MANAGER_ID CHAR(9),
                            DEP_ID CHAR(9) NOT NULL,
                            PRIMARY KEY (EMP_ID));

3) The program finds the structure of tables (table names, column names), then finds all files with values. 
Processes values to match the correct format. Generates files <TABLE_NAME_new.csv> that query to 
database to INSERT values into the table.
