from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars
# import pandas as pd

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    return redirect("/scrape", code=302)


@app.route("/scrape")
def scraper():

    # client = PyMongo.MongoClient(conn)

    # Connect to a database. Will create one if not already available.
    db = mongo.db.mars

    # Drops collection if available to remove duplicates
    db.mars_data.drop()
    marsDict = mission_to_mars.scrape()
    # Creates a collection in the database and inserts the dictionary
    db.mars_data.insert_one(marsDict)

    # browser.quit()
    return render_template("index.html", items=marsDict, image_urls=marsDict['hemisphere_imgs'])


if __name__ == "__main__":
    app.run(debug=True)
