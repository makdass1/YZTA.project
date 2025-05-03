from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    bot_reply = f"Bot: '{user_message}' mesajını aldım."  # Burada basit cevap var
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
