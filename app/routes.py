from flask import render_template, request, redirect, url_for, flash, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, APP_NAME, bcrypt
from app.models import Member, User
from app.schemas import member_schema, members_schema
from app.forms import MemberForm, ExtendedMemberForm, LoginForm
from marshmallow import ValidationError

# Available roles for form dropdown
ROLES = [
    {'id': 1, 'name': 'Leader'},
    {'id': 2, 'name': 'Officer'},
    {'id': 3, 'name': 'Member'},
    {'id': 4, 'name': 'Recruit'},
]


# ============================================
# HTML ROUTES (Web Interface)
# ============================================

@app.route('/')
def home():
    """Homepage"""
    return render_template('index.html', title='Home', app_name=APP_NAME)


@app.route('/login', methods=['GET', 'POST'])
def web_login():
    """Web interface login"""
    if current_user.is_authenticated:
        return redirect(url_for('members'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')

            # Redirect to next page or members page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('members'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', title='Login', form=form, app_name=APP_NAME)


@app.route('/logout')
@login_required
def web_logout():
    """Web interface logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))


@app.route('/members')
@login_required
def members():
    """Display all members from database"""
    all_members = Member.query.all()
    return render_template('members.html', title='Members', members=all_members, app_name=APP_NAME)


@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    """Add new member via form (saves to database) - Admin only"""
    # Check if user is admin
    if current_user.role != 'admin':
        flash('Admin access required to add members', 'danger')
        return redirect(url_for('members'))

    form = MemberForm()
    form.role.choices = [(r['id'], r['name']) for r in ROLES]

    if form.validate_on_submit():
        role_name = next((r['name'] for r in ROLES if r['id'] == int(form.role.data)), 'Member')

        # Create new member in database
        new_member = Member(
            name=form.name.data,
            email=form.email.data,
            role=role_name,
            user_id=current_user.id
        )

        db.session.add(new_member)
        db.session.commit()

        flash(f'Successfully added member: {form.name.data}', 'success')
        return redirect(url_for('members'))

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')

    return render_template('submit.html', title='Submit', form=form, app_name=APP_NAME)


@app.route('/submit-extended', methods=['GET', 'POST'])
@login_required
def submit_extended():
    """Extended form with phone field - Admin only"""
    # Check if user is admin
    if current_user.role != 'admin':
        flash('Admin access required to add members', 'danger')
        return redirect(url_for('members'))

    form = ExtendedMemberForm()
    form.role.choices = [(r['id'], r['name']) for r in ROLES]
    del form.email  # Demonstrate field removal

    if form.validate_on_submit():
        role_name = next((r['name'] for r in ROLES if r['id'] == int(form.role.data)), 'Member')

        new_member = Member(
            name=form.name.data,
            email='no-email@example.com',
            role=role_name,
            phone=form.phone.data or 'N/A',
            user_id=current_user.id
        )

        db.session.add(new_member)
        db.session.commit()

        flash(f'Added member: {form.name.data}', 'success')
        return redirect(url_for('members'))

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')

    return render_template('submit_extended.html', title='Extended Form', form=form, app_name=APP_NAME)


# ============================================
# API ROUTES 
# ============================================

@app.route('/api/members/<int:member_id>', methods=['GET'])
@jwt_required()
def get_member(member_id):
    """Get single member by ID (for hyperlink in schema)"""
    member = Member.query.get_or_404(member_id)
    return member_schema.jsonify(member), 200



class MembersAPI(MethodView):
    """
    API endpoints for members with JWT protection and role-based access
    - GET: Both 'user' and 'admin' can view members
    - POST/PUT/DELETE: Only 'admin' can modify members
    """
    decorators = [jwt_required()]  # Require JWT for all methods

    def get(self):
        """Get all members - accessible by both user and admin"""
        all_members = Member.query.all()
        return jsonify({
            'success': True,
            'count': len(all_members),
            'members': members_schema.dump(all_members)  # Use Marshmallow schema
        }), 200

    def post(self):
        """Add new member - admin only"""
        # Check if user is admin
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403

        try:
            # Validate with Marshmallow schema
            data = member_schema.load(request.get_json())
        except ValidationError as err:
            return jsonify({'error': err.messages}), 400

        # Get current user ID from JWT
        current_user_id = get_jwt_identity()

        # Create new member
        new_member = Member(
            name=data.get('name'),
            email=data.get('email'),
            role=data.get('role'),
            phone=data.get('phone'),
            user_id=current_user_id
        )

        db.session.add(new_member)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Member added successfully',
            'member': member_schema.dump(new_member)
        }), 201


@app.route('/api/members/<int:member_id>', methods=['PUT'])
@jwt_required()
def update_member(member_id):
    """Update member - admin only"""
    # Check if user is admin
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    member = Member.query.get_or_404(member_id)

    try: # Validate 
        data = member_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    # Update member fields
    if 'name' in request.get_json():
        member.name = data.get('name')
    if 'email' in request.get_json():
        member.email = data.get('email')
    if 'role' in request.get_json():
        member.role = data.get('role')
    if 'phone' in request.get_json():
        member.phone = data.get('phone')

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Member updated successfully',
        'member': member_schema.dump(member)
    }), 200


@app.route('/api/members/<int:member_id>', methods=['DELETE'])
@jwt_required()
def delete_member(member_id):
    """Delete member - admin only"""
    # Check if user is admin
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    member = Member.query.get_or_404(member_id)

    db.session.delete(member)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Member deleted successfully'
    }), 200


# Register MembersAPI
app.add_url_rule(
    '/api/members',
    view_func=MembersAPI.as_view('members_api'),
    methods=['GET', 'POST']
)

# Postman Testing 
# 1. Register: POST /auth/register with {"username":"admin","email":"admin@test.com","password":"admin123","confirm_password":"admin123","role":"admin"}
# 2. Login: POST /auth/login with {"username":"admin","password":"admin123"} - Copy access_token
# 3. Get Members: GET /api/members - Add header: Authorization: Bearer <access_token>
# 4. Add Member (admin): POST /api/members with JWT - Body: {"name":"Test","email":"test@test.com","role":"Member"}
# 5. Update Member (admin): PUT /api/members/1 with JWT
# 6. Delete Member (admin): DELETE /api/members/1 with JWT
