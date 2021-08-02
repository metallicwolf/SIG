# SQL INSERT generator (SIG)
* ### The program finds the structure of tables (table names, column names), then finds all files with values. 
* ### Processes values to match the correct format. 
* ### Generates ready-made database queries to add large numbers of values to tables. Queries with values are saved to files like <TABLENAME_new.sql>.

## For example. 
* Search for *.sql and *.csv files. SQL files containing a table structure, CSV files containing a list of values to be INSERTED 
into the database table. Below is an example.
  
        Script_Create_Tables_1.sql:
        
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
  
        Script_Create_Tables_2.sql:
  
        CREATE TABLE JOBS (
                            JOB_IDENT CHAR(9) NOT NULL, 
                            JOB_TITLE VARCHAR(15) ,
                            MIN_SALARY DECIMAL(10,2),
                            MAX_SALARY DECIMAL(10,2),
                            PRIMARY KEY (JOB_IDENT));


        Employees.csv:
  
        E1001,John,Thomas,123456,01/09/1976,M,"5631 Rice, OakPark,IL",100,100000,30001,2
        E1002,Alice,James,123457,07/31/1972,F,"980 Berry ln, Elgin,IL",200,80000,30002,5
        E1003,Steve,Wells,123458,08/10/1980,M,"291 Springs, Gary,IL",300,50000,30002,5
        E1004,Santosh,Kumar,123459,07/20/1985,M,"511 Aurora Av, Aurora,IL",400,60000,30004,5

        Jobs.csv

        100,'Sr. Architect',60000,100000,
        200,'Sr. Software Developer',60000,80000,
        300,'Jr.Software Developer',40000,60000,
        400,'Jr.Software Developer',40000,60000,
        500,'Jr. Architect',50000,70000,
        600,'Lead Architect',70000,100000,
        650,'Jr. Designer',60000,70000,
        660,'Jr. Designer',60000,70000,
        234,'Sr. Designer',70000,90000,
        220,'Sr. Designer',70000,90000
        

* Looks in the SQL files for the name of the table and columns. Looks for data for tables in CSV files. 
  Then the data is converted in the correct format. 
  Next, the program generates files with ready-made queries for insertion into tables. 
  If there are no SQL files, then the program generates only data files.
  
        Employees_New.sql
  
        INSERT INTO EMPLOYEES
        (EMP_ID, F_NAME, L_NAME, SSN, B_DATE, SEX, ADDRESS, JOB_ID, SALARY, MANAGER_ID, DEP_ID)
        VALUES
        ('E1001', 'John', 'Thomas', 123456, '1976-01-09', 'M', '5631 Rice, OakPark,IL', 100, 100000, 30001, 2),
        ('E1002', 'Alice', 'James', 123457, '1972-07-31', 'F', '980 Berry ln, Elgin,IL', 200, 80000, 30002, 5),
        ('E1003', 'Steve', 'Wells', 123458, '1980-08-10', 'M', '291 Springs, Gary,IL', 300, 50000, 30002, 5),
        ('E1004', 'Santosh', 'Kumar', 123459, '1985-07-20', 'M', '511 Aurora Av, Aurora,IL', 400, 60000, 30004, 5),
        ('E1005', 'Ahmed', 'Hussain', 123410, '1981-01-04', 'M', '216 Oak Tree, Geneva,IL', 500, 70000, 30001, 2),
        ('E1006', 'Nancy', 'Allen', 123411, '1978-02-06', 'F', '111 Green Pl, Elgin,IL', 600, 90000, 30001, 2),
        ('E1007', 'Mary', 'Thomas', 123412, '1975-05-05', 'F', '100 Rose Pl, Gary,IL', 650, 65000, 30003, 7),
        ('E1008', 'Bharath', 'Gupta', 123413, '1985-05-06', 'M', '145 Berry Ln, Naperville,IL', 660, 65000, 30003, 7),
        ('E1009', 'Andrea', 'Jones', 123414, '1990-07-09', 'F', '120 Fall Creek, Gary,IL', 234, 70000, 30003, 7),
        ('E1010', 'Ann', 'Jacob', 123415, '1982-03-30', 'F', '111 Britany Springs,Elgin,IL', 220, 70000, 30004, 5);

        Jobs_new.sql

        INSERT INTO JOBS
        (JOB_IDENT, JOB_TITLE, MIN_SALARY, MAX_SALARY)
        VALUES
        (100, 'Sr. Architect', 60000, 100000),
        (200, 'Sr. Software Developer', 60000, 80000),
        (300, 'Jr.Software Developer', 40000, 60000),
        (400, 'Jr.Software Developer', 40000, 60000),
        (500, 'Jr. Architect', 50000, 70000),
        (600, 'Lead Architect', 70000, 100000),
        (650, 'Jr. Designer', 60000, 70000),
        (660, 'Jr. Designer', 60000, 70000),
        (234, 'Sr. Designer', 70000, 90000),
        (220, 'Sr. Designer', 70000, 90000);