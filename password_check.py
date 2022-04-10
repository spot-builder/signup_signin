import pymysql
import re
from pprint import pprint
host = input("Type your host: ") or "localhost"
login = input("Type your login: ") or "root"
password = input("Type your password: ")
database = input("Type your database name: ")

def validate_password(passwd):
    pat = re.compile('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')

    mat = re.search(pat, passwd)

    if mat:
        return True
    else:
        return False


try:
    connection = pymysql.connect(
        host=f"{host}",
        port=3306,
        user=f"{login}",
        password=f"{password}",
        database=f"{database}",
        cursorclass=pymysql.cursors.DictCursor
    )

    def check_password_and_username():
        choice = input("Sign up(0) or sign in(1) or get data by name(2): ")
        if choice == "0":
            print("Type your data below")
            user_sign_up = input("Type your username: ")
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM `users`;")
                for i in cursor.fetchall():
                    if i.get('name') == user_sign_up:
                        print("User already exists")
                        return False
            password_sign_up = input("Type your password: ")
            if validate_password(password_sign_up):
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO `users` (name, password) VALUES" +
                                   f"('{user_sign_up}', '{password_sign_up}');")
                    connection.commit()
                print("Register was successful")
            else:
                print("Password is bad")
        elif choice == "1":
            print("Type your data below")
            user_sign_in = input("Type your username: ")
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM `users` WHERE name='{user_sign_in}'")
                data = cursor.fetchall()
                if data:
                    password_sign_in = input("Type your password: ")
                    if password_sign_in == data[0].get("password"):
                        print("Login was successful")
                    else:
                        print("Wrong password")
                else:
                    print("Wrong name")
        elif choice == "2":
            username = input("Type username of you want get data: ")
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM `users` WHERE name='{username}'")
                pprint(cursor.fetchall())

        else:
            print("Wrong command")


    try:
        check_password_and_username()
    finally:
        connection.close()

except Exception as ex:
    print("Connection failed...")
    print(ex)
