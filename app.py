# Import Libraries
import datetime as dt
import os
import numpy as np
import pandas as pd
import sqlalchemy
from flask_cors import CORS
from flask import Flask, render_template, redirect, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import psycopg2

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)
#################################################

# Database Setup
connection = psycopg2.connect(user = "postgres",
                                  password = "Isla",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "books")

db_string = "postgres://postgres:Isla@localhost:5432/books"
engine = connection.cursor()
db = create_engine(db_string)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/authors")
def authors():
    authors_df = pd.read_sql_query(
                   ''' SELECT DISTINCT author FROM books \
                       ORDER BY author DESC
                   ''' , db)
    i = 0
    authors_list = []
    for i in range(len(authors_df.to_dict('split')['data'])):
        authors = authors_df.to_dict('split')['data'][i][0]

        data = {
            'Author Name' : authors
        }
        authors_list.append(data)
    return jsonify(authors_list)

@app.route("/avgprice_yearly")
def avgprice_yearly():
    avgprice_df = pd.read_sql_query(
                   '''  SELECT year,ROUND(avg(price),2) FROM books \
                        GROUP BY year
                        ORDER BY year;
                   ''' , db)
    i = 0
    avgprice_list = []
    for i in range(len(avgprice_df.to_dict('split')['data'])):
        year = avgprice_df.to_dict('split')['data'][i][0]
        avgprice = avgprice_df.to_dict('split')['data'][i][1]

        data = {
            'Year' : year,
            'Average Price' : avgprice
        }
        avgprice_list.append(data)
    return jsonify(avgprice_list)

@app.route("/avg_rating")
def avg_rating():
    avg_rating_df = pd.read_sql_query(
                   ''' SELECT year,ROUND(avg(rating),2) FROM books \
                       GROUP BY year \
                       ORDER BY year
                   ''' , db)
    i = 0
    avg_rating_list = []
    for i in range(len(avg_rating_df.to_dict('split')['data'])):
        year = avg_rating_df.to_dict('split')['data'][i][0]
        rating =  avg_rating_df.to_dict('split')['data'][i][1]
        data = {
            'Year': year,
            'Average Rating': rating
        }
        avg_rating_list.append(data)
    return jsonify(avg_rating_list)

@app.route("/avg_rating_by_author")
def avg_rating_by_author():
    avg_author_rating_df = pd.read_sql_query(
                   ''' SELECT author,ROUND(avg(rating),2) FROM books \
                       GROUP BY author \
                       ORDER BY author
                   ''' , db)
    i = 0
    avg_author_rating_list = []
    for i in range(len(avg_author_rating_df.to_dict('split')['data'])):
        author = avg_author_rating_df.to_dict('split')['data'][i][0]
        rating =  avg_author_rating_df.to_dict('split')['data'][i][1]
        data = {
            'Author Name': author,
            'Average Rating': rating
        }
        avg_author_rating_list.append(data)
    return jsonify(avg_author_rating_list)


@app.route("/genre_count")
def genre_count():
    genre_count_df = pd.read_sql_query(
                   '''  SELECT year,genre,COUNT(*) FROM books \
                        GROUP BY year,genre \
                        ORDER BY year,genre
                   ''' , db)
    i = 0
    genre_count_list = []
    for i in range(len(genre_count_df.to_dict('split')['data'])):
        year = genre_count_df.to_dict('split')['data'][i][0]
        genre = genre_count_df.to_dict('split')['data'][i][1]
        cnt = genre_count_df.to_dict('split')['data'][i][2]


        data = {
            'Year': year,
            'Genre': genre,
            'Count': cnt
        }
        genre_count_list.append(data)
    return jsonify(genre_count_list)                               

# combined average rating and price per year
@app.route("/avg_rating_price")
def avg_rating_price():
    avg_rating_price_df = pd.read_sql_query(
                   ''' SELECT year, ROUND(avg(rating),2), ROUND(avg(price),2) FROM books \
                       GROUP BY year \
                       ORDER BY year
                   ''' , db)
    i = 0
    avg_rating_price_list = []
    for i in range(len(avg_rating_price_df.to_dict('split')['data'])):
        year = avg_rating_price_df.to_dict('split')['data'][i][0]
        avg_rating =  avg_rating_price_df.to_dict('split')['data'][i][1]
        avg_price =  avg_rating_price_df.to_dict('split')['data'][i][2]     

        data = {
            'Year': year,
            'AvgRating': avg_rating,
            'AvgPrice': avg_price

        }
        avg_rating_price_list.append(data)
    return jsonify(avg_rating_price_list)
   



if __name__ == "__main__":
    app.run(debug=True)