from flask import Flask, request, render_template, jsonify, redirect, url_for
import requests
import os
from database import init_db, save_history, get_history, delete_record

app = Flask(__name__)
app.secret_key = os.urandom(24)
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

# 初始化数据库
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    history = get_history()
    return render_template('index.html', history=history)

@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.form['prompt']
    
    # 调用DeepSeek API
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)
        answer = response.json()['choices'][0]['message']['content']
        save_history(prompt, answer)
        return jsonify({"status": "success", "answer": answer})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete(record_id):
    delete_record(record_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)