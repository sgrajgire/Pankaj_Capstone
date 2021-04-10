# Capstone_RecoSystem
Sentiment-based product recommendation system, this is an upGgrad assigned capstone project

Explanation for each file present current directory.

Input_Data:
./Input_Data/user_recommendation.pkl --> user - user recommnedation model
./Input_Data/product_review.csv --> input raw data [product data]
./Input_Data/clean_df.csv --> clean data frame to get the reviews of predicted users from user recommedation model
./Input_Data/best_ML_model_save.pkl --> sentiment analysis best model [logsistic regression]
./Input_Data/tfidf_vector.pkl --> tfidf vectorizer object to convert the text to features

static:
./static/style.css --> style sheet for index.html

templates:
./templates/index.html --> web page view is designed in this html file

app.py --> interface for flask api to connect ML models with webpage

model.py --> ML related computional functions and reading all the input files

procfile & requirements.txt --> heroku deployment related files

deployed under heroku website, access the website using the below link:
https://recommendation-system-pankaj.herokuapp.com/
