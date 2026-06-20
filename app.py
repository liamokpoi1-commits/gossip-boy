import os
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)

# Secret key
app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY',
    'super-secret-gossip-key'
)

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'gossip123')

# Sample post
blog_posts = [
    {
        "title": "Welcome to Gossip Girl",
        "content": "Spotted: The ultimate Python story blog going live on Render. XOXO...",
        "image": "https://images.unsplash.com/photo-1522158632604-63824b3c4baf?w=500"
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Gossip Girl Blog</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #fff0f5;
            padding: 20px;
        }
        .container {
            max-width: 700px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
        }
        h1 {
            color: #d11141;
            text-align: center;
        }
        .post {
            border-left: 5px solid #d11141;
            padding: 15px;
            margin-bottom: 15px;
            background: #fafafa;
        }
        img {
            max-width: 100%;
            border-radius: 5px;
        }
        input, textarea {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        button {
            background: #d11141;
            color: white;
            border: none;
            padding: 10px;
            width: 100%;
            cursor: pointer;
        }
        a {
            color: #d11141;
            text-decoration: none;
        }
        .nav {
            text-align: right;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
<div class="container">

    <h1>Gossip Girl</h1>

    <div class="nav">
        {% if logged_in %}
            Logged in as Admin |
            <a href="{{ url_for('logout') }}">Logout</a>
        {% else %}
            <a href="{{ url_for('login') }}">Admin Login</a>
        {% endif %}
    </div>

    {% if logged_in %}
    <h2>Publish New Post</h2>

    <form method="POST" action="{{ url_for('add_post') }}">
        <input type="text" name="title" placeholder="Post Title" required>

        <textarea name="content" rows="5"
                  placeholder="Write your gossip..." required></textarea>

        <input type="text"
               name="image"
               placeholder="Image URL (optional)">

        <button type="submit">Publish Post</button>
    </form>

    <hr>
    {% endif %}

    <h2>The Feed</h2>

    {% for post in posts %}
        <div class="post">
            <h3>{{ post.title }}</h3>
            <p>{{ post.content }}</p>

            {% if post.image %}
                <img src="{{ post.image }}" alt="Post Image">
            {% endif %}
        </div>
    {% endfor %}

</div>
</body>
</html>
"""

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            background: #fff0f5;
            font-family: Arial, sans-serif;
            padding: 30px;
        }
        .box {
            max-width: 400px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
        }
        input {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        button {
            width: 100%;
            padding: 10px;
            background: #d11141;
            color: white;
            border: none;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>

<div class="box">
    <h2>Admin Login</h2>

    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}

    <form method="POST">
        <input type="text"
               name="username"
               placeholder="Username"
               required>

        <input type="password"
               name="password"
               placeholder="Password"
               required>

        <button type="submit">Login</button>
    </form>

    <p>
        <a href="{{ url_for('home') }}">Back to Feed</a>
    </p>
</div>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(
        HTML_TEMPLATE,
        posts=blog_posts,
        logged_in=session.get('logged_in', False)
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password."

    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
def add_post():
    if not session.get('logged_in'):
        return "Unauthorized Access", 401

    title = request.form.get('title')
    content = request.form.get('content')
    image = request.form.get('image', '').strip()

    if title and content:
        blog_posts.insert(0, {
            "title": title,
            "content": content,
            "image": image if image else None
        })

    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
