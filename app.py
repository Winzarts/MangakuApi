from flask import Flask
from routes.status import status_bp
from routes.genre import genre_bp
from routes.list_komik import list_bp
from routes.popular import popular_bp
from routes.latest import latest_bp
from routes.search import search_bp
from routes.manga import manga_bp

app = Flask(__name__)

app.register_blueprint(status_bp)
app.register_blueprint(genre_bp)
app.register_blueprint(list_bp)
app.register_blueprint(popular_bp)
app.register_blueprint(latest_bp)
app.register_blueprint(search_bp)
app.register_blueprint(manga_bp)

if __name__ == "__main__":
    app.run(port=3080, debug=True)