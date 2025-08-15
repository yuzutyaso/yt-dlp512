from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

# cookies.txtのパス
# Renderにデプロイする場合、環境変数で設定することも推奨されます。
COOKIES_FILE = 'cookies.txt'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        # yt-dlpコマンドの実行
        # cookies.txtファイルへのパスを指定
        command = [
            'yt-dlp',
            '--cookies', COOKIES_FILE,
            url
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300 # 5分でタイムアウト
        )

        output = result.stdout
        error = result.stderr
        status_code = result.returncode

        response_data = {
            'output': output,
            'error': error,
            'status_code': status_code
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
