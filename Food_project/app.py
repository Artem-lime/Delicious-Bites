from flask import Flask, request, render_template, redirect, url_for
import requests
app = Flask(__name__)

API_URL = 'https://api.spoonacular.com'
API_KEY = 'b3b7fbf43f574c2bae973697d378f77e'



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recipes')
def recipes():
    response = requests.get(f"{API_URL}/recipes/random?number=3&includeNutrition=false&apiKey={API_KEY}")
    foods_data = response.json()

    food1 = foods_data['recipes'][0]
    food1_name = food1['title']
    food1_image = food1['image']
    food1_description = food1['summary']

    food2 = foods_data['recipes'][1]
    food2_name = food2['title']
    food2_image = food2['image']
    food2_description = food2['summary']

    food3 = foods_data['recipes'][2]
    food3_name = food3['title']
    food3_image = food3['image']
    food3_description = food3['summary']

    return render_template('recipes.html',
                           food1_name=food1_name,
                           food1_image=food1_image,
                           food1_description=food1_description,
                           food2_name=food2_name,
                           food2_image=food2_image,
                           food2_description=food2_description,
                           food3_name=food3_name,
                           food3_image=food3_image,
                           food3_description=food3_description)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    food_name = request.args.get('name')

    if not food_name:
        return redirect(url_for('index'))

    try:
        # get product id
        response = requests.get(f"{API_URL}/food/ingredients/search?query={food_name}&apiKey={API_KEY}")
        food_data = response.json()
        product = food_data['results'][0]
        product_name = product['name']
        product_id = product['id']

        #get nutrition info from product json
        nutritionRequest = requests.get(f"{API_URL}/recipes/{product_id}/nutritionWidget.json", params = {"apiKey": API_KEY})
        nutrition_data = nutritionRequest.json()

        if food_data and food_data['results']:
            return render_template('search.html',
                                   success=True,
                                   food={
                                       'name': product_name,
                                       'calories': nutrition_data['calories'],
                                       'protein': nutrition_data['protein'],
                                       'carbs': nutrition_data['carbs'],
                                       'fats': nutrition_data['fat']
                                   })
        else:
            return render_template('search.html', success=False, message="Food not found")

    except Exception as e:
        print(e)
        return render_template('search.html', success=False, message="Error fetching food data")


if __name__ == '__main__':
    app.run(debug=True)