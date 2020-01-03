"""
 Created by jbn
"""

from flask import Flask, make_response

app = Flask(__name__)
app.config.from_object('config') # 模块路径, 不是文件名
# print(app.config['Debug']) error 配置变量字母必须大写, 否则会被忽略
# print(app.config)  # 'DEBUG': False  是 Flask 的默认配置


# /hello 不兼容 http://localhost:5000/hello/ 
# /hello/ http://localhost:5000/hello 会重定向
# redirect Status Code:301 Location:http://localhost:5000/hello/
@app.route('/hello/')
def hello():
    # Status Code 200,404,301
    # content-type http headers
    # content-type = text/html  默认值
    # return '<html>hello, fishbook</html>'
    headers = {
        'content-type': 'text/plain',
        'location': 'http://www.bing.com'
    }
    # 状态码只是一种标识, 并不会影响内容的显示
    # response = make_response('<html></html>', 301)
    # response.headers = headers
    # return response
    return '<html>hello</html>', 301, headers


# app.add_url_rule('/hello', view_func=hello)
# endpoint 默认为视图函数名称
# app.add_url_rule('/hello', view_func=hello, endpoint='hello')

# 192.168.1.108
if __name__ == '__main__':
    # 生产环境会用 nginx + uwsgi, 不会使用内置服务器
    # 所以需要添加 __name__ == '__main__', 因为不需要被执行
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=8000)