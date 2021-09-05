from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


@app.route("/")
def home():


    mars_input1 = mongo.db.facts.find_one()
    
    return render_template("index.html", mars_input = mars_input1)


@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scrape_info()

    mongo.db.facts.update({}, mars_data, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)