import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


load_dotenv()

app = Flask(__name__)


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://",
                "postgresql://",
                1,
            )

        return database_url

    mysql_user = os.getenv("DB_USER", "root")
    mysql_password = os.getenv("DB_PASSWORD", "")
    mysql_host = os.getenv("DB_HOST", "127.0.0.1")
    mysql_port = os.getenv("DB_PORT", "3306")
    mysql_database = os.getenv(
        "DB_NAME",
        "selenium_test_site",
    )

    encoded_password = quote_plus(mysql_password)

    return (
        f"mysql+pymysql://{mysql_user}:{encoded_password}"
        f"@{mysql_host}:{mysql_port}/{mysql_database}"
    )


app.config["SQLALCHEMY_DATABASE_URI"] = get_database_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(100),
        nullable=False,
    )

    email = db.Column(
        db.String(255),
        nullable=False,
    )

    role = db.Column(
        db.String(100),
        nullable=False,
    )

    experience = db.Column(
        db.String(50),
        nullable=False,
    )

    newsletter = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )


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

        submission = Submission(
            name=name,
            email=email,
            role=role,
            experience=experience,
            newsletter=newsletter,
        )

        db.session.add(submission)
        db.session.commit()

        return render_template(
            "result.html",
            name=name,
            email=email,
            role=role,
            experience=experience,
            newsletter=newsletter,
        )

    return render_template("form.html")

@app.route("/submissions")
def submissions():
    saved_submissions = (
        Submission.query
        .order_by(Submission.created_at.desc())
        .all()
    )

    return render_template(
        "submissions.html",
        submissions=saved_submissions,
    )

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)