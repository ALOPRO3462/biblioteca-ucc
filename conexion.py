import pyodbc

conexion = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=.\\SQLEXPRESS;'
    'DATABASE=biblioteca_ucc;'
    'Trusted_Connection=yes;'
)

print("Conexion exitosa")