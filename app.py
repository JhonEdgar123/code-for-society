from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Simulated in-memory database
users = {}  # {username: password}
checkins = []  # List of check-in dictionaries

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('checkin'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', error="Username already exists!")
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        mood = request.form['mood']
        stress_level = request.form['stress_level']
        thoughts = request.form['thoughts']
        checkins.append({
            'username': session['username'],
            'mood': mood,
            'stress_level': stress_level,
            'thoughts': thoughts
        })
    user_checkins = [c for c in checkins if c['username'] == session['username']]
    return render_template('checkin.html', checkins=user_checkins)

if __name__ == '__main__':
    app.run(debug=True)
