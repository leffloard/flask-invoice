from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "sales.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM entries ORDER BY date DESC")
    entries = c.fetchall()

    c.execute("SELECT SUM(amount) FROM entries WHERE type = 'gelir'")
    total_income = c.fetchone()[0] or 0

    c.execute("SELECT SUM(amount) FROM entries WHERE type = 'gider'")
    total_expense = c.fetchone()[0] or 0

    conn.close()
    balance = total_income - total_expense

    return render_template("index.html", entries=entries, income=total_income, expense=total_expense, balance=balance)

@app.route('/add', methods=["GET", "POST"])
def add_entry():
    if request.method == "POST":
        entry_type = request.form["type"]
        description = request.form["description"]
        amount = float(request.form["amount"])

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO entries (type, description, amount) VALUES (?, ?, ?)",
                  (entry_type, description, amount))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("add_entry.html")

@app.route('/delete/<int:id>')
def delete_entry(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM entries WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if request.method == 'POST':
        entry_type = request.form['type']
        description = request.form['description']
        amount = float(request.form['amount'])
        c.execute("UPDATE entries SET type = ?, description = ?, amount = ? WHERE id = ?",
                  (entry_type, description, amount, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    c.execute("SELECT * FROM entries WHERE id = ?", (id,))
    entry = c.fetchone()
    conn.close()
    return render_template('edit_entry.html', entry=entry)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


# Developed by LeffLoard with <3


# Copyright (c) 2025 LeffLoard
# For any developement related queries, you can contact me at contact@leffloard.xyz
# You can find my CV at https://leffloard.xyz

# This code is licensed under the GPL License.
# You can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this code.
# If not, see <https://www.gnu.org/licenses/>.