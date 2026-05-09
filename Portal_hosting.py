from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# =========================
# MYSQL CONNECTION
# =========================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9856",
    database="Food"
)

cursor = db.cursor()



# =========================
# HOME PAGE
# =========================

@app.route('/')
def home():

    cursor.execute("SELECT * FROM Food_1")

    data = cursor.fetchall()

    return render_template("inventory.html", items=data)

# =========================
# ADD ITEM
# =========================

@app.route('/add', methods=['POST'])
def add_item():

    item = request.form.get("name")
    price = int(request.form.get("price"))


    sql = """

    INSERT INTO Food_1(Item, Price)

    VALUES(%s, %s)

    """

    values = (item, price)

    cursor.execute(sql, values)

    db.commit()

    return redirect('/')

# =========================
# DELETE ITEM
# =========================

@app.route('/delete/<int:id>')
def delete_item(id):

    sql = "DELETE FROM food WHERE id = %s"

    cursor.execute(sql, (id,))

    db.commit()

    return redirect('/')

# =========================
# RUN FLASK
# =========================

if __name__ == "__main__":
    app.run(debug=True)