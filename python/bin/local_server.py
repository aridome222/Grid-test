from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-command', methods=['POST'])
def run_command():
    # リクエストからコマンドを取得
    data = request.get_json()
    command = data.get("command")

    # コマンドをローカルで実行し、結果を返す
    try:
        # コマンドをシェルで実行
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return jsonify({"output": result.stdout, "error": result.stderr})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)  # 全てのIPからアクセス可能にする
