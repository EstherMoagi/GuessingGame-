from flask import Flask, render_template, request, redirect, url_for, session
import random
import time

app = Flask(__name__)
app.secret_key = 'secret-key'  # Needed to store data between requests

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        difficulty = request.form['difficulty']
        if difficulty == '1':
            secret_number = random.randint(1, 50)
            max_range = 50
        elif difficulty == '2':
            secret_number = random.randint(1, 100)
            max_range = 100
        else:
            secret_number = random.randint(1, 200)
            max_range = 200

        # Store game data in session
        session['secret_number'] = secret_number
        session['max_range'] = max_range
        session['attempts'] = 0
        session['guess_history'] = []
        session['start_time'] = time.time()

        return redirect(url_for('game'))

    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    message = ""
    if request.method == 'POST':
        guess = int(request.form['guess'])
        session['attempts'] += 1
        session['guess_history'].append(guess)

        secret_number = session['secret_number']

        if guess < secret_number:
            message = "Too low! Try again."
        elif guess > secret_number:
            message = "Too high! Try again."
        else:
            elapsed_time = time.time() - session['start_time']
            return render_template('game.html', 
                                   message=f'🎉 Correct! You guessed it in {session["attempts"]} attempts and {elapsed_time:.2f} seconds!',
                                   guess_history=session['guess_history'], 
                                   game_over=True)

    return render_template('game.html', 
                           message=message, 
                           guess_history=session['guess_history'], 
                           game_over=False)

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

@app.route('/debug')
def debug():
    from os import listdir
    try:
        files = listdir('static/audio')
        return f"Files in /static/audio/: {files}"
    except Exception as e:
        return f"Error reading directory: {e}"

if __name__ == '__main__':
    app.run(debug=True)
