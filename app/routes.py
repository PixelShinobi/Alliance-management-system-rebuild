
from flask import render_template, request
from app import app, APP_NAME

# Default values for routes (Flask style)
USER_DEFAULTS = {'name': 'User'}
SEARCH_DEFAULTS = {'query': '', 'page': 1}


# Route 1: Homepage with HTML return
@app.route('/')
def home():
    """Homepage route returning HTML template"""
    return render_template('index.html',
                         title='Home',
                         app_name=APP_NAME)


# Route 2: About page with HTML return
@app.route('/about')
def about():
    """About page route returning HTML template"""
    return render_template('about.html',
                         title='About',
                         app_name=APP_NAME)


# Route 3: Path variable 
@app.route('/user', defaults=USER_DEFAULTS)
@app.route('/user/<string:name>')
def user(name):
    """User route with path variable and default value"""
    return render_template('user.html',
                         title='User',
                         name=name,
                         app_name=APP_NAME)


# Route 4: Request arguments (query parameters) 
@app.route('/search', defaults=SEARCH_DEFAULTS)
def search(query, page):
    """Search route with request arguments and defaults"""
    # Get actual query params, use defaults if not provided
    query = request.args.get('query', query)
    page = int(request.args.get('page', page))

    return render_template('search.html',
                         title='Search',
                         query=query,
                         page=page,
                         app_name=APP_NAME)


# Route 5: Multiple HTTP verbs (GET and POST)
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """Route accepting multiple HTTP verbs"""
    if request.method == 'POST':
        # Handle POST request
        name = request.form.get('name', 'Unknown')
        return render_template('submit.html',
                             title='Submitted',
                             submitted=True,
                             name=name,
                             app_name=APP_NAME)
    else:
        # Handle GET request - show form
        return render_template('submit.html',
                             title='Submit',
                             submitted=False,
                             app_name=APP_NAME)
