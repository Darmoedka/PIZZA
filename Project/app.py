from flask import Flask

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

import controllers.index
import controllers.new_reader
import controllers.search
if __name__ == '__main__':
    app.run()