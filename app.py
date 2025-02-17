from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize Database
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS leads 
                      (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, topic TEXT)""")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template('index.html')

# Route to handle form submission (POST)
@app.route("/submit", methods=["POST"])
def submit():
    data = request.form
    name, email, phone, topic = data.get("name"), data.get("email"), data.get("phone"), data.get("topic")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leads (name, email, phone, topic) VALUES (?, ?, ?, ?)", 
                   (name, email, phone, topic))
    conn.commit()
    conn.close()

    return jsonify({"message": "Form submitted successfully!"})

# Route to get all leads (GET)
@app.route("/leads", methods=["GET"])
def get_leads():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads")
    leads = cursor.fetchall()
    conn.close()

    # Format the data into a list of dictionaries
    leads_list = [{"id": row[0], "name": row[1], "email": row[2], "phone": row[3], "topic": row[4]} for row in leads]
    
    return jsonify(leads_list)  # Return JSON response

@app.route('/supervised_learning')
def supervised_learning():
    return render_template('supervised_learning.html')  # This is the Supervised Learning page

@app.route('/unsupervised-learning')
def unsupervised_learning():
    return render_template('unsupervised_learning.html')  # This is the Unsupervised Learning page

@app.route('/reinforcement-learning')
def reinforcement_learning():
    return render_template('reinforcement_learning.html')  # This is the Reinforcement Learning page


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    