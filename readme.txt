DeBos application.

Desktop application used to present data from MySQL DB to end user.
The data can be filtered - user can select the table columns that he wants to be presented
or filter the table by any other parameter.

The user can select the amount of entries that are to be presented, sort the table
by any column and restore the table original view.

Table data can be exported to XLS file, file name will be identical to the table name,
table headers in XLS file will be identical to table headers.

The user also can enter an SQL query manually, an it will be executed (if it's valid).


Screen 1 : Table selection.

Contains 4 input fields for DB name, IP and credentials.
Once all of them are filled the user must click the "Connect" button to connect to DB.
When the connection is established the user is presented with DB tables list.
After one of the tables is selected the user must click on "Select table" button to access it's content.

Screen 2: Table content:
%pass%




App Design

The app has 3 modules: "Executor", "Presentor" and "Sky".

1. Executor: responsible for all operations with MySQL DB. Based mainly on 'pysql' library.
   New methods can be added to Executor to support new features for the app.

2. Presentor: responsible for creating and managing UI objects. Based mainly on 'tkinter' library.
   'Presentor' instance requires an 'Executor' instance to be initialized.

