print("开始测试...") 
from flask import Flask 
print("Flask 导入成功") 
app = Flask(__name__) 
print("App 创建成功") 
@app.route('/') 
def index(): 
    return "Hello World!" 
if __name__ == '__main__': 
    print("?? 服务器启动中...") 
    app.run(host='0.0.0.0', port=5000, debug=True) 
