from flask import Flask, render_template, request, redirect, url_for, session
import os
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey' 

@app.route('/')
def home():
    signed_in = session.get('signed_in', False)
    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '').lower()

    current_dir = os.path.abspath(os.path.dirname(__file__))
    image_folder = os.path.join(current_dir, 'static', 'images')

    if not os.path.exists(image_folder):
        return f"The directory {image_folder} does not exist.", 404

    images = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

    if search_query:
        images = [img for img in images if search_query in img.lower()]

    if category_filter:
        images = [img for img in images if category_filter in img.lower()]

    random.shuffle(images)

    return render_template('index.html', signed_in=signed_in, images=images)

@app.route('/signin', methods=['POST'])
def signin():
    session['signed_in'] = True
    return redirect(url_for('home'))

@app.route('/signout')
def signout():
    session['signed_in'] = False
    return redirect(url_for('home'))

@app.route('/image/<filename>')
def display_image(filename):
    image_title = filename.replace(".jpg", "")
    current_dir = os.path.abspath(os.path.dirname(__file__))
    image_folder = os.path.join(current_dir, 'static', 'images')

    if not os.path.exists(image_folder):
        return f"The directory {image_folder} does not exist.", 404

    images = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    recommended_images = random.sample(images, 3)
    return render_template('image.html', filename=filename, image_title=image_title, recommended_images=recommended_images)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
