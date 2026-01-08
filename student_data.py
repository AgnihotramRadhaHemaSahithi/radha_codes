from flask import Flask,request,jsonify
import psycopg2
from psycopg2 import sql

app=Flask(__name__)


#dB config 

DB_HOST='localhost'
DB_NAME='postgres'
DB_USER='postgres'
DB_PASSWORD='2525'

def get_db_connection():
    connection=psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection

def create_table():
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS students_data_ai(
        student_id SERIAL PRIMARY KEY ,
        studentname TEXT NOT NULL,
        email TEXT NOT NULL,
        phoneno TEXT  NOT NULL,
        rollno TEXT NOT NULL,
        course TEXT NOT NULL,
        coursecode TEXT NOT NULL
        );
        """)
    connection.commit()
    cursor.close()
    connection.close()
create_table()
@app.route('/student_register',methods=['POST'])
def student_register():
    studentname=request.json['studentname']
    email=request.json['email']
    phoneno=request.json['phoneno']
    rollno =request.json['rollno']
    course=request.json['course']
    coursecode=request.json['coursecode']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
    INSERT INTO students_data_ai(studentname,email,phoneno,rollno,course,coursecode)
    VALUES (%s,%s,%s,%s,%s,%s)
    """,(studentname,email,phoneno,rollno,course,coursecode))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message':'student data registered successfully'}),200
@app.route('/get_student_details',methods=['GET'])
def get_student_details():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM students_data_ai;
    """)

    students_data_ai = cursor.fetchall()
    cursor.close()
    connection.close()
    result = [
        {
            "student_id": student[0],
            "studentname": student[1],
            "email": student[2],
            "phoneno":student[3],
            "rollno":student[4],
            "course":student[5],
            "coursecode":student[6]

        }
        for student in students_data_ai
    ]
    return jsonify(result), 200
@app.route('/update_student',methods=['PUT'])
def update_student():
    student_id=request.args['student_id']
    studentname=request.json['studentname']
    email=request.json['email']
    phoneno=request.json['phoneno']
    rollno =request.json['rollno']
    course=request.json['course']
    coursecode=request.json['coursecode']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute( """
    UPDATE students_data_ai
    SET studentname=%s,email=%s,phoneno =%s,rollno =%s,course=%s,coursecode=%s where student_id = %s;
    """,(studentname,email,phoneno,rollno,course,coursecode,student_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message':'user update successfully'}),201
@app.route('/delete_student',methods=['DELETE'])
def delete_student():
    student_id=request.args.get('student_id')
    connection = get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
    DELETE FROM students_data_ai WHERE student_id=%s;
    """,(student_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message':'student deleted successfully'}),200

if __name__ =='__main__':
        app.run(debug=True)


