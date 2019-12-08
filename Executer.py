import pymysql
from tabulate import tabulate
import xlwt



class Executer:


            def __init__(self):
                pass


            # Connect to DB
            def connect_me(self,hst, usr, pwd, db_name):
                try:
                    conn = pymysql.connect(host=hst, user=usr, password=pwd, db=db_name, autocommit='True')
                    cursor = conn.cursor()

                # Wrong Credentials error
                except pymysql.err.OperationalError:
                    print("Log: Error - Wrong Credentials or Host")
                    return

                # Wrong DB name error
                except pymysql.err.InternalError:
                    print("Log: Error - Unknown Database")

                return cursor


            # Get Table Column Names
            def get_columns(self, table, cursor):
                request = 'show columns from ''%s'';' % table
                cursor.execute(request)
                columns = cursor.fetchall()
                result = []

                for cl in columns:
                    result.append(cl[0])

                return result


            # Print list in line (simple variation)
            def list_in_line(list):
                result = ""
                for item in list:
                    result = result + item + "\t"
                print(result)


            # Print a table
            def print_table(self,table, cursor):
                column_names = self.get_columns(table, cursor)

                # Getting the table from DB and saving it to "table"
                query = 'select * from ''%s'';' % table
                cursor.execute(query)
                table = cursor.fetchall()

                # Printing the table using "tabulate"
                print(tabulate(table, headers=column_names, tablefmt='orgtbl'))


            # Find a raw in table by ID provided (ID - numeric)
            def find_by_id(self,table, cursor, id):


                try:
                    query = 'select * from ''%s'' where id=''%s'';' % (table, id)
                    cursor.execute(query)
                    result = cursor.fetchall()
                    print(tabulate(result, headers=self.get_columns(table, cursor), tablefmt='orgtbl'))
                    return result

                except pymysql.err.ProgrammingError:
                    print("No such table -" + table)

                except AttributeError:
                    print('Must provide a cursor!')

                except pymysql.err.InternalError:
                    print("ID must be numeric.")


            # Find a raw in table by a parameter provided
            def find_by_param(self,table, cursor, param, value):
                query = 'select * from ''%s'' WHERE %s="%s";' % (table, param, value)

                try:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    print(tabulate(result, headers=self.get_columns(table, cursor), tablefmt='orgtbl'))
                    return result

                except pymysql.err.ProgrammingError:
                    print("Log: Executer - Failed to execute the given query, invalid parameter is provided.")


            #Order the table by provided column
            def order_by_column(self,table,cursor,column,order):

                if order == 0:
                    query = f"select * from {table} order by {column} desc;"
                else:
                    query = f"select * from {table} order by {column} asc;"

                try:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    return result

                except pymysql.err.ProgrammingError:
                    print("Log: Executer - Failed to execute the given query, invalid parameter is provided.")

            #Show only the requested columns
            def show_only(self,table,cursor,columns):

                try:
                    query = F"select {columns} from {table}"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    return result

                except pymysql.err.ProgrammingError:
                    print("Log: Executer - Failed to execute the given query, invalid parameter is provided.")

            #Present only given number of enteries from the table
            def limit_by(self, table, cursor, limited_by):

                try:
                    query = F"select * from {table} limit {limited_by}"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    return result

                except pymysql.err.ProgrammingError:
                    print("Log: Executer - Failed to execute the given query, invalid parameter is provided.")



            # Add a new row to existing table
            def add_row(self,table, cursor):

                columns = self.get_columns(table, cursor)
                values = []

                for current_column in columns:
                    print("Log: Executor - Adding row to the table.")
                    entered = input("Enter " + current_column + " : ")
                    entered = "'" + entered + "'"
                    values.append(entered)

                cols = ",".join(columns)
                vals = ",".join(values)

                query = 'insert into ''%s''(%s) values(%s);' % (table, cols, vals)
                cursor.execute(query)


            # Delete row from table by ID
            def delete_row(table, cursor):
                print("Log: Executor - Delete procedure initiated.")
                id_to_delete = input("Enter the ID of the row: ")
                query = 'delete  from ''%s'' where id=''%s'';' % (table, id_to_delete)
                cursor.execute(query)


            # Alters row in the table after finding it by the provided param
            def alter_row(table, cursor, target_column, target_creterea, updated_column, new_value):
                print("Log: Executor - Altering table row")
                query = 'update ''%s'' set %s="%s" where %s="%s";' % (
                    table, updated_column, new_value, target_column, target_creterea)

                cursor.execute(query)

            #Export a table to Excel
            def excel_all(self,table, cursor,file_name):

                columns = self.get_columns(table, cursor)

                wb = xlwt.Workbook()
                ws = wb.add_sheet('Exported')

                for col_number in range(len(columns)):

                    query = 'select ''%s'' from ''%s'';' % (columns[col_number], table)

                    ws.write(0, col_number, columns[col_number])

                    cursor.execute(query)

                    output = cursor.fetchall()

                    column = []

                    for el in output:
                        column.append(el)

                    print(column)

                    for i in range(len(column)):
                        actual_inserted = str(column[i])[2:-3]
                        ws.write(i + 1, col_number, actual_inserted)

                wb.save(file_name)


            # This class is used to support the feature of table record to object conversion.
            class Dynamic:
                name = " "
                properties = []
                mapped = {}

                def __init__(self):
                    pass


            #Returns one table record converted to object.
            def to_object(self, table, cursor, line):
                query = 'select * from ''%s'' where id=''%s'';' % (table, line)
                cursor.execute(query)
                record = cursor.fetchall()[0]
                columns = self.get_columns(table, cursor)

                mapped = {}

                for x in range(len(record)):
                    mapped.setdefault(columns[x], record[x])

                result = self.Dynamic()

                result.name = str(table)
                result.properties = columns
                result.mapped = mapped

                return result

            #Returns a list of tables related to connected DB
            def show_tables(self, cursor):

                cursor.execute('show tables')
                tups = cursor.fetchall()

                tables = [tup[0] for tup in tups]

                return tables



            def lots_of_eggs(self, cursor, table):
                """
                Get table content as a tuple of tuples

                :cursor: pymysql cursor variable
                :table: SQL table object
                """
                query = 'select * from ''%s'';' % (table)
                cursor.execute(query)
                result = cursor.fetchall()
                return result






