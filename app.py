from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Password strength criteria regex patterns
PATTERNS = {
    "length": r".{8,}",
    "uppercase": r"[A-Z]",
    "lowercase": r"[a-z]",
    "number": r"\d",
    "special": r"[!@#$%^&*(),.?\":{}|<>]"
}

def check_password_strength(password):
    """Check the strength of the given password."""
    strength = {
        "length": bool(re.search(PATTERNS["length"], password)),
        "uppercase": bool(re.search(PATTERNS["uppercase"], password)),
        "lowercase": bool(re.search(PATTERNS["lowercase"], password)),
        "number": bool(re.search(PATTERNS["number"], password)),
        "special": bool(re.search(PATTERNS["special"], password))
    }

    score = sum(strength.values())

    if score == 5:
        return "Strong", strength
    elif 3 <= score < 5:
        return "Medium", strength
    else:
        return "Weak", strength

@app.route("/", methods=["GET", "POST"])
def index():
    feedback = None
    strength_details = None

    if request.method == "POST":
        password = request.form.get("password")
        feedback, strength_details = check_password_strength(password)

    return render_template("index.html", feedback=feedback, strength_details=strength_details)

if __name__ == "__main__":
    app.run(debug=True)
