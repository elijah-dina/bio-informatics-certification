from flask import Flask, render_template, abort, url_for
import os

app = Flask(__name__)
IMAGE_DIR = os.path.join("static", "images")


# Helper: get people from filenames
def get_people():
    people = {}
    for filename in os.listdir(IMAGE_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            name = os.path.splitext(filename)[0]  # e.g., "John Doe"
            slug = name.lower().replace(' ', '-')  # e.g., "john-doe"
            people[slug] = filename
    return people


@app.route('/')
def home():
    people = get_people()
    links = [f'<a href="/{slug}">{slug.replace("-", " ").title()}</a>' for slug in people]
    return "<h1>People</h1>" + "<br>".join(links)


@app.route('/<slug>')
def person(slug):
    people = get_people()
    if slug not in people:
        abort(404)
    image_url = url_for('static', filename=f'images/{people[slug]}')
    name = people[slug].rsplit('.', 1)[0]
    return render_template("person.html", name=name, image_url=image_url)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
