import pymysql
from tabulate import tabulate
import xlwt
import xlrd

##conn=pymysql.connect(host='127.0.0.1',user='root',password='7417418',db='play')

hst = '127.0.0.1'
usr = 'root'
pwd = '7417418'
db_name = 'play'


class Executer:

            saved = ""


            def __init__(self):
                pass


            # Connect to DB
            def connect_me(self,hst, usr, pwd, db_name):
                try:
                    conn = pymysql.connect(host=hst, user=usr, password=pwd, db=db_name, autocommit='True')
                    cursor = conn.cursor()
                # Wrong Credentials error
                except pymysql.err.OperationalError:
                    print("Wrong Credentials or Host")

                # Wrong DB name error
                except pymysql.err.InternalError:
                    print("Unknown Database")

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
                # list_in_line(column_names)

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
                # query='select * from ''game'' WHERE name="Edge";'
                cursor.execute(query)
                result = cursor.fetchall()
                print(tabulate(result, headers=self.get_columns(table, cursor), tablefmt='orgtbl'))
                return result


            #Order the table by provided column
            def order_by_column(self,table,cursor,column,order):

                if order == 0:
                    query = f"select * from {table} order by {column} desc;"
                else:
                    query = f"select * from {table} order by {column} asc;"
                cursor.execute(query)
                result = cursor.fetchall()
                return result

            #Show only the requested columns
            def show_only(self,table,cursor,columns):

                query = F"select {columns} from {table}"
                cursor.execute(query)
                result = cursor.fetchall()
                return result

            #Present only given number of enteries from the table
            def limit_by(self, table, cursor, limited_by):

                query = F"select * from {table} limit {limited_by}"
                cursor.execute(query)
                result = cursor.fetchall()
                return result



            # Add a new row to existing table
            def add_row(table, cursor):
                # cols=[]

                columns = get_columns(table, cursor)
                values = []

                for current_column in columns:
                    print("Adding row.")
                    entered = input("Enter " + current_column + " : ")
                    entered = "'" + entered + "'"
                    values.append(entered)

                cols = ",".join(columns)
                vals = ",".join(values)

                print("****" + cols)
                print("####" + vals)
                # query='insert into ''%s''(%s) values("817450","Test2","0");'%(table,cols)
                query = 'insert into ''%s''(%s) values(%s);' % (table, cols, vals)
                cursor.execute(query)


            # Delete row from table by ID
            def delete_row(table, cursor):
                print("Delete procedure initiated.")
                id_to_delete = input("Enter the ID of the row: ")
                query = 'delete  from ''%s'' where id=''%s'';' % (table, id_to_delete)
                cursor.execute(query)


            # Alters row in the table after finding it by the provided param
            def alter_row(table, cursor, target_column, target_creterea, updated_column, new_value):
                print("Altering row")
                query = 'update ''%s'' set %s="%s" where %s="%s";' % (
                    table, updated_column, new_value, target_column, target_creterea)
                # query='update game set name="Edges" WHERE name="Edge";'

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


            class Dynamic:
                name = " "
                properties = []
                mapped = {}

                def __init__(self):
                    pass


            #Returns one table record as an object
            def to_object(table, cursor, line):
                query = 'select * from ''%s'' where id=''%s'';' % (table, line)
                cursor.execute(query)
                record = cursor.fetchall()[0]
                columns = get_columns(table, cursor)

                mapped = {}

                for x in range(len(record)):
                    mapped.setdefault(columns[x], record[x])

                result = Dynamic()

                result.name = str(table)
                result.properties = columns
                result.mapped = mapped

                # print(record)

                return result

            #Returns a list of tables related to connected DB
            def show_tables(self,cursor):

                cursor.execute('show tables')
                tups = cursor.fetchall()

                tables = [tup[0] for tup in tups]

                return tables



            def lots_of_eggs(self, cursor, table):
                """Get table content as a tuple of tuples

                       :cursor: pymysql cursor variable
                       :table: SQL table object
                """
                query = 'select * from ''%s'';' % (table)
                cursor.execute(query)
                result = cursor.fetchall()
                return result


            def keeper(self, saved_object):
                self.saved = saved_object



            #######################################


example = Executer()
cursor = example.connect_me(hst, usr, pwd, db_name)
# print(example.lots_of_eggs(cursor,"game"))
example.print_table('game', cursor)


            # print (show_tables('game',cursor))

            #
            # cols=get_columns('game',cursor)
            #
            # list_in_line(cols)

            # print(get_columns('game', cursor))

            # add_row('game',cursor)


            #
            # example = to_object('game', cursor, 645450)
            #
            # print(example.mapped)

            # excel_all('game',cursor)

            # delete_row('game',cursor)

            # def alter_row(table,cursor,target_column,target_creterea,updated_column,new_value):

            # alter_row('game', cursor, 'name', 'Edges', 'id', '883450')
            #
            # print_table('game', cursor)

            # find_by_id('game',cursor,'663250')

            # find_by_param('game',cursor,'name','7 Wonders II')


            # name='Paul'
            # {FORMATING EXAMPLE!}
            # print("Hello, %s!. Nice to meet you. My name is %s" % (name,'John'))
