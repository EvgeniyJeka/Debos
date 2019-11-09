from Executer import *
from presentor import *
from tkinter import *
from tkinter import ttk
import Pmw



# Used classes (
executor = Executer()
presentor = ""

# Enteries open to user input
entry_1 = ""
entry_2 = ""
entry_3 = ""
entry_4 = ""

variable = ""


# Creating a window and setting it's size
root = Tk()
root.geometry("400x400")
root.resizable(0, 0)
Pmw.initialise(root)

# Used listbox - for tables presentation and selection
tables_list = Listbox(root)
tables_list.grid(row=5, column=0)
tables_list.grid(rowspan=10)

# Setting head label

Head_label = Label(root, text="Debos version 1.0", fg="white", bg="blue", font=("", 20))
Head_label.grid(row=0, column=0)
Head_label.grid(columnspan=3)
# root.columnconfigure(0, weight=1)

# Adding input fields - they will be used to receive the information required for connection to DB

# Enter Host IP
label_1 = Label(root, text="Enter Host IP: ", fg="blue", font=("", 15))
entry_1 = Entry(root, width="35")
label_1.grid(row=1, column=0, pady=5, padx=1, sticky=W)
entry_1.grid(row=1, column=1, sticky=E)
entry_1.insert(0, '127.0.0.1')

# Enter Username
label_2 = Label(root, text="Enter Username: ", fg="blue", font=("", 15))
entry_2 = Entry(root, width="35")
label_2.grid(row=2, column=0, pady=5, padx=1, sticky=W)
entry_2.grid(row=2, column=1, sticky=E)
entry_2.insert(0, 'root')

# Enter Password
label_3 = Label(root, text="Enter Password: ", fg="blue", font=("", 15))
entry_3 = Entry(root, width="35")
label_3.grid(row=3, column=0, pady=5, padx=1, sticky=W)
entry_3.grid(row=3, column=1, sticky=E)
entry_3.insert(0, '7417418')

# Enter the database name
label_4 = Label(root, text="Enter DB name: ", fg="blue", font=("", 15))
entry_4 = Entry(root, width="35")
label_4.grid(row=4, column=0, pady=5, padx=1, sticky=W)
entry_4.grid(row=4, column=1, sticky=E)
entry_4.insert(0, 'play')

# Connect button
button_connect = Button(root, text= "Connect", bg="purple", fg="white", height="2",width="10",command = lambda:connect())
button_connect.grid(row=5, column=1)

#Select button
button_select = Button(root, text= "Select Table", bg="green", fg="white", height="2",width="10", command = lambda:select_table())
button_select.grid(row=6, column=1)

#Connecting to the selected DB, all the required input gathered from UI
def connect():
    print("Connect")
    executor = Executer()

    hst = entry_1.get()
    usr = entry_2.get()
    pwd = entry_3.get()
    db_name = entry_4.get()

    # Create a Presentor
    presentor = Presentor(hst, usr, pwd, db_name, executor)


    # Establish connection
    presentor.establish_connection(executor)

    #Present available tables
    available_tables = executor.show_tables(presentor.cursor)
    tables_list.delete(0,END)
    tables_list.insert(END, *available_tables)

