


last_name = 'aaa'
first_name = 'bbb'
patronymic = 'ccc'
birthday = 'ddd'



insert_stmt = "INSERT INTO user (last_name, first_name, patronymic, birthday) VALUES (%s, %s, %s, %s)"
                
data = last_name, first_name, patronymic, birthday

print(insert_stmt%data)

a = "PythonRU"
b = "PythonRU"
c = "%s — целое число, а %s — строка."
print(c%(a,b))