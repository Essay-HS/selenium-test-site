from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    message_type = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == "testuser" and password == "Password123":
            message = "Login successful"
            message_type = "success"
        else:
            message = "Invalid username or password"
            message_type = "error"

    return render_template(
        "login.html",
        message=message,
        message_type=message_type,
    )


@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        role = request.form.get("role", "")
        experience = request.form.get("experience", "")
        newsletter = request.form.get("newsletter") == "yes"

        return render_template(
            "result.html",
            name=name,
            email=email,
            role=role,
            experience=experience,
            newsletter=newsletter,
        )

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)