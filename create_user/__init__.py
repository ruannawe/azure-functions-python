import azure.functions as func
import pyodbc


def connection():
    server = 'tcp:crud-example.database.windows.net'
    database = 'Crud'
    username = 'ruannawe'
    password = 'Bleat@95'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor, cnxn


def main(req: func.HttpRequest) -> func.HttpResponse:
    cursor, cnxn = connection()

    req_body   = req.get_json()
    first_name = req_body.get('firstName')
    last_name  = req_body.get('lastName')
    age        = req_body.get('age')

    cursor.execute(
        """INSERT INTO users (first_name, last_name, age) VALUES (?, ?, ?);""",
        first_name,
        last_name,
        str(age)
    )
    cnxn.commit()

    user_id = cursor.execute('SELECT @@IDENTITY AS id;').fetchone()[0]

    row = cursor.execute(
        """SELECT * FROM users WHERE id = ? FOR JSON AUTO, WITHOUT_ARRAY_WRAPPER;""",
        user_id
    ).fetchone()

    func.HttpResponse.mimetype = 'application/json'
    func.HttpResponse.charset = 'utf-8'
    func.HttpResponse.status_code = 200

    return func.HttpResponse(row[0])
