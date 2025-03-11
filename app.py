import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=10.3.25.126,1433;"
    "DATABASE=VBE_BZD_DBC;"
    "UID=usrvbeap;"
    "PWD=Mv.A42-n;"
    "Encrypt=no;"
    "TrustServerCertificate=yes"
)

try:
    conn = pyodbc.connect(conn_str)
    print("Bağlanti başarili!")
    conn.close()
except Exception as e:
    print(f"Hata oluştu: {e}")
