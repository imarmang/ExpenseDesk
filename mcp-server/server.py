# MCP SERVER
# My host is the FastAPI, which has the MCP client inside, the client is responsible to invoke the MCP protocol to connect to the MCP server
# 1. Server setup
#    → create the FastMCP instance
#    → define the database path
#
# 2. Tool 1 — list_tables
#    → returns all table names
#    → no parameters needed
#
# 3. Tool 2 — get_schema
#    → takes a table name
#    → returns columns and types for that table
#
# 4. Tool 3 — execute_query
#    → takes a SQL string
#    → validates it (reject DROP, TRUNCATE, ALTER, DDL)
#    → executes it against the database
#    → returns rows as JSON
#
# 6. Entry point
#    → if __name__ == "__main__": mcp.run()
import sqlite3

from mcp.server.fastmcp import FastMCP
import os

# Step 1
mcp = FastMCP( "ExpenseDesk" )
DB_PATH = os.path.join( os.path.dirname( __file__ ), "../data/database.db" )

# Step 2
# → registers this function as an MCP tool
# → the agent can now call list_tables()
# → FastMCP handles all the protocol details
@mcp.tool()
def list_tables() -> list[ str ]:
    """Returns a list of all table names in the database."""
    try:
        conn = sqlite3.connect( DB_PATH )
        cursor = conn.cursor()
        cursor.execute( "SELECT name FROM sqlite_master WHERE type='table'" )
        tables = [ row[0] for row in cursor.fetchall() ]
        conn.close()
        return tables
    except Exception as ex:
        return [ f"error: { str(ex) }" ]

@mcp.tool()
def get_schema( table_name: str ) -> list[ str ]:
    """Returns column names and types for a given table."""
    try:
        conn = sqlite3.connect( DB_PATH )
        cursor = conn.cursor()
        cursor.execute( f"PRAGMA table_info({table_name})" )
        columns = cursor.fetchall()

        col_defs = []

        # extract name and type from each column
        for column in columns:
            column_name = column[ 1 ]
            column_type = column[ 2 ]
            col_defs.append( f"{column_name} {column_type}" )
        # return as a list of strings
        conn.close()
        return col_defs
    except Exception as ex:
        return [ f"error: { str(ex) }" ]


# 1. if invalid → return an error message
# 2. if valid → connect to database
# 3. execute the SQL
# 4. fetch the results
# 5. return rows as a list of dictionaries
# 6. close the connection
# block DDL (Data Definition Language), approve DML (Data Manipulation Language)
# Allow Read-only operations
# DDL: → DROP, TRUNCATE, ALTER, CREATE
# DML: → SELECT, INSERT, UPDATE, DELETE
@mcp.tool()
def execute_query( sql: str ) -> list[dict]:
    """Executes READ-ONLY SELECT queries against the database."""

    if not sql.strip().upper().startswith( "SELECT" ):
        return [{"error": "Only SELECT queries are allowed. This is a read-only server."}]

    BLOCKED = [ "DROP", "TRUNCATE", "ALTER", "CREATE" ]
    # Step 1
    for keyword in BLOCKED:
        if keyword in sql.upper():
            return [{"error": f"Query contains blocked keyword: {keyword}"}]
    # Step 2
    try:
        conn = sqlite3.connect( DB_PATH )
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        # Step 3
        cursor.execute( sql )
        # Step 4
        rows = [ dict(row) for row in cursor.fetchall() ]
        # Step 5, 6
        conn.close()
        return rows
    except Exception as e:
        return [ {"error": str(e)} ]

if __name__ == "__main__":
    print( "ExpenseDesk MCP server starting...", flush=True )
    mcp.run()

