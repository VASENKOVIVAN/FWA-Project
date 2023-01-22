from flask import Flask, render_template, jsonify, request, redirect, make_response
import pymysql
from config import host, user, password, db_name
from werkzeug.exceptions import abort

app = Flask(__name__, template_folder="templates")

# try:
#     connection = pymysql.connect(
#         host=host,
#         port=3306,
#         user=user,
#         password=password,
#         database=db_name,
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     print("successfully connected...")
#     print("#" * 20)

#     try:

#         cursor = connection.cursor()

#         # create table
#         # with connection.cursor() as cursor:
#         #     create_table_query = "CREATE TABLE `users`(id int AUTO_INCREMENT," \
#         #                         " name varchar(32)," \
#         #                         " password varchar(32)," \
#         #                         " email varchar(32), PRIMARY KEY (id));"
#         #     cursor.execute(create_table_query)
#         #     print("Table created successfully")

#         # insert data
#         # with connection.cursor() as cursor:
#         #     insert_query = "INSERT INTO `user` (last_name, first_name, patronymic, birthday) VALUES ('Иванов', 'Иван', 'Иванович', '1985.01.14');"
#         #     cursor.execute(insert_query)
#         #     connection.commit()

#         # with connection.cursor() as cursor:
#         #     insert_query = "INSERT INTO `users` (name, password, email) VALUES ('Victor', '123456', 'victor@gmail.com');"
#         #     cursor.execute(insert_query)
#         #     connection.commit()
        
#         # with connection.cursor() as cursor:
#         #     insert_query = "INSERT INTO `users` (name, password, email) VALUES ('Oleg', '112233', 'olegan@mail.ru');"
#         #     cursor.execute(insert_query)
#         #     connection.commit()

#         # with connection.cursor() as cursor:
#         #     insert_query = "INSERT INTO `users` (name, password, email) VALUES ('Oleg', 'kjlsdhfjsd', 'ole2gan@mail.ru');"
#         #     cursor.execute(insert_query)
#         #     connection.commit()
        
#         # with connection.cursor() as cursor:
#         #     insert_query = "INSERT INTO `users` (name, password, email) VALUES ('Oleg', '889922', 'olegan3@mail.ru');"
#         #     cursor.execute(insert_query)
#         #     connection.commit()

#         # update data
#         # with connection.cursor() as cursor:
#         #     update_query = "UPDATE `users` SET password = 'xxxXXX' WHERE name = 'Oleg';"
#         #     cursor.execute(update_query)
#         #     connection.commit()

#         # delete data
#         # with connection.cursor() as cursor:
#         #     delete_query = "DELETE FROM `users` WHERE id = 5;"
#         #     cursor.execute(delete_query)
#         #     connection.commit()

#         # drop table
#         # with connection.cursor() as cursor:
#         #     drop_table_query = "DROP TABLE `users`;"
#         #     cursor.execute(drop_table_query)

#         # select all data from table
#         # with connection.cursor() as cursor:
#         #     select_all_rows = "SELECT * FROM `users`"
#         #     cursor.execute(select_all_rows)
#         #     rows = cursor.fetchall()
#         #     # for row in rows:
#         #     #     print(row)
#         #     # print("#" * 20)
#         #     print(rows)


#     finally:
#         connection.close()
    
# except Exception as ex:
#     print("Connection refused...")
#     print(ex)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/users_page")
def users_page():
    return render_template('users_page.html', users=users())


@app.route("/users_page_detail/<int:id>")
def users_page_detail(id):
    # return jsonify(user_id)
    return render_template('users_page_detail.html', user=user_id(id))


# @app.route("/create_user")
# def create_user():
#     return render_template('create_user.html')


@app.route("/create_user", methods=['POST', 'GET'])
def create_user():
    name_route = "/create_user"
    print("#" * 50 + '\n' + name_route + " " + "#" * (49 - len(name_route)))
    if request.method == 'POST':
        try:
            # Подключение к БД
            connection = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")

            try:
                cursor = connection.cursor()

                last_name = request.form['lastname']
                first_name = request.form['firstname']
                patronymic = request.form['patronymic']
                birthday = request.form['birthday']

                print("Тут: ", last_name, first_name, patronymic, birthday)
                data = last_name, first_name, patronymic, birthday
                insert_stmt = "INSERT INTO user (last_name, first_name, patronymic, birthday) VALUES ('%s', '%s', '%s', '%s')"
                print('Это данные: '+ insert_stmt % data)

                with connection.cursor() as cursor:
                    cursor.execute(insert_stmt % data)
                    connection.commit()
                    
                    if cursor.lastrowid:
                        print('last insert id', cursor.lastrowid)
                    else:
                        print('last insert id not found')
                    
                    return redirect('/create_user')


            finally:
                connection.close()
                print("Connection close...")
            
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    return render_template('create_user.html')

# API
@app.route("/api/v1/users", methods=['GET'])
def users():
    print("#" * 50 + '\n' + "/api/users" + '\n' + "#" * 50)
    try:
        # Подключение к БД
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected..." + '\n' + "#" * 50)

        try:
            cursor = connection.cursor()

            # select all data from table
            with connection.cursor() as cursor:
                select_all_rows = "SELECT * FROM `user`"
                cursor.execute(select_all_rows)
                rows = cursor.fetchall()
                respon = rows
                print(respon)
                return respon
                
        finally:
            connection.close()
        
    except Exception as ex:
        print("Connection refused...")
        print(ex)


@app.route("/api/v1/user/<int:user_id>", methods=['GET'])
def user_id(user_id):
    print("#" * 50 + '\n' + "/user/<int:user_id>" + '\n' + "#" * 50)
    # return jsonify(user_id)
    try:
        # Подключение к БД
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected..." + '\n' + "#" * 50)

        try:
            cursor = connection.cursor()

            with connection.cursor() as cursor:
                select_one_row_by_user_id = "SELECT id, last_name, first_name, patronymic, birthday FROM `user` WHERE id =%s"
                cursor.execute(select_one_row_by_user_id, user_id)
                row = cursor.fetchone()

            print(row)
            if row is None:
                message = jsonify(message="Not Found")
                return make_response(message, 404)

            return jsonify(row)
            
        finally:
            connection.close()
        
    except Exception as ex:
        print("Connection refused...")
        print(ex)


@app.route("/api/v1/create_user", methods=['POST'])
def create_user():
    name_route = "/api/v1/create_user"
    print("#" * 50 + '\n' + name_route + " " + "#" * (49 - len(name_route)))
    if request.method == 'POST':
        try:
            # Подключение к БД
            connection = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")

            try:
                cursor = connection.cursor()

                last_name = request.form['lastname']
                first_name = request.form['firstname']
                patronymic = request.form['patronymic']
                birthday = request.form['birthday']

                print("Тут: ", last_name, first_name, patronymic, birthday)
                data = last_name, first_name, patronymic, birthday
                insert_stmt = "INSERT INTO user (last_name, first_name, patronymic, birthday) VALUES ('%s', '%s', '%s', '%s')"
                print('Это данные: '+ insert_stmt % data)

                with connection.cursor() as cursor:
                    cursor.execute(insert_stmt % data)
                    connection.commit()
                    
                    if cursor.lastrowid:
                        print('last insert id', cursor.lastrowid)
                    else:
                        print('last insert id not found')
                    
                    return redirect('/create_user')


            finally:
                connection.close()
                print("Connection close...")
            
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    return render_template('create_user.html')



@app.route("/api/v1/json-example", methods=['POST', 'GET'])
def json_example():
    if request.method == 'POST':
        request_data = request.get_json()

        language = request_data['language']
        framework = request_data['framework']

        return '''
            The language value is: {}
            The framework value is: {}'''.format(language, framework)
    return 'это гет'

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=True)
    app.run(host="0.0.0.0", port=5001)


