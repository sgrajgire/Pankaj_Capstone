import model
from flask import Flask, render_template, request

app = Flask(__name__)

# This is the Flask file to connect the backend ML model with the frontend HTML code

@app.route('/', methods=['POST', 'GET'])
def get_recommendation():
    '''
    Get top 5 recommended products
    '''
    if request.method == 'POST':
        username = request.form['uname']
        out_data = [[]]
        title=['Index','Product']
        infotext = "Invalid user! please enter valid user name."

        if len(username) > 0:
            infotext, out_data = model.predict(username)                
        return render_template('index.html', info=infotext, data=out_data, headings=title)  
    else:
        return render_template('index.html')  


if __name__ == '__main__':
    app.run(debug=True)