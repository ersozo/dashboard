import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

def get_tables():
    """Get all table names from the database."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT name
            FROM sys.tables
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]
    return tables

def get_columns(table_name):
    """Get column information for the specified table."""
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT c.name, t.name as data_type, 
                   c.max_length, c.is_nullable
            FROM sys.columns c
            JOIN sys.types t ON c.user_type_id = t.user_type_id
            JOIN sys.tables tb ON c.object_id = tb.object_id
            WHERE tb.name = '{table_name}'
            ORDER BY c.column_id
        """)
        columns = cursor.fetchall()
    return columns

def get_sample_data(table_name, limit=5):
    """Get sample data from the specified table."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT TOP {limit} * FROM [{table_name}]")
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return columns, rows
    except Exception as e:
        return [], f"Error: {str(e)}"

if __name__ == "__main__":
    print("Database Tables:")
    tables = get_tables()
    for i, table in enumerate(tables, 1):
        print(f"{i}. {table}")

    if tables:
        table_idx = input("\nEnter table number to inspect (or press Enter to exit): ")
        if table_idx and table_idx.isdigit() and 1 <= int(table_idx) <= len(tables):
            table_name = tables[int(table_idx) - 1]

            print(f"\nColumns in '{table_name}':")
            columns = get_columns(table_name)
            for col_name, data_type, max_length, is_nullable in columns:
                nullable = "NULL" if is_nullable else "NOT NULL"
                max_len = f"({max_length})" if max_length and max_length < 10000 else ""
                print(f"- {col_name}: {data_type}{max_len} {nullable}")

            print(f"\nSample data from '{table_name}':")
            col_names, rows = get_sample_data(table_name)

            if isinstance(rows, str):
                print(rows)  # Error message
            else:
                # Print column names
                if col_names:
                    print(" | ".join(col_names))
                    print("-" * 80)

                    # Print rows
                    for row in rows:
                        print(" | ".join(str(val) for val in row))
