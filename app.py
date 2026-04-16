from app import create_app

app = create_app()

if __name__ == '__main__':
    # 在 5000 port 啟動開發伺服器
    app.run(debug=True, host='0.0.0.0', port=5000)
