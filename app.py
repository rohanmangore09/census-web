from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import SessionLocal, init_db
from models import Household, Person

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.before_first_request
def startup():
    init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form
    address = data.get("address", "")
    names = request.form.getlist("name[]")
    ages = request.form.getlist("age[]")
    genders = request.form.getlist("gender[]")
    married_list = request.form.getlist("married[]")
    other_list = request.form.getlist("other[]")

    db = SessionLocal()
    try:
        household = Household(address=address)
        db.add(household)
        db.flush()

        for i, name in enumerate(names):
            if not name.strip():
                continue
            age = None
            try:
                age = int(ages[i]) if ages[i] else None
            except:
                age = None
            gender = genders[i] if i < len(genders) else None
            married = married_list[i] in ["on", "true", "1"] if i < len(married_list) else False
            other = other_list[i] if i < len(other_list) else None
            person = Person(
                household_id=household.id,
                name=name.strip(),
                age=age,
                gender=gender,
                married=married,
                other_info=other,
            )
            db.add(person)

        db.commit()
    except Exception as e:
        db.rollback()
        return f"Error: {e}", 500
    finally:
        db.close()

    return redirect(url_for("index"))

@app.route("/api/households", methods=["GET"])
def get_households():
    db = SessionLocal()
    try:
        households = db.query(Household).all()
        result = []
        for h in households:
            members = []
            for m in h.members:
                members.append({
                    "id": m.id,
                    "name": m.name,
                    "age": m.age,
                    "gender": m.gender,
                    "married": m.married,
                    "other": m.other_info
                })
            result.append({"id": h.id, "address": h.address, "members": members})
        return jsonify(result)
    finally:
        db.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
