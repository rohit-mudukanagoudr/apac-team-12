import pyodbc
server='ctrlfreaks1.database.windows.net'
database='namdedatabase'
username='azureuser'
password='1qwertyuiop!'
driver='{ODBC Driver 17 for SQL Server}'

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM clients")
        rows = cursor.fetchall()
        
        for row in rows:
            print (str(row))
            # row = cursor.fetchone()