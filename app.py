import pickle
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)


# load all input files
user_reco_file = open('./Input_Data/user_recommendation.pkl', 'rb')
user_reco_matrix = pickle.load(user_reco_file)

review_df = pd.read_csv('./Input_Data/product_review.csv')
sentiment_df = pd.read_csv('./Input_Data/clean_df.csv')

sentiment_model_file = open('./Input_Data/best_ML_model_save.pkl', 'rb')
sentiment_model = pickle.load(sentiment_model_file)

tfidf_file = open('./Input_Data/tfidf_vector.pkl', 'rb')
tfidf_vector = pickle.load(tfidf_file)

# prediction 
@app.route('/', methods=['POST', 'GET'])
def predict_recommendation():
    '''
    Predicting the top 5 recommendation product
    '''
    if request.method == 'POST':
        username = request.form['uname']
        out_data = [[]]

        # check for empty user name
        if len(username) == 0:
            infotext = "Invalid user! please enter valid user name."
            return render_template('view.html', info=infotext, data=out_data, headings=['Index','Product'])
                
        # check for valid username
        if username not in user_reco_matrix.index:
            infotext = "Entered user name is not available. Please enter valid user name!"
            return render_template('view.html', info=infotext, data=out_data, headings=['Index','Product'])

        product_ids = user_reco_matrix.loc[username].sort_values(ascending=False)[:20]
        product_map = pd.DataFrame(review_df[['id','name']]).drop_duplicates()

        user_top20 = pd.merge(product_ids, product_map, on='id')
        # Mapping product with product reviews
        product_mapping_review = pd.DataFrame(sentiment_df[['id','reviews_combine','user_sentiment']]).drop_duplicates()
        product_review_data =pd.merge(user_top20, product_mapping_review,left_on='id',right_on='id', how = 'left')

        final_test_data=product_review_data['reviews_combine']
        y_target_final=product_review_data['user_sentiment']

        # get features using tfidf vectorizer
        test_features= tfidf_vector.transform(final_test_data)

        # Predict Sentiment Score on the above Product Reviews using the finally selected ML model
        product_review_data['predicted_sentiment'] = sentiment_model.predict(test_features)
        product_review_data['predicted_sentiment_score'] = product_review_data['predicted_sentiment'].replace(['Negative','Positive'],[0,1])

        # Find positive sentiment percentage for every product
        product_pivot = product_review_data.reset_index().pivot_table(values='predicted_sentiment_score', index='name', aggfunc='mean')
        product_pivot.sort_values(by='predicted_sentiment_score',inplace= True, ascending= False)
        # Get top 5 products
        # product_map[product_map['name'] == out]['id']
        out_data = [[index, out] for index, out in enumerate (product_pivot.head(5).index, 1)]
        infotext = "Top 5 Recommended products for \"" + username +  "\""
        return render_template('view.html', info=infotext, data=out_data, headings=['Index','Product'])  
    else:
        return render_template('view.html')  


if __name__ == '__main__':
    app.run(debug=True)