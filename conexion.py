import pyodbc

conexion = pyodbc.connect(

    'DRIVER={ODBC Driver 17 for SQL Server};'

    'SERVER=biblioteca-kevin-server.database.windows.net;'

    'DATABASE=biblioteca_ucc;'

    'UID=adminbiblioteca;'

    'PWD=Panda3462.13;'

    'Encrypt=yes;'
    'TrustServerCertificate=yes;'
    'Connection Timeout=30;'

)