from flask import current_app, render_template


@current_app.route('/')
@current_app.route('/homepage')
def homepage():
    return render_template('homepage.html', title='Homepage')
