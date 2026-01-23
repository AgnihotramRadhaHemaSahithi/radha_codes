from flask import Flask,request,jsonify
import psycopg2
from flask_bcrypt import Bcrypt

app=Flask(__name__)
bcrypt =Bcrypt(app)


#dB config 

DB_HOST='localhost'
DB_NAME='postgres'
DB_USER='postgres'
DB_PASSWORD='2525'
#db connection function 

def get_db_connection():
    connection=psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection
#table creation 
def create_tb_if_not_exist():
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
                   user_id SERIAL PRIMARY KEY,
                   username TEXT NOT NULL,
                   password TEXT NOT NULL,
                   email TEXT NOT NULL
                   );
                   """)
    connection.commit()
    cursor.close()
    connection.close()
create_tb_if_not_exist()


def create_form_table_if_not_exists():
    connection = get_db_connection()
    cursor =connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_forms(
    form_id SERIAL PRIMARY KEY ,
    user_id INTEGER,
    full_name TEXT,
    age TEXT,
    course TEXT );
    """)
    connection.commit()
    cursor.close()
    connection.close()
create_form_table_if_not_exists()


@app.route("/signup",methods=['POST'])
def signup():
    username=request.json['username']
    password=request.json['password']
    email=request.json['email']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
        INSERT INTO userdata(username,password,email)
        VALUES(%s,%s,%s)
    """, (username,hashed_password,email))
    

    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "User signup successful"}),201
@app.route('/login',methods=['POST'])
def login():
    email=request.json['email']
    password=request.json['password']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
    SELECT user_id,username,password
    FROM userdata WHERE email=%s
    """,(email,))
    user =cursor.fetchone()
    cursor.close()
    connection.close()
    if user is None:
        return jsonify({'error':'user not found'}),404
    user_id,username,hashed_password= user
    if not bcrypt.check_password_hash(hashed_password,password):
        return jsonify({'error':'invalid password'}),401
    return jsonify({
        "message":"login successful",
        "user":{
            "user_id":user_id,
            "username":username,
            "email":email
        }
    }),200







@app.route('/apply',methods=['POST'])
def apply():
    user_id=request.json['user_id']
    full_name=request.json['full_name']
    age=request.json['age']
    course=request.json['course']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
    INSERT INTO student_forms (user_id,full_name,age,course)
    VALUES (%s,%s,%s,%s)
    """,(user_id,full_name,age,course))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message':'student applied  successfully'}),200
@app.route('/get_student_details',methods=['GET'])
def get_student_details():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM student_forms;
    """)
    student_forms = cursor.fetchall()
    cursor.close()
    connection.close()
    result = [
        {
           "user_id":student[1],
           "full_name":student[2],
           "age":student[3],
           "course":student[4]
        }
        for student in student_forms
    ]
    return jsonify(result), 200
@app.route('/update_student_details',methods=['PUT'])
def update_student_details():
    user_id=request.json['user_id']
    full_name=request.json['full_name']
    age=request.json['age']
    course=request.json['course']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute( """
    UPDATE student_forms
    SET user_id=%s,full_name=%s,age =%s,course =%s
    """,(user_id,full_name,age,course))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message':'student updated successfully'}),201
@app.route('/delete_student',methods=['DELETE'])
def delete_student():
    user_id=request.args.get('user_id')
    connection = get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
    DELETE FROM student_forms WHERE user_id=%s;
    """,(user_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message':'student deleted successfully'}),200
if __name__ =='__main__':
    app.run(debug=True)