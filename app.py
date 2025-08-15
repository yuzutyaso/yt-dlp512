from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Renderの環境変数からクッキーの内容を取得
cookies_content = os.environ.get('YTDLP_COOKIES')
COOKIES_FILE = 'cookies.txt'

# アプリケーションの起動時にクッキーファイルを生成
# Renderは毎回新しい環境でアプリを起動するため、
# この処理が必要です。
if cookies_content:
    with open(COOKIES_FILE, 'w') as f:
        f.write(cookies_content)
else:
    print("WARNING: 'YTDLP_COOKIES' environment variable is not set. Downloads requiring login will fail.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # yt-dlpコマンドの構築
        command = [
            'yt-dlp',
            url
        ]

        # クッキーが設定されていればオプションを追加
        if cookies_content:
            command.insert(1, '--cookies')
            command.insert(2, COOKIES_FILE)

        # yt-dlpコマンドの実行
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
    # 開発環境向けの設定
    # Renderではgunicornが起動するため、この部分は無視されます。
    app.run(debug=True, host='0.0.0.0')
