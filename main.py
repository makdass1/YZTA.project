import bcrypt
import pyodbc
from flask import Flask, render_template, request, jsonify
from genai import take_suggesiton_by_gemini

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('register.html')
@app.route('/login')
def login1():
    return render_template('login.html')

@app.route('/register')
def register1():
    return render_template('register.html')

@app.route('/chatbot')
def chatbt():
    return render_template('chatbot.html')

conn_str = r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=EMIR\SQLEXPRESS;DATABASE=Tasklar;Trusted_Connection=yes;"



def get_db_connection():
    return pyodbc.connect(conn_str)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password']
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE Email = ?", (email,))
    if cursor.fetchone():
        return jsonify({'message': 'Kullanıcı zaten var'}), 400

    cursor.execute("INSERT INTO Users (Email, PasswordHash) VALUES (?, ?)", (email, hashed))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Kayıt başarılı'}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT PasswordHash FROM Users WHERE Email = ?", (email,))
    row = cursor.fetchone()
    conn.close()

    if row and bcrypt.checkpw(password.encode('utf-8'), row[0]):
        return jsonify({'message': 'Giris başarılı'}), 200
    else:
        return jsonify({'message': 'Hatali giris'}), 401







@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    bot_reply = take_suggesiton_by_gemini(user_message)

    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)