#Presents the selected table
def select_table():
    selected_table = tables_list.get(tables_list.curselection())
    print("Selected: "+str(selected_table))

    # Window size
    hight = 700
    width = 1300
    size = '%sx%s' % (width, hight)
    columns_size = 100

    hst = entry_1.get()
    usr = entry_2.get()
    pwd = entry_3.get()
    db_name = entry_4.get()

    # Create a Presentor
    presentor = Presentor(hst, usr, pwd, db_name, executor)
    presentor.establish_connection(executor)

    # Open a window
    presentor.open_window(size)
    presentor.select_table(selected_table)

    # Set headers
    presentor.set_headers(presentor.executer, presentor.tree, presentor.cursor, presentor.table, 120)

    #Fill table
    presentor.fill_table(presentor.executer, presentor.tree, presentor.cursor, presentor.table)

    #Button Find By ID (OB - 1)
    button_find_by_id = Button(presentor.root, text="Find Element By ID", bg="grey", fg="white", height="1", width="15", command = lambda:find_by_id())
    button_find_by_id.grid(row=6,column=0, padx=20, pady=5, sticky=W)

    #Button Find By Param (OB - 2)
    button_find = Button(presentor.root, text="Find By Selected Parameter", bg="grey", fg="white", height="1", width="20", command = lambda:find_by_param())
    button_find.grid(row=6, column=1, padx=1, pady=5, sticky=W)

    # Button Restore (OB - 3)
    button_restore = Button(presentor.root, text="Restore", bg="grey", fg="white", height="1",width="20", command = lambda:restore())
    button_restore.grid(row=6, column=2, padx=1, pady=5, sticky=W)

    # Button Query (OB - 4)
    button_query = Button(presentor.root, text = "Query", bg="grey", fg="white", height="1",width="20", command = lambda:run_query())
    button_query.grid(row=6, column=3, padx=1, pady=5, sticky=W)

    # Button Order By (OB - 5)
    button_order_by = Button(presentor.root, text="Order By", bg="blue", fg="white", height="1", width="20", command = lambda:order_by())
    button_order_by.grid(row=6, column=4, padx=1, pady=5, sticky=W)


    # Button Columns (OB - 6)
    button_columns = Button(presentor.root, text="Select", bg="purple", fg="white", height="1", width="10", command=lambda:select_column())
    button_columns.grid(row=8, column=1, padx=1, pady=5, sticky=W)


    #Drop Box that contains all table columns
    variable = StringVar(presentor.root)
    variable.set("Columns")  # default value
    columns = executor.get_columns(presentor.table, presentor.cursor)
    w = OptionMenu(presentor.root, variable, *columns)
    w.grid(row=8, column=0, padx=1, pady=5, sticky=E)
    w.config(width = 18, bg = "blue", fg="white")

    # Button Export (OB - 7)
    button_export = Button(presentor.root, text="Export", bg="blue", fg="white", height="1", width="20", command = lambda:export())
    button_export.grid(row=8, column=2, padx=1, pady=5, sticky=W)

    # Button Show Only (OB - 8)
    button_show_only = Button(presentor.root, text="Show Only", bg="blue", fg="white", height="1", width="20", command = lambda:show_only())
    button_show_only.grid(row=8, column=3, padx=1, pady=5, sticky=W)

    #Button Limit (OB - 9)
    button_limit = Button(presentor.root, text="Limit", bg="green", fg="white", height="1", width="20", command = lambda:limit_by())
    button_limit.grid(row=8, column=4, padx=1, pady=5, sticky=W)


    #Entry used to receive user input. Related to "Operation Buttons".
    request_input = Entry(presentor.root, width="200")
    request_input.grid(row=7, column=0, padx=20, pady=10, sticky=W)
    request_input.grid(columnspan=5)


    #Show only
    def show_only():
        print("Test - show only")
        input = request_input.get()
        elements = input.split(",")

        headers = executor.get_columns(presentor.table, presentor.cursor)

        for x in elements:
            if x not in headers:
                print(F"No such column - {x}")
                request_input.delete(0, 'end')
                request_input.insert(10, F"No such column - {x}")
                return

        result = executor.show_only(selected_table, presentor.cursor,input)

        ####### Experimental ########

        presentor.customize_headers(presentor.executer, presentor.tree, presentor.cursor, presentor.table, 120, elements)

        ####### Experimental ########

        # Clearing the table to present the result
        for i in presentor.tree.get_children():
            presentor.tree.delete(i)

        #Entering content
        counter = 0
        table_content = result
        for line in table_content:
            presentor.tree.insert('', 'end', text=counter, values=line)
            counter += 1

    #Select column
    def select_column():
        request_input.insert(10, variable.get())






    #Export
    def export():
        cursor = presentor.cursor
        table = presentor.table
        file_name = str(presentor.table)+".xls"

        executor.excel_all(table,cursor,file_name)
        request_input.insert(10, 'Table exported!')


    #Restore
    def restore():

        # Clearing the table to present the result
        for i in presentor.tree.get_children():
            presentor.tree.delete(i)


        #Since some of the columns might be removed by previous operations we create new Tree object
        presentor.tree = ttk.Treeview(presentor.root, heigh=20)
        presentor.tree.grid(row=4, column=0, padx=20)
        presentor.tree.grid(columnspan=5)

        #We are restoring the original table headers
        presentor.set_headers(presentor.executer, presentor.tree, presentor.cursor, presentor.table, 120)

        #We are filling the table with it's original content.
        presentor.fill_table(presentor.executer, presentor.tree, presentor.cursor, presentor.table)
        request_input.delete(0, 'end')




    #Method Find By ID
    def find_by_id():
        id = request_input.get()
        if len(id) < 1:
            request_input.insert(10, 'Cannot be empty!')
            return
        elif id == 'Cannot be empty!' or id=='No ID column!':
            request_input.delete(0, 'end')
            return

        column_names = executor.get_columns(selected_table, presentor.cursor)

        if id not in column_names:
            request_input.delete(0, 'end')
            request_input.insert(10, 'No ID column!')
            return

        print("Test - looking for record with ID " + str(id))
        result = executor.find_by_id(selected_table, presentor.cursor, id)
        print(result)

        #Clearing the table to present the result
        for i in presentor.tree.get_children():
            presentor.tree.delete(i)

        #Entering content
        counter = 0
        table_content = result
        for line in table_content:
            presentor.tree.insert('', 'end', text=counter, values=line)
            counter += 1




    #Method Run DB Query
    def run_query():

        query = request_input.get()
        if len(query)<1 :
            request_input.insert(10, 'Cannot be empty!')
            return
        elif query =='Cannot be empty!':
            request_input.delete(0, 'end')
            return


        try:

            cursor = presentor.cursor
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)

        except pymysql.err.ProgrammingError:
            request_input.delete(0, 'end')
            request_input.insert(10,'Invalid Query!')
            return

        # Clearing the table to present the result
        for i in presentor.tree.get_children():
            presentor.tree.delete(i)

        #Entering content
        counter = 0
        table_content = result
        for line in table_content:
            presentor.tree.insert('', 'end', text=counter, values=line)
            counter += 1




    #Limit by - present only limited amount of table records
    def limit_by():
        # Input - the amount of records to be presented
        limit = request_input.get()

        if len(limit)<1 :
            request_input.insert(10, 'Cannot be empty!')
            return
        elif limit == 'Cannot be empty!':
            request_input.delete(0, 'end')
            return



        try:
            result = executor.limit_by(selected_table, presentor.cursor, limit)

        except pymysql.err.InternalError:
            request_input.delete(0, 'end')
            request_input.insert(10, 'Please enter a numeric value')
            return



        # Clearing the table to present the result
        for i in presentor.tree.get_children():
            presentor.tree.delete(i)

        counter = 0
        table_content = result
        for line in table_content:
            presentor.tree.insert('', 'end', text=counter, values=line)
            counter += 1




    # Order by - ordering the table by selected column. Order is changed each time.
    def order_by():
        #Input - the column by which the table is sorted
        column = request_input.get()
        if len(column)<1 :
            request_input.insert(10, 'Cannot be empty!')
            return
        elif column =='Cannot be empty!':
            request_input.delete(0, 'end')
            return


        try:
            result = executor.order_by_column(selected_table, presentor.cursor,column,presentor.order)

        except pymysql.err.InternalError:
            request_input.delete(0, 'end')
            request_input.insert(10, 'No such column in this table!')
            return

        # Clearing the table to present the result
        for i in presentor.tree.get_children():
            presentor.tree.delete(i)

        counter = 0
        table_content = result
        for line in table_content:
            presentor.tree.insert('', 'end', text=counter, values=line)
            counter += 1

        #Changing the "order" param to the opposite value to the sorting will work correctly each time
        if presentor.order == 0:
            presentor.order = 1
            print(F"Sorting order: {presentor.order}")

        else:
            presentor.order = 0
            print(F"Sorting order: {presentor.order}")


    #Method "Find By Param"
    def find_by_param():
        print("Test - find by param")
        input = request_input.get()
        elements = input.split("=")

        if len(elements)!= 2:
            print("Error - must insert two arguements")
            return

        first = elements[0]
        second = elements[1]

        result = executor.find_by_param(selected_table, presentor.cursor, first, second)

        # Clearing the table to present the result
        for i in presentor.tree.get_children():
            presentor.tree.delete(i)

        counter = 0
        table_content = result
        for line in table_content:
            presentor.tree.insert('', 'end', text=counter, values=line)
            counter += 1


    ############# Tooltips attached to buttons ###############

    # Button Find By ID tooltip (OB - 1)
    tooltip_find_by_id = Pmw.Balloon(presentor.root)
    tooltip_find_by_id.bind(button_find_by_id, "This option can be used if a table has an ID column. Enter the ID and click on this button")

    # Button Find By Param tooltip (OB - 2)
    tooltip_find = Pmw.Balloon(presentor.root)
    tooltip_find.bind(button_find, "All table entries that contain the entered value are presented, enter the column name and the value: %column name% = %value%")

    # Button Restore tooltip(OB - 3)
    tooltip_button_restore = Pmw.Balloon(presentor.root)
    tooltip_button_restore.bind(button_restore, "Click to restore the original table and clean the input box")

    # Button Query tooltip(OB - 4)
    tooltip_button_query = Pmw.Balloon(presentor.root)
    tooltip_button_query.bind(button_query, "Click to execute any valid SQL query")

    # Button Order By tooltip(OB - 5)
    tooltip_button_order_by = Pmw.Balloon(presentor.root)
    tooltip_button_order_by.bind(button_order_by, "Click to order table by column in ascending or descending order after the column name was entered: %column%")

    # Button Columns tooltip(OB - 6)
    tooltip_button_columns = Pmw.Balloon(presentor.root)
    tooltip_button_columns.bind(button_columns, "Add the selected column to the string in the input box")


    #Export button tooltip (OB - 7)
    export__button_tooltip = Pmw.Balloon(presentor.root)
    export__button_tooltip.bind(button_export, "Export table content to EXCEL")

    # Button Show Only (OB - 8)
    show_only_button_tooltip = Pmw.Balloon(presentor.root)
    show_only_button_tooltip.bind(button_show_only, "Choose the columns you want to be presented: %column name%, %column name%,%column name%")

    # Button Show Only (OB - 9)
    limit_button_tooltip = Pmw.Balloon(presentor.root)
    show_only_button_tooltip.bind(button_limit, "Choose how many entires do you want to be presented")


    #Close the window
    presentor.close_window()



root.mainloop()
