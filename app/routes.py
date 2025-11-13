
from flask import render_template, request, redirect, url_for, flash, jsonify  # Import jsonify for JSON responses
from flask.views import MethodView  # Import MethodView for class-based views
from app import app, APP_NAME
from app.forms import MemberForm, ExtendedMemberForm  # Import form classes

# In-memory member storage (will reset when server restarts)
MEMBERS = [
    {'id': 1, 'name': 'Alice Johnson', 'email': 'alice@example.com', 'role': 'Leader'},
    {'id': 2, 'name': 'Bob Smith', 'email': 'bob@example.com', 'role': 'Member'},
    {'id': 3, 'name': 'Carol Davis', 'email': 'carol@example.com', 'role': 'Officer'},
]

# Available roles (simulating database query result)
ROLES = [
    {'id': 1, 'name': 'Leader'},
    {'id': 2, 'name': 'Officer'},
    {'id': 3, 'name': 'Member'},
    {'id': 4, 'name': 'Recruit'},
]

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


# Route 5: Multiple HTTP verbs with form validation and flash messages
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """Route accepting multiple HTTP verbs with form validation"""
    # Create form instance
    form = MemberForm()

    # Set dynamic choices for role SelectField 
    form.role.choices = [(r['id'], r['name']) for r in ROLES]  

    # Check if form was submitted and passes all validations
    if form.validate_on_submit():
        # Get the next member ID
        next_id = max([m['id'] for m in MEMBERS]) + 1 if MEMBERS else 1  

        # Get role name from role ID
        role_id = int(form.role.data)  # Get selected role ID from form
        role_name = next((r['name'] for r in ROLES if r['id'] == role_id), 'Member')  

        # Create new member dictionary
        new_member = {
            'id': next_id,
            'name': form.name.data, 
            'email': form.email.data,  
            'role': role_name  
        }

        # Add to members list
        MEMBERS.append(new_member) 

     
        flash(f'Successfully added member: {form.name.data}', 'success')

      
        return redirect(url_for('members'))  

    # If form has errors, flash them
    if form.errors:
        # Loop through all field errors
        for field, errors in form.errors.items():  
            for error in errors:  
                flash(f'{field}: {error}', 'danger')  

    # GET request or validation failed - show form
    return render_template('submit.html',
                         title='Submit',
                         form=form, 
                         app_name=APP_NAME)


# Route 6: Members list page -  for loop and if conditional in template
@app.route('/members')
def members():

    # Pass the MEMBERS list to the template
    return render_template('members.html',
                         title='Members',
                         members=MEMBERS,  
                         app_name=APP_NAME)


# Route 7: Extended form - demonstrates subclassing and field removal
@app.route('/submit-extended', methods=['GET', 'POST'])
def submit_extended():
    """Demonstrates ExtendedMemberForm and field removal"""
    form = ExtendedMemberForm()
    form.role.choices = [(r['id'], r['name']) for r in ROLES]

    # Remove email field to demonstrate field deletion
    del form.email

    if form.validate_on_submit():
        next_id = max([m['id'] for m in MEMBERS]) + 1 if MEMBERS else 1
        role_name = next((r['name'] for r in ROLES if r['id'] == int(form.role.data)), 'Member')

        MEMBERS.append({
            'id': next_id,
            'name': form.name.data,
            'email': 'no-email@example.com', 
            'role': role_name,
            'phone': form.phone.data or 'N/A'
        })

        flash(f'Added member: {form.name.data}', 'success')
        return redirect(url_for('members'))

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')

    return render_template('submit_extended.html', title='Extended Form', form=form, app_name=APP_NAME)


# ============================================
# METHOD VIEWS - Class-based views
# ============================================

class MembersAPI(MethodView):
    """
    MethodView for /api/members endpoint
    """

    def get(self):
        """Handle GET request - return all members as JSON"""
        # Return JSON response (for Postman testing)
        return jsonify({
            'success': True, 
            'count': len(MEMBERS), 
            'members': MEMBERS  
        }), 200  

    def post(self):
        """Handle POST request - add new member via JSON"""
        # Get JSON data from request body
        data = request.get_json()  

        # Validate required fields
        if not data or not data.get('name') or not data.get('email') or not data.get('role'):
            # Return error response if validation fails
            return jsonify({
                'success': False,
                'error': 'Missing required fields: name, email, role'
            }), 400  

        # Get next ID
        next_id = max([m['id'] for m in MEMBERS]) + 1 if MEMBERS else 1

        # Create new member
        new_member = {
            'id': next_id,
            'name': data['name'],
            'email': data['email'],
            'role': data['role']
        }

        # Add to list
        MEMBERS.append(new_member)

        # Return success response
        return jsonify({
            'success': True,
            'message': 'Member added successfully',
            'member': new_member
        }), 201  # HTTP status code 201 = Created


# Register the MembersAPI view with the Flask app
app.add_url_rule(
    '/api/members',  # URL route
    view_func=MembersAPI.as_view('members_api'),  # Convert class to view function
    methods=['GET', 'POST']  # Allowed HTTP methods
)

# Postman Testing:
# GET  http://localhost:5000/api/members - View all members
# POST http://localhost:5000/api/members - Add member (Body: raw JSON)
#      {"name": "David Miller", "email": "david@alliance.com", "role": "Recruit"}


