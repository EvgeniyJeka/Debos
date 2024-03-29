**DeBos application**.

Desktop application used to present data from MySQL DB to end user.
The data can be filtered - user can select the table columns that he wants to be presented
or filter the table by any other parameter.

The user can select the amount of entries that are to be presented, sort the table
by any column and restore the table original view.

Table data can be exported to XLS file, file name will be identical to the table name,
table headers in XLS file will be identical to table headers.

The user also can enter an SQL query manually, an it will be executed (if it's valid).

To run the app open the file Sky.py with Python.

To launch the application you must have Python 3.6 or newer installed on your PC.
It is recommended to execute the following command to install all requirements:
"pip install -r requirements.txt"

<b>NOTE: To test the application you can fetch an image of MySQL server DB and run it 
with 'docker-compose up', providing there is a running Docker application on your PC</b>

Providing MySQL server is running you can use the 'Debos' app to connect to it.   

**Screen 1 : Table selection**.

<img src="https://github.com/EvgeniyJeka/Debos/blob/master/Debos_screen_1.jpg" alt="Screenshot" width="500" />

Contains 4 input fields for DB name, IP and credentials.
Once all of them are filled the user must click the "Connect" button to connect to DB.
When the connection is established the user is presented with DB tables list.
After one of the tables is selected the user must click on "Select table" button to access it's content.

**Screen 2: Table content**.

<img src="https://github.com/EvgeniyJeka/Debos/blob/master/Debos_screen_2.jpg" alt="Screenshot" width="700" />

Contains the content of the selected table, the Command Line and several buttons.
The Command Line and the buttons are used to receive commands from user.

Buttons list:

1. **Clear line** - clears the Command Line.

2. **Find By Selected Parameter** - allows to search the table by one of the selected parameters.
The column name and the value must be entered to command line while separated by equals sign.
Example:  name = John

3. **Query** - executes any valid SQL query entered by user. The query must be entered to Command Line.

4. **Order By** - orders the table by one of the columns. Column name must be entered to Command Line.

5. **Export** - exports the currently selected table to XLS file.

6. **Show Only** - presents only the columns selected by the user. Column names must be entered to Command Line and separated by comma:
Example: name, city, country

7. **Limit** - reads the number entered by user to command line and presents the requested amount of records.
The value must be numeric.

8. **Restore** - removes all filters and presents the original table.

9. **Columns** drop down menu - contains the names of all table columns. To add a column name to the Command Line
select a column and click on "**Select**" button.

10. **Comma** - adds comma after the last string in Command Line.



**__App Design__**

The app has 3 modules: "Executor", "Presentor" and "Sky" .

1. Executor: responsible for all operations with MySQL DB. Based mainly on 'pysql' library.
   New methods can be added to Executor to support new features for the app.

2. Presentor: responsible for creating and managing UI objects. Based mainly on 'tkinter' library.
   'Presentor' instance requires an 'Executor' instance to be initialized.

3. Sky: the main module, gets input from user via UI and executes the required operations.
