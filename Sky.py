from Executer import *
from Presentor import *
from tkinter import *
import Pmw


# This class is the upper level of the app. It's instance is used to run and manage the DeBos app.
class Sky(object):

    def __init__(self):

        # Executer instance - contains methods required for work with DB.
        self.executor = Executer()


        # Enteries open to user input
        self.entry_1 = ""
        self.entry_2 = ""
        self.entry_3 = ""
        self.entry_4 = ""

        # Variable used to create drop down menu
        self.dropdown_menu = ""


        # Creating a window and setting it's size
        self.root = Tk()
        self.root.geometry("400x400")
        self.root.resizable(0, 0)

        # Tooltips integrated.
        Pmw.initialise(self.root)

        # Used listbox - for tables presentation and selection
        self.tables_list = Listbox(self.root)
        self.tables_list.grid(row=5, column=0)
        self.tables_list.grid(rowspan=10)

        # Setting head label
        self.Head_label = Label(self.root, text="Debos version 1.2", fg="white", bg="blue", font=("", 20))
        self.Head_label.grid(row=0, column=0)
        self.Head_label.grid(columnspan=3)


        # Adding input fields - they will be used to receive the information required for connection to DB

        # Enter Host IP
        self.label_1 = Label(self.root, text="Enter Host IP: ", fg="blue", font=("", 15))
        self.entry_1 = Entry(self.root, width="35")
        self.label_1.grid(row=1, column=0, pady=5, padx=1, sticky=W)
        self.entry_1.grid(row=1, column=1, sticky=E)
        self.entry_1.insert(0, '127.0.0.1')

        # Enter Username
        self.label_2 = Label(self.root, text="Enter Username: ", fg="blue", font=("", 15))
        self.entry_2 = Entry(self.root, width="35")
        self.label_2.grid(row=2, column=0, pady=5, padx=1, sticky=W)
        self.entry_2.grid(row=2, column=1, sticky=E)
        self.entry_2.insert(0, 'root')

        # Enter Password
        self.label_3 = Label(self.root, text="Enter Password: ", fg="blue", font=("", 15))
        self.entry_3 = Entry(self.root, width="35")
        self.label_3.grid(row=3, column=0, pady=5, padx=1, sticky=W)
        self.entry_3.grid(row=3, column=1, sticky=E)
        self.entry_3.insert(0, 'password1')

        # Enter the database name
        self.label_4 = Label(self.root, text="Enter DB name: ", fg="blue", font=("", 15))
        self.entry_4 = Entry(self.root, width="35")
        self.label_4.grid(row=4, column=0, pady=5, padx=1, sticky=W)
        self.entry_4.grid(row=4, column=1, sticky=E)
        self.entry_4.insert(0, 'mysql')

        # Connect button
        self.button_connect = Button(self.root, text= "Connect", bg="purple", fg="white", height="2",width="10", command = lambda:self.connect())
        self.button_connect.grid(row=5, column=1)

        # Select button
        self.button_select = Button(self.root, text= "Select Table", bg="green", fg="white", height="2",width="10", command = lambda:self.select_table())
        self.button_select.grid(row=6, column=1)

        self.connected = False


    def connect(self):
        """

         Connecting to the selected DB, all the required information is taken from user input via UI.

        """
        print("Log: Connect")

        # Taking the data from user input.
        self.hst = self.entry_1.get()
        self.usr = self.entry_2.get()
        self.pwd = self.entry_3.get()
        self.db_name = self.entry_4.get()

        try:

            # Create a Presentor
            self.presentor = Presentor(self.hst, self.usr, self.pwd, self.db_name, self.executor)

            # Establish a connection
            self.presentor.establish_connection(self.executor)

            # Present available tables
            available_tables = self.executor.show_tables(self.presentor.cursor)
            self.tables_list.delete(0, END)
            self.tables_list.insert(END, *available_tables)

            self.connected = True

        except Exception:
            print("Log: Error - failed to connect to DB.")
            return


    #Presents the selected table
    def select_table(self):
        """

        Method used to build the window and present the selected table and all other components - buttons e.t.c.

        """

        if self.connected == False:
            print("Log: Error - must connect to DB before selecting a table.")
            return


        try:
            if self.tables_list.curselection() == ():
                print("Log: Error - no table is selected from the list.")
                return

            self.selected_table = self.tables_list.get(self.tables_list.curselection())
            print("Log: Selected table: "+str(self.selected_table))

        except TclError as e:
            print(f"Log: Failed to present the table. Terminating.")


        # Window size
        hight = 700
        width = 1300
        size = '%sx%s' % (width, hight)

        try:

            # Open a window
            self.presentor.open_window(size)
            self.presentor.select_table(self.selected_table)

        except AttributeError:
            print("Log: Must connect to DB before selecting a table.")
            return

        # Set headers
        self.presentor.set_headers(self.presentor.executer, self.presentor.tree, self.presentor.cursor,
                                   self.presentor.table, 120)

        # Fill table
        self.presentor.fill_table(self.presentor.executer, self.presentor.tree, self.presentor.cursor,
                                  self.presentor.table)

        # Buttons are created, relevant methods are connected to each button.

        #Button Find By ID (OB - 1)
        self.button_clear_line = Button(self.presentor.root, text="Clear Line", bg="green", fg="white", height="1", width="15", command = lambda: self.clear_line())
        self.button_clear_line.grid(row=6, column=0, padx=20, pady=5, sticky=W)

        #Button Find By Param (OB - 2)
        self.button_find = Button(self.presentor.root, text="Find By Selected Parameter", bg="grey", fg="white", height="1", width="20", command = lambda:self.find_by_param())
        self.button_find.grid(row=6, column=1, padx=1, pady=5, sticky=W)

        # Button Restore (OB - 3)
        self.button_restore = Button(self.presentor.root, text="Restore", bg="grey", fg="white", height="1",width="20", command = lambda:self.restore())
        self.button_restore.grid(row=6, column=2, padx=1, pady=5, sticky=W)

        # Button Query (OB - 4)
        self.button_query = Button(self.presentor.root, text = "Query", bg="grey", fg="white", height="1",width="20", command = lambda:self.run_query())
        self.button_query.grid(row=6, column=3, padx=1, pady=5, sticky=W)

        # Button Order By (OB - 5)
        self.button_order_by = Button(self.presentor.root, text="Order By", bg="blue", fg="white", height="1", width="20", command = lambda:self.order_by())
        self.button_order_by.grid(row=6, column=4, padx=1, pady=5, sticky=W)


        # Button Columns (OB - 6)
        self.button_columns = Button(self.presentor.root, text="Select", bg="purple", fg="white", height="1", width="10", command=lambda:self.select_column())
        self.button_columns.grid(row=8, column=1, padx=1, pady=5, sticky=W)

        # Button Columns (OB - 7)
        self.button_comma = Button(self.presentor.root, text="Comma", bg="Black", fg="white", height="1",width="10", command=lambda: self.insert_comma())
        self.button_comma.grid(row=8, column=1, padx=1, pady=5)


        #Drop Box that contains all table columns
        self.dropdown_menu = StringVar(self.presentor.root)
        self.dropdown_menu.set("Columns")  # default value

        # Columns are taken from the table
        columns = self.executor.get_columns(self.presentor.table, self.presentor.cursor)

        # Header names used in drop down menu.
        w = OptionMenu(self.presentor.root, self.dropdown_menu, *columns)
        w.grid(row=8, column=0, padx=0, pady=5, sticky=E)
        w.config(width = 18, bg = "blue", fg="white")

        # Button Export (OB - 7)
        self.button_export = Button(self.presentor.root, text="Export", bg="blue", fg="white", height="1", width="20", command = lambda:self.export())
        self.button_export.grid(row=8, column=2, padx=1, pady=5, sticky=W)

        # Button Show Only (OB - 8)
        self.button_show_only = Button(self.presentor.root, text="Show Only", bg="blue", fg="white", height="1", width="20", command = lambda:self.show_only())
        self.button_show_only.grid(row=8, column=3, padx=1, pady=5, sticky=W)

        #Button Limit (OB - 9)
        self.button_limit = Button(self.presentor.root, text="Limit", bg="green", fg="white", height="1", width="20", command = lambda:self.limit_by())
        self.button_limit.grid(row=8, column=4, padx=1, pady=5, sticky=W)


        #Entry used to receive user input. Related to "Operation Buttons".
        self.request_input = Entry(self.presentor.root, width="200")
        self.request_input.grid(row=7, column=0, padx=20, pady=10, sticky=W)
        self.request_input.grid(columnspan=5)

        self.tool_tip()

    #Show only
    def show_only(self):
        """

        This method is used to present only the selected columns from all table content.

        """
        print("Log: Show only")
        input = self.request_input.get()

        input = input.replace(" ", "")
        elements = input.split(",")

        headers = self.executor.get_columns(self.presentor.table, self.presentor.cursor)

        # Filtering table columns, saving only the columns selected by the user.
        for x in elements:
            if x not in headers:
                print(F"No such column - {x}")
                self.request_input.delete(0, 'end')
                self.request_input.insert(10, F"No such column - {x}")
                return

        result = self.executor.show_only(self.selected_table, self.presentor.cursor,input)
        self.presentor.customize_headers(self.presentor.executer, self.presentor.tree, self.presentor.cursor, self.presentor.table, elements)


        # Clearing the table to present the result
        for i in self.presentor.tree.get_children():
            self.presentor.tree.delete(i)

        #Inserting content
        counter = 0
        table_content = result
        for line in table_content:
            self.presentor.tree.insert('', 'end', text=counter, values=line)
            counter += 1

    #Select column
    def select_column(self):
        """

        Method used to select column name label from drop down menu.

        """
        insert_after = len(self.request_input.get()) + 1
        self.request_input.insert(insert_after, self.dropdown_menu.get())

    # Insert comma separator
    def insert_comma(self):
        """

        Method used to add comma separator after the last string in command line

        """
        insert_after = len(self.request_input.get()) + 1
        self.request_input.insert(insert_after,", ")



    #Clear Command Line
    def clear_line(self):
        """

        Method used to clean the command line.

        """
        self.request_input.delete(0, 'end')

    #Export
    def export(self):
        """

        Method used to export table data to Excel file

        """
        cursor = self.presentor.cursor
        table = self.presentor.table
        file_name = str(self.presentor.table)+".xls"

        self.executor.excel_all(table, cursor, file_name)
        self.request_input.insert(10, 'Table exported!')


    def restore(self):
        """

        Restores the original table view

        """
        self.presentor.close_window()
        self.select_table()



    #Method Run DB Query
    def run_query(self):
        """

        Method used to run user's SQL query entered to Command Line.

        """
        query = self.request_input.get()
        if len(query)<1 :
            self.request_input.insert(10, 'Cannot be empty!')
            return
        elif query =='Cannot be empty!':
            self.request_input.delete(0, 'end')
            return


        try:

            cursor = self.presentor.cursor
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)

        except pymysql.err.ProgrammingError:

            self.request_input.delete(0, 'end')
            self.request_input.insert(10,'Invalid Query!')
            return

        # Clearing the table to present the result
        for i in self.presentor.tree.get_children():
            self.presentor.tree.delete(i)

        #Entering content
        counter = 0
        table_content = result
        for line in table_content:
            self.presentor.tree.insert('', 'end', text=counter, values=line)
            counter += 1




    #Limit by - present only limited amount of table records
    def limit_by(self):
        """

        Method is used to limit the amount of presented entries.

        """
        print("Log: Limit By method used.")

        # Input - the amount of records to be presented
        limit = self.request_input.get()

        if len(limit)<1 :
            self.request_input.insert(10, 'Cannot be empty!')
            return
        elif limit == 'Cannot be empty!':
            self.request_input.delete(0, 'end')
            return

        try:
            result = self.executor.limit_by(self.selected_table, self.presentor.cursor, limit)

        except pymysql.err.InternalError:
            self.request_input.delete(0, 'end')
            self.request_input.insert(10, 'Please enter a numeric value')
            return

        # Clearing the table to present the result
        for i in self.presentor.tree.get_children():
            self.presentor.tree.delete(i)

        try:
            counter = 0
            table_content = result
            for line in table_content:
                self.presentor.tree.insert('', 'end', text=counter, values=line)
                counter += 1

        except TypeError:
            print("Log: Limit By - invalid input")
            self.restore()


    # Order by - ordering the table by selected column. Order is changed each time.
    def order_by(self):
        """

        Method is used to sort the table by the selected column.
        User input is taken from UI.


        """
        print("Log: Order By")

        #Input - the column by which the table is sorted
        column = self.request_input.get()
        if len(column)<1 :
            self.request_input.insert(10, 'Cannot be empty!')
            return
        elif column =='Cannot be empty!':
            self.request_input.delete(0, 'end')
            return

        try:
            result = self.executor.order_by_column(self.selected_table, self.presentor.cursor,column, self.presentor.order)

        except pymysql.err.InternalError:
            self.request_input.delete(0, 'end')
            self.request_input.insert(10, 'No such column in this table!')
            return

        # Clearing the table to present the result
        for i in self.presentor.tree.get_children():
            self.presentor.tree.delete(i)

        try:
            counter = 0
            table_content = result
            for line in table_content:
                self.presentor.tree.insert('', 'end', text=counter, values=line)
                counter += 1

        except TypeError:
            print("Log: Order By - invalid input.")
            self.restore()

        #Changing the "order" param to the opposite value to the sorting will work correctly each time
        if self.presentor.order == 0:
            self.presentor.order = 1
            print(F"Sorting order: {self.presentor.order}")

        else:
            self.presentor.order = 0
            print(F"Sorting order: {self.presentor.order}")


    #Method "Find By Param"
    def find_by_param(self):
        """

        Method is used to search the table by any selected parameter.
        Any column can be used for this purpose.


        """
        print("Log: Find by param")
        input = self.request_input.get()
        input = input.replace(" ","")
        elements = input.split("=")

        if len(elements)!= 2:
            print("Error - must insert two arguements")
            return

        first = elements[0]
        second = elements[1]

        result = self.executor.find_by_param(self.selected_table, self.presentor.cursor, first, second)

        # Clearing the table to present the result
        for i in self.presentor.tree.get_children():
            self.presentor.tree.delete(i)

        counter = 0
        table_content = result
        for line in table_content:
            self.presentor.tree.insert('', 'end', text=counter, values=line)
            counter += 1


    def tool_tip(self):
        """

        This method us used to bind tooltips to buttons.

        """
        # Button Find By ID tooltip (OB - 1)
        tooltip_find_by_id = Pmw.Balloon(self.presentor.root)
        tooltip_find_by_id.bind(self.button_clear_line, "Clear the command line")

        # Button Find By Param tooltip (OB - 2)
        tooltip_find = Pmw.Balloon(self.presentor.root)
        tooltip_find.bind(self.button_find, "All table entries that contain the entered value are presented, enter the column name and the value: %column name% = %value%")

        # Button Restore tooltip(OB - 3)
        tooltip_button_restore = Pmw.Balloon(self.presentor.root)
        tooltip_button_restore.bind(self.button_restore, "Click to restore the original table and clean the input box")

        # Button Query tooltip(OB - 4)
        tooltip_button_query = Pmw.Balloon(self.presentor.root)
        tooltip_button_query.bind(self.button_query, "Click to execute any valid SQL query")

        # Button Order By tooltip(OB - 5)
        tooltip_button_order_by = Pmw.Balloon(self.presentor.root)
        tooltip_button_order_by.bind(self.button_order_by, "Click to order table by column in ascending or descending order after the column name was entered: %column%")

        # Button Columns tooltip(OB - 6)
        tooltip_button_columns = Pmw.Balloon(self.presentor.root)
        tooltip_button_columns.bind(self.button_columns, "Add the selected column to the string in the input box")


        #Export button tooltip (OB - 7)
        export__button_tooltip = Pmw.Balloon(self.presentor.root)
        export__button_tooltip.bind(self.button_export, "Export table content to EXCEL")

        # Button Show Only (OB - 8)
        show_only_button_tooltip = Pmw.Balloon(self.presentor.root)
        show_only_button_tooltip.bind(self.button_show_only, "Choose the columns you want to be presented separated by comma: %column name%, %column name%,%column name%")

        # Button Show Only (OB - 9)
        limit_button_tooltip = Pmw.Balloon(self.presentor.root)
        show_only_button_tooltip.bind(self.button_limit, "Choose how many entires do you want to be presented")




if __name__ == "__main__":
    run_me = Sky()
    run_me.root.mainloop()
