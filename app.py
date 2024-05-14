from flask import Flask, render_template, request
import main  # Assuming the main logic is in main.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_price', methods=['POST'])
def check_price():
    url = request.form['url']
    budget = float(request.form['budget'])
    
    product_info = main.check_price_and_features(url, budget)
    
    if product_info:
        product_title = product_info['title']
        product_price = product_info['price']
        within_budget = product_info['within_budget']
        features = product_info['features']
    else:
        product_title = None
        product_price = None
        within_budget = None
        features = None

    return render_template('result.html', product_title=product_title, product_price=product_price, within_budget=within_budget, features=features)

if __name__ == '__main__':
    app.run(debug=True)
