from flask import Flask,  render_template, session
from routes.collections import collections_bp
from routes.documents import documents_bp
from routes.authorize import authorize_bp

app = Flask(__name__)

app.register_blueprint(collections_bp, url_prefix='/api')
app.register_blueprint(documents_bp, url_prefix='/api')
app.register_blueprint(authorize_bp, url_prefix='/api')


@app.route('/', methods=['GET'])
def get_index_page():
    return render_template(
        "index.html"
    )


if __name__ == '__main__':
    app.run(debug=True)
