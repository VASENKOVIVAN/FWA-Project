from flask import Flask, render_template, jsonify, request, redirect, make_response
import pymysql
from config import host, user, password, db_name, port
from werkzeug.exceptions import abort

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/auth")
def auth():
    return render_template('auth.html')


@app.route("/users_page")
def users_page():
    return render_template('users_page.html', users=api_v1_users())


@app.route("/users_page_detail/<int:id>")
def users_page_detail(id):
    # return jsonify(user_id)
    print("Это тут: ", api_v1_user_user_id(id))
    return render_template('users_page_detail.html', user=api_v1_user_user_id(id))


@app.route("/create_user", methods=['POST', 'GET'])
def create_user():
    name_route = "/create_user"
    print("#" * 50 + '\n' + name_route + " " + "#" * (49 - len(name_route)))
    if request.method == 'POST':
        try:
            # Подключение к БД
            connection = pymysql.connect(
                host=host,
                port=port,
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


@app.route("/users/<int:id>/delete", methods=['GET'])
def users_id_delete(id):

    name_route = "/users/<int:id>/delete"
    print("#" * 50 + '\n' + name_route + " " + "#" * (49 - len(name_route)))

    if request.method == 'GET':
           
        try:
            # Подключение к БД
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")

            try:
                cursor = connection.cursor()

                with connection.cursor() as cursor:
                    select_one_row_by_user_id = "SELECT id, last_name, first_name, patronymic, birthday FROM `user` WHERE id =%s"
                    cursor.execute(select_one_row_by_user_id, id)
                    row = cursor.fetchone()

                print(row)
                if row is None:
                    message = jsonify(message="Not Found")
                    return make_response(message, 404)

                with connection.cursor() as cursor:
                    sql = "DELETE FROM user WHERE id =%s"
                    cursor.execute(sql, id)
                    connection.commit()

                resp = jsonify('User deleted successfully!')
                resp.status_code = 200
                return redirect("/users_page")
                
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    else:
        resp = jsonify('Method Not Allowed!')
        resp.status_code = 405
        return resp




# =======================================================
# A P I =================================================
# =======================================================
@app.route("/api/v1/users", methods=['GET', 'POST', 'DELETE'])
def api_v1_users():

    name_route = "/api/v1/users"
    print("#" * 50 + '\n' + name_route + " " + "#" * (49 - len(name_route)))

    if request.method == 'GET':
        try:
            # Подключение к БД
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")

            try:
                cursor = connection.cursor()

                # select all data from table
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `user`"
                    cursor.execute(sql)
                    data = cursor.fetchall()

                    if data:
                        respon = data
                        print(data)
                        return respon
                    
                    respon = data
                    print(data)
                    return []
                
                    # message = []
                    # return make_response(message, 200)
                    
                    
            finally:
                connection.close()     
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    elif request.method == 'POST':
        try:
            # Подключение к БД
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")

            try:
                cursor = connection.cursor()

                request_data = request.get_json()
                last_name = request_data['last_name']
                first_name = request_data['first_name']
                patronymic = request_data['patronymic']
                birthday = request_data['birthday']

                if last_name and first_name and patronymic and birthday and request.method == 'POST':

                    sql = "INSERT INTO user (last_name, first_name, patronymic, birthday) VALUES ('%s', '%s', '%s', '%s')"
                    data = last_name, first_name, patronymic, birthday
                # print('Это данные: '+ sql % data)

                    with connection.cursor() as cursor:
                        cursor.execute(sql % data)
                        connection.commit()
                
                    if cursor.lastrowid:
                        id = cursor.lastrowid
                        with connection.cursor() as cursor:
                            sql = "SELECT id, last_name, first_name, patronymic, birthday FROM `user` WHERE id =%s"
                            cursor.execute(sql, id)
                            row = cursor.fetchone()
                    else:
                        id = 'last insert id not found'
                    
                    if row is None:
                        message = jsonify(message="Not Found")
                        return make_response(message, 404)

                    return make_response(jsonify(row), 201)

            finally:
                connection.close()
                print("Connection close...")     
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    elif request.method == 'DELETE':
        try:
            # Подключение к БД
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")

            try:
                cursor = connection.cursor()

                sql = "DELETE FROM user"

                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    connection.commit()
            
                message = jsonify(message='Users deleted successfully!')
                return make_response(message, 200)

            finally:
                connection.close()
                print("Connection close...") 
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    else:
        resp = jsonify('Method Not Allowed!')
        resp.status_code = 405
        return resp


@app.route("/api/v1/users/<int:user_id>", methods=['GET', 'DELETE'])
def api_v1_user_user_id(user_id):

    name_route = "/api/v1/user/<int:user_id>"
    print("#" * 50 + '\n' + name_route + " " + "#" * (49 - len(name_route)))
    
    if request.method == 'GET':
        try:
            # Подключение к БД
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")

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

                return row
                
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    elif request.method == 'DELETE':
        try:
            # Подключение к БД
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")

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

                with connection.cursor() as cursor:
                    sql = "DELETE FROM user WHERE id =%s"
                    cursor.execute(sql, user_id)
                    connection.commit()

                resp = jsonify('User deleted successfully!')
                resp.status_code = 200
                return resp
                
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    else:
        resp = jsonify('Method Not Allowed!')
        resp.status_code = 405
        return resp



# @app.route("/api/v1/create_user", methods=['POST', 'DELETE'])
# def api_v1_create_user():
#     name_route = "/api/v1/create_user"
#     print("#" * 50 + '\n' + name_route + " " + "#" * (49 - len(name_route)))
#     try:
#         # Подключение к БД
#         connection = pymysql.connect(
#             host=host,
#             port=port,
#             user=user,
#             password=password,
#             database=db_name,
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         print("successfully connected...")

#         try:
#             cursor = connection.cursor()

#             request_data = request.get_json()
#             last_name = request_data['last_name']
#             first_name = request_data['first_name']
#             patronymic = request_data['patronymic']
#             birthday = request_data['birthday']

#             if last_name and first_name and patronymic and birthday and request.method == 'POST':

#                 sql = "INSERT INTO user (last_name, first_name, patronymic, birthday) VALUES ('%s', '%s', '%s', '%s')"
#                 data = last_name, first_name, patronymic, birthday
#             # print('Это данные: '+ sql % data)

#                 with connection.cursor() as cursor:
#                     cursor.execute(sql % data)
#                     connection.commit()
            
#                 if cursor.lastrowid:
#                     id = cursor.lastrowid
#                     with connection.cursor() as cursor:
#                         sql = "SELECT id, last_name, first_name, patronymic, birthday FROM `user` WHERE id =%s"
#                         cursor.execute(sql, id)
#                         row = cursor.fetchone()
#                 else:
#                     id = 'last insert id not found'
                
#                 if row is None:
#                     message = jsonify(message="Not Found")
#                     return make_response(message, 404)

#                 return make_response(jsonify(row), 201)

#         finally:
#             connection.close()
#             print("Connection close...")
        
#     except Exception as ex:
#         print("Connection refused...")
#         print(ex)













# =======================================================
# =======================================================
# =======================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=True)
    # app.run(host="0.0.0.0", port=5001)


