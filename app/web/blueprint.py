from flask import Blueprint

web = Blueprint('web', __name__)
# 蓝图也可以有自己的静态文件目录和模版目录
# web = Blueprint('web', __name__, static_folder='static', template_folder='templates')
