from flask import Flask, request, redirect, render_template
import sqlite3



app = Flask(__name__)
# Function to add a quest


def add_quest(name, exp_reward):
    conn = sqlite3.connect("rpg_game.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quests (name, exp_reward) VALUES (?, ?)", (name, exp_reward))
    conn.commit()
    conn.close()


# Function to get player data
def get_player():
    conn = sqlite3.connect("rpg_game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT level, exp FROM player WHERE id=1")
    player = cursor.fetchone()
    conn.close()
    return player if player else (1, 0)  # Default to level 1, EXP 0 if missing

# Database setup
def init_db():
    conn = sqlite3.connect("rpg_game.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player (
            id INTEGER PRIMARY KEY,
            level INTEGER,
            exp INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            exp_reward INTEGER
        )
    """)
    cursor.execute("SELECT * FROM player")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO player (level, exp) VALUES (?, ?)", (1, 0))
    conn.commit()
    conn.close()

init_db()

# Function to complete a quest
def complete_quest(quest_id):
    conn = sqlite3.connect("rpg_game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT exp_reward FROM quests WHERE id=?", (quest_id,))
    quest = cursor.fetchone()
    if quest:
        exp_reward = quest[0]
        level, exp = get_player()
        exp += exp_reward
        level_up_exp = 100  # EXP required for each level-up
        while exp >= level_up_exp:
            exp -= level_up_exp
            level += 1
        cursor.execute("UPDATE player SET level=?, exp=? WHERE id=1", (level, exp))
        cursor.execute("DELETE FROM quests WHERE id=?", (quest_id,))
    conn.commit()
    conn.close()

# Function to delete a quest
def delete_quest(quest_id):
    conn = sqlite3.connect("rpg_game.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quests WHERE id=?", (quest_id,))
    conn.commit()
    conn.close()

# Function to reset player progress
def reset_player():
    conn = sqlite3.connect("rpg_game.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE player SET level=1, exp=0 WHERE id=1")
    conn.commit()
    conn.close()

@app.route('/delete_quest/<int:quest_id>')
def delete_quest_route(quest_id):
    delete_quest(quest_id)
    return redirect('/')

@app.route('/reset_player')
def reset_player_route():
    reset_player()
    return redirect('/')

@app.route('/')
def index():
    player = get_player()
    conn = sqlite3.connect("rpg_game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quests")
    quests = cursor.fetchall()
    conn.close()

    # Pass player and quests to the HTML file
    return render_template('index.html', player=player, quests=quests)

@app.route('/add_quest', methods=['POST'])
def add_quest_route():
    name = request.form['name']
    exp_reward = int(request.form['exp_reward'])
    add_quest(name, exp_reward)
    return redirect('/')

@app.route('/complete_quest/<int:quest_id>')
def complete_quest_route(quest_id):
    complete_quest(quest_id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
