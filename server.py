from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/alexandria'

db = SQLAlchemy(app)


class Scroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    url = db.Column(db.String(400))
    note = db.Column(db.String(250))

    def __init__(self, title, url, note):
        self.title = title
        self.url = url
        self.note = note

    def __repr__(self):
        return "{}: {}".format(self.note, self.url)


@app.route('/')
def home():
    return render_template('home.html', **{'scrolls': Scroll.query.all()})


@app.route('/add', methods=["POST"])
def add():
    scroll = Scroll(
        request.form['title'],
        request.form['url'],
        request.form['note'])
    db.session.add(scroll)
    db.session.commit()
    return jsonify(
        {
            "message": "We just added {} to your library!".format(
                request.form['title'])})

if __name__ == '__main__':
    app.run()
