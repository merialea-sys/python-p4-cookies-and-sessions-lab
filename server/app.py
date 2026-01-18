#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session.clear()
    return {}, 204

@app.route('/articles')
def index_articles():

    pass

@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session["page_views"] if "page_views" in session else 0

    session['page_views'] += 1

    if session['page_views'] > 3:
        return{
            "message": "Maximum pageview limit reached. Please sign up to continue.",
        }, 401
    
    article = Article.query.get(id)

    if not article:
        return {
            "message": "Article not found."
        }, 404
    
    return article.to_dict(), 200

if __name__ == '__main__':
    app.run(port=5555)
