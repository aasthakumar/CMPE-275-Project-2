import sqlite3
from sqlite3 import Error
 
 
def create_connection(database_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(database_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database_file = "Downloads\\pythonsqlite-assignment.db"
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS Classification (
                                        Review NOT NULL,
                                        Class text
                                    ); """
    
    # create a database connection
    conn = create_connection(database_file)
    if conn is not None:
        # create projects table
        print(sql_create_projects_table)
        create_table(conn, sql_create_projects_table)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()