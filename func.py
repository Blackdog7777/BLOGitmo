import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import init_db


def setup():
    init_db.init_db()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///F://BLOGitmo//database.db'

    def get_db_connection():
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn

    def get_post(post_id):
        conn = get_db_connection()
        posts = conn.execute('SELECT * FROM posts WHERE id = ?',
                             (post_id,)).fetchone()
        conn.close()
        if posts is None:
            abort(404)
        return posts

    def get_comment():
        conn = get_db_connection()
        posts = conn.execute('SELECT * FROM comments',).fetchall()
        conn.close()
        if posts is None:
            abort(404)
        return posts

    # Обработка страниц

    @app.route('/')
    def draw_main_page():
        conn = get_db_connection()
        posts = conn.execute('SELECT * FROM posts ORDER BY likes DESC').fetchall()
        conn.close()
        return render_template('index.html', posts=posts)

    @app.route('/<int:post_id>')
    def post(post_id):
        get_value = get_post(post_id)
        return render_template('post.html', post=get_value)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/create', methods=('GET', 'POST'))
    def create():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            author = request.form['author']

            if not title:
                flash('Введите заголовок!')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
                             (title, content, author))
                conn.commit()
                conn.close()
                return redirect(url_for('draw_main_page'))

        return render_template('create.html')

    @app.route('/<int:id>/edit', methods=('GET', 'POST'))
    def edit(id):
        get_value = get_post(id)

        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']

            if not title:
                flash('У поста должен быть заголовок!')
            else:
                conn = get_db_connection()
                conn.execute('UPDATE posts SET title = ?, content = ?'
                             ' WHERE id = ?',
                             (title, content, id))
                conn.commit()
                conn.close()
                return redirect(url_for('draw_main_page'))

        return render_template('edit.html', post=get_value)

    @app.route('/<int:id>/delete', methods=['POST'])
    def delete(id):
        get_value = get_post(id)
        conn = get_db_connection()
        conn.execute('DELETE FROM posts WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('"{}" был успешно удален!'.format(get_value['title']))
        return redirect(url_for('draw_main_page'))

    @app.route('/comment', methods=('GET', 'POST'))
    def comment():
        if request.method == 'POST':
            name = request.form['name']
            content = request.form['content']

            if not name or not content:
                flash('Заполните поля!')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO comments (name, content) VALUES (?, ?)',
                             (name, content))
                conn.commit()
                conn.close()
                return redirect(url_for('comment'))

        return render_template('comment.html', posts=get_comment())

    @app.route('/<int:id>/like', methods=["POST", "GET"])
    def like(id):
        get_value = get_post(id)
        count_of_likes = get_value['likes']
        conn = get_db_connection()
        conn.execute('UPDATE posts SET likes = ? WHERE id = ? ', (count_of_likes + 1, id,))
        conn.commit()
        conn.close()
        flash('"{}" был успешно лайкнут!'.format(get_value['title']))
        return redirect(url_for('draw_main_page'))

    # Ошибки HTML

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(403)
    def page_not_found(e):
        return render_template("403.html"), 403

    if __name__ == 'func':
        app.run()
