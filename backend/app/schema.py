# 1. Connect to the database
# 2. Get all table names
# 3. For each table → get its columns and types
# 4. Format it as a readable string
# 5. Return that string
# 6. Close the connection

# Read the database
# → find all tables
# → for each table find all columns and their types
# → format as a readable string
# → return it

import os
import sqlite3

DB_PATH = os.path.join( os.path.dirname( __file__ ), "../../data/database.db" )
def get_schema_string() -> str:
    #  Step 1
    conn = sqlite3.connect( DB_PATH )
    cursor = conn.cursor()

    # Step 2
    cursor.execute( """SELECT name FROM sqlite_master WHERE type='table'""" )
    tables = [ row[0] for row in cursor.fetchall() ]

    schema_parts = []
    # Step 3, note: O(n^2) time complexity, works for now, kinda bad
    for table in tables:
        cursor.execute( f"""PRAGMA table_info({table})""" )
        columns = cursor.fetchall()

        col_defs = []
        for column in columns:
            column_name = column[1]
            column_type = column[2]
            col_defs.append( f"{column_name} {column_type}" )

        # Step 4
        table_string = f"{table}({','.join( col_defs )})"
        schema_parts.append( table_string )

    #  Step 5, 6
    conn.close()
    return "\n".join( schema_parts )
