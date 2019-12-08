from tkinter import *
from tkinter import ttk


class Presentor:


    column_length_configurator = 1050
    min_width=150

    #Variable used to check in which order should the column be sorted (asc/desc)
    order = 0

    tree = ""  #Tree parameter used for "Tree" table presentation
    root = ""  #"Root" is used for python window creation
    executer = "" #Executor type object is used to perform actions in MySQL DB (pymysql) - a wraper.
    cursor = ""   #Cursor is the tool used directly to perform actions in MySQL DB
    table= ""  #Selected table


    def __init__(self, hst, usr, pwd, db_name, executer):
        self.hst = hst
        self.usr = usr
        self.pwd = pwd
        self.db_name = db_name
        self.executer = executer

    # Window size
    hight = 800
    width = 1200
    size = '%sx%s' % (width, hight)
    columns_size = 100

    def open_window(self,size):
        """

        Opens a window of the provided size
        :size: The required window size

        """
        # Window
        self.root = Tk()
        self.root.geometry(size)
        self.root.resizable(0, 0)


        # Tree
        self.tree = ttk.Treeview(self.root, heigh=20)
        self.tree.grid(row=4, column=0, padx=20)
        self.tree.grid(columnspan=5)

        hsb = ttk.Scrollbar(self.root, orient="horizontal")
        hsb.configure(command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)
        hsb.grid(row=5, column=0, padx=20, pady=20, columnspan=5, sticky=(W + E))


    def select_table(self,table):
        """

        Table setter
        :table: The selected table that is assigned to the current presentor

        """
        self.table = table


    def establish_connection(self,executer):
        """

        Uses an "executer" type object and presentor instance variables to establish connection to DB

       :executer: "Executer" type object
       :self.hst: Host (inst. var)
       :self.usr: Username (inst. var)
       :self.pwd: Password (inst. var)
       :self.db_name: selected DB name (inst. var)

        """
        self.cursor = self.executer.connect_me(self.hst, self.usr, self.pwd, self.db_name)


    # Sets the header of each column to be table header
    def set_headers(self,executer, tree, cursor, table, columns_size):
        """
        Setting the headers of each column, values taken from the provided table

        :executer: "Executer" type object
        :tree: Treeview object, ttk.Treeview(root)
        :cursor: pymysql cursor variable
        :table: SQL table object
        :columns_size: width of each column
        """

        # Getting headers
        headers = executer.get_columns(table, cursor)
        tree["columns"] = headers

        # Setting width to all column headers basing on columns amount.
        set_width = int(self.column_length_configurator/len(headers))


        # Setting columns width and headers
        for column in headers:
            tree.column(column, width=set_width,minwidth=self.min_width)
            tree.heading(column, text=column)


    #Setting custom headers to a table
    def customize_headers(self,executer, tree, cursor, table,custom_headers):
        """

        This method is used when the user selects several columns to be presented.
        It is used to modify the table headers and present only the names of the selected
        columns.


        :param executer: "Executer" type object
        :param tree: Treeview object, ttk.Treeview(root)
        :param cursor:  pymysql cursor variable
        :param table: SQL table object
        :param custom_headers: list of column names that are to be presented.
        """
        headers = executer.get_columns(table, cursor)
        tree["columns"] = custom_headers


        set_width = int(self.column_length_configurator / len(headers))

        # Setting columns width and headers
        for column in custom_headers:
            tree.column(column, width=set_width, minwidth=self.min_width)
            tree.heading(column, text=column)


    def fill_table(self, executer, tree, cursor, table):
        """

        Filling the provided table with data that cursor currently contains.

        :executer: "Executer" type object
        :tree: Treeview object, ttk.Treeview(root)
        :cursor: pymysql cursor variable
        :table: SQL table object

        """
        counter = 0
        table_content = executer.lots_of_eggs(cursor, table)
        for line in table_content:
            tree.insert('', 'end', text=counter, values=line)
            counter += 1



    def close_window(self):
        """

        Closes the window that runs in current Presentor

        """
        # Window - END
        self.root.destroy()


    def test_method(self):
       return "Presentor is available"


