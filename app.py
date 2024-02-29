# app.py
import os
from flask import Flask, render_template, redirect, url_for, request,session,flash
from utility import get_product_data
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/shirt.html')
def shirt():
    return render_template('shirt.html')

@app.route('/necklace.html')
def necklace():
    return render_template('necklace.html')

@app.route('/glass.html')
def glass():
    return render_template('glass.html')

@app.route('/earrings.html')
def earrings():
    return render_template('earrings.html')

@app.route('/try_shirt_image/<image_name>')
def try_shirt_image(image_name):
    # image_name = request.args.get('image_name', '')
    shirt_path = f"static/shirt_images/{image_name}"

    # Write the path to a file
    with open("shirt_path.txt", "w") as file:
        file.write(shirt_path)

    # Run the shirt.py script
    os.system("python shirt.py")

    # return redirect(url_for('sproduct', product_id='pro1'))
    # return redirect(url_for('shirt', product_id=image_name))
    return redirect(url_for('shirt'))

@app.route('/try_necklace_image/<image_name>')
def try_necklace_image(image_name):
    necklace_path = f"static/necklace_images/{image_name}"

    # Write the path to a file
    with open("necklace_path.txt", "w") as file:
        file.write(necklace_path)

    # Run the necklace.py script
    os.system("python necklace.py")

    return redirect(url_for('necklace'))

@app.route('/try_glass_image/<image_name>')
def try_glass_image(image_name):
    glass_path = f"static/glass_images/{image_name}"

    # Write the path to a file
    with open("glass_path.txt", "w") as file:
        file.write(glass_path)

    # Run the necklace.py script
    os.system("python glass.py")

    return redirect(url_for('glass'))

@app.route('/try_earrings_image/<image_name>')
def try_earrings_image(image_name):
    earrings_path = f"static/earring_images/{image_name}"

    # Write the path to a file
    with open("earrings_path.txt", "w") as file:
        file.write(earrings_path)

    # Run the necklace.py script
    os.system("python earrings.py")

    return redirect(url_for('earrings'))

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/sproduct.html')
# def sproduct():
#     return render_template('sproduct.html')