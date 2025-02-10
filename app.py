from flask import Flask, render_template, request, redirect, url_for, flash
import os
#import pandas as pd
from werkzeug.utils import secure_filename

from helpers import process_csv, add_results_to_csv

# Configure application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Ensure the uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        # Get the file from the post
        file = request.files['file']

        # Check again if there is a file and the file has a name
        if not file or file.filename == '':
            return redirect("/upload")

        # Create a secure filename and save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Analyze the data
        results = process_csv("uploads/"+filename)

        # Add the results to the csv file
       # add_results_to_csv("uploads/"+filename , results)
       # file.save(file_path)

        # Return the results page with the results loaded
        return render_template("results.html", results=results)

    else:
        return render_template("upload.html")

@app.route("/about")
def about():
    return render_template("about.html")