from flask import Flask,request,jsonify
import psycopg2 
from psycopg2 import sql 

app = Flask(__name__)

#DataBase Configuration 
DB_HOST = 'localhost'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = '2525'

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
     CREATE TABLE IF NOT EXISTS To_Do_db(
        task_id SERIAL PRIMARY KEY ,
        title  TEXT NOT NULL,
        description TEXT NOT NULL,
        duedate TEXT  NOT NULL,
        priority TEXT NOT NULL,
        status TEXT DEFAULT 'pending'
          );
    """)
    connection.commit()
    cursor.close()
    connection.close()
create_table()
@app.route('/new_task',methods=['POST'])
def new_task():
    title=request.json['title']
    description=request.json['description']
    duedate=request.json['duedate']
    priority=request.json['priority']
    status=request.json['status']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
    INSERT INTO To_Do_db(title,description,duedate,priority,status)
    VALUES (%s,%s,%s,%s,%s)
    """,(title,description,duedate,priority,status))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message':'task added successfully'}),200
@app.route('/get_task_details',methods=['GET'])
def get_task_details():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM To_Do_db;
    """)
    To_Do_db = cursor.fetchall()
    cursor.close()
    connection.close()
    result = [
        {
            "task_id": task[0],
            "title": task[1],
            "description": task[2],
            "duedate":task[3],
            "priority":task[4],
            "status":task[5],
        }
        for task in To_Do_db
    ]
    return jsonify(result), 200
@app.route('/update_task_details',methods=['PUT'])
def update_task_details():
    task_id=request.args['task_id']
    title=request.json['title']
    description=request.json['description']
    duedate=request.json['duedate']
    priority=request.json['priority']
    status=request.json['status']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute( """
    UPDATE To_Do_db
    SET title=%s,description=%s,duedate =%s,priority =%s,status=%s where task_id = %s;
    """,(title,description,duedate,priority,status,task_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message':'task updated successfully'}),201
@app.route('/delete_task',methods=['DELETE'])
def delete_task():
    task_id=request.args.get('task_id')
    connection = get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
    DELETE FROM To_Do_db WHERE task_id=%s;
    """,(task_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message':'task deleted successfully'}),200

if __name__ =='__main__':
        app.run(debug=True)