from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('fortraining.csv')

def recommend_phones(df, selected_brand, min_price, max_price, top_n=5):
    filtered_df = df[
        (df['Brand'].str.lower() == selected_brand.lower()) &
        (df['price'] >= min_price) &
        (df['price'] <= max_price)
    ]
    top_phones = filtered_df.sort_values(by='ratings', ascending=False).head(top_n)
    return top_phones[['Brand', 'Model', 'price', 'ratings', 'specifications', 'imgURL']]

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    brand = request.form['brand']
    min_price = float(request.form['min_price'])
    max_price = float(request.form['max_price'])
    prediction = recommend_phones(df, brand, min_price, max_price)
    return render_template('results.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
