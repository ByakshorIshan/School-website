# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# # @app.route("/")
# # def index():
# #     return flask.redirect("/login")
#
# @app.route('/login', methods=["GET", "POST"])
# def login():
#     return render_template("login.html")
#
# @app.route('/admin')
# def admin():
#     return render_template("admin.html")
#
#
# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create mock user database
users = {'john@example.com': {'password': 'password', 'name':'JHON', 'profile_picture': '', 'classes': [], 'remarks': []}}

# Define User model
class User(UserMixin):
    def __init__(self, email):
        self.id = email
        self.name = users[self.email]["name"]
        self.profile_picture = users[self.email]["profile_picture"]
        self.classes = users[self.email]["classes"]
        self.remarks = users[self.email]["remarks"]

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    user = User(user_id)
    return user


# Define login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            user = User(email)
            login_user(user)
            return redirect(url_for('admin', email=email))
        else:
            return render_template('login.html', error=True)
    return render_template('login.html')

# Define logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Define admin route
@app.route('/admin')
@login_required
def admin():
    user = User(request.args.get('email'))
    return render_template('admin.html', name=user.name)

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
