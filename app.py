from flask import Flask, jsonify, request
import os
import openai
import logging

app = Flask(__name__)

# 設置日誌
logging.basicConfig(level=logging.INFO)

# 配置 OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")  # 替換為你的 API Key 或設置環境變數

# 根路由
@app.route('/')
def index():
    app.logger.info("GET /")
    return "Welcome, this is a Flask app with ChatGPT integration!"

# 健康檢查路由
@app.route('/health')
def health_check():
    app.logger.info("GET /health")
    return jsonify({"status": "healthy"}), 200

# ChatGPT 路由
@app.route('/chat', methods=['POST'])
def chat_with_gpt():
    app.logger.info("POST /chat")
    try:
        # 獲取用戶的輸入
        user_input = request.json.get("message", "")
        if not user_input:
            return jsonify({"error": "Message is required"}), 400

        # 調用 OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 或 "gpt-4" 視你的帳戶權限而定
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        # 提取 ChatGPT 的回應
        chat_response = response['choices'][0]['message']['content']

        return jsonify({"response": chat_response}), 200

    except Exception as e:
        app.logger.error(f"Error in /chat: {e}")
        return jsonify({"error": str(e)}), 500

# 環境變數測試
@app.route('/env')
def show_env():
    app.logger.info("GET /env")
    port = os.getenv("PORT", "5000")
    environment = os.getenv("ENV", "development")
    return jsonify({"PORT": port, "ENV": environment}), 200

# 自定義 404 錯誤處理
@app.errorhandler(404)
def not_found(e):
    app.logger.warning("404 Not Found")
    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000), host='0.0.0.0')
