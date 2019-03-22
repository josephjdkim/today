from flask import Flask, render_template, request, session, url_for, redirect
from datetime import datetime
import pymysql.cursors
import creds

app = Flask(__name__)

conn = pymysql.connect(host = creds.HOST,
                       port = creds.PORT,
                       user = creds.USER,
                       password = creds.PASSWORD,
                       db = creds.DB,
                       charset = "utf8mb4",
                       cursorclass = pymysql.cursors.DictCursor)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/submit", methods=["GET", "POST"])
def submit():
    try:
        response = request.form["input"].lower()
        if (response != "good") and (response != "bad"):
            return redirect(url_for("home"))

        cursor = conn.cursor()
        query = "INSERT INTO Response (mood) VALUES(%s)"
        cursor.execute(query, (response))
        conn.commit()
        cursor.close()
        return redirect(url_for("today"))
    except:
        return redirect(url_for("home"))

@app.route("/today", methods=["GET", "POST"])
def today():
    cursor = conn.cursor()
    query = "SELECT mood FROM Response WHERE post_time >= NOW() - INTERVAL 1 DAY"
    cursor.execute(query)
    responses = cursor.fetchall()
    cursor.close()

    goods, bads = 0, 0
    for r in responses:
        if r["mood"] == "good":
            goods += 1
        elif r["mood"] == "bad":
            bads += 1

    avg_color = calculateColor(goods, bads)
    g_percent = str(round(100*(goods/(goods+bads)), 1))
    b_percent = str(round(100*(bads/(goods+bads)), 1))

    return render_template("today.html", color=avg_color, good=g_percent, bad=b_percent)

def calculateColor(g, b):
    good_color = [255, 226, 239]
    bad_color = [91, 80, 127]
    t = g+b

    color_rgb = (int((good_color[0]*g + bad_color[0]*b)/t),
                int((good_color[1]*g + bad_color[1]*b)/t),
                int((good_color[2]*g + bad_color[2]*b)/t))
    color_hex = '#%02x%02x%02x' % color_rgb
    return color_hex

if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=False)
    