
import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'local-gossip-secret')

blog_posts = [
    {"title": "Welcome to Gossip Girl", "content": "Spotted: The ultimate Python story blog going live on Render. XOXO..."}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Gossip Girl Blog</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Courier New', monospace; background: #fff0f5; color: #333; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h1 { color: #d11141; text-align: center; font-size: 2.5em; text-transform: uppercase; }
        .post { background: #fafafa; padding: 15px; margin-bottom: 15px; border-left: 5px solid #d11141; border-radius: 4px; }
        .post h3 { margin-top: 0; color: #111; }
        input, textarea { width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        button { background: #d11141; color: white; border: none; padding: 10px 20px; width: 100%; border-radius: 4px; font-size: 1.1em; cursor: pointer; }
        button:hover { background: #b00e35; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Gossip Girl</h1>
        
        <form method="POST" action="/add">
            <input type="text" name="title" placeholder="Post Title (e.g., Spotted at Central Park...)" required>
            <textarea name="content" rows="4" placeholder="Type the juicy details here..." required></textarea>
            <button type="submit">Spill the Gossip</button>
        </form>

        <h2>The Feed</h2>
        <hr>
        {% for post in posts %}
        <div class="post">
            <h3>{{ post.title }}</h3>
            <p>{{ post.content }}</p>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, posts=blog_posts)

@app.route('/add', methods=['POST'])
def add_post():
    title = request.form.get('title')
    content = request.form.get('content')
    if title and content:
        blog_posts.insert(0, {"title": title, "content": content})
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
