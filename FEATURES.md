# Flask Features Implementation

This document explains all the Flask features implemented in this project.

---

## Phase 1: Template Loops and Conditionals

### Feature: Using `{% for %}` and `{% if %}` in templates

**Route:** `/members`

**What it demonstrates:**
- Loop through a list of members using `{% for member in members %}`
- Conditional logic using `{% if %}`, `{% elif %}`, `{% else %}`
- Nested conditionals (checking role to display different badge colors)
- Empty list handling (show message if no members exist)

**How to test:**
1. Start the Flask server: `python run.py`
2. Open browser: `http://localhost:5000/members`
3. You'll see a table displaying all members with colored badges based on their role

**Code location:**
- Route: `app/routes.py:121-128`
- Template: `app/templates/members.html`

---

## Phase 2: Forms with Validation and Flash Messages

### Feature 1: Form Class with Validations

**Route:** `/submit`

**What it demonstrates:**
- Using Flask-WTF for form handling
- Field validations (required, length, email format)
- CSRF protection (automatic with Flask-WTF)
- Flash messages for success/error feedback
- Dynamic SelectField choices set in route

**Validations:**
- Name: Required, 2-50 characters
- Email: Required, valid email format
- Role: Required, must select from dropdown

**How to test:**
1. Open browser: `http://localhost:5000/submit`
2. Try submitting empty form → See error messages
3. Try invalid email → See validation error
4. Try name with 1 character → See length validation error
5. Submit valid form → Success message and redirect to members page

**Code location:**
- Form class: `app/forms.py:11-43`
- Route: `app/routes.py:70-117`
- Template: `app/templates/submit.html`

### Feature 2: Dynamic SelectField Choices

**Location:** `app/routes.py:78`

**Code example:**
```python
form.role.choices = [(r['id'], r['name']) for r in ROLES]
```

This line demonstrates setting dropdown choices dynamically from a data source (simulating a database query).

### Feature 3: Flash Messages

**Locations:**
- Success flash: `app/routes.py:101`
- Error flash: `app/routes.py:107-111`
- Display: `app/templates/base.html:48-60`

**How it works:**
- `flash(message, category)` in route adds message to session
- Template uses `get_flashed_messages(with_categories=true)` to display
- Bootstrap alert styling based on category (success=green, danger=red)

---

## Phase 3: Form Field Controls

### Feature 1: Subclassing Forms (Adding Fields)

**Route:** `/submit-extended`

**What it demonstrates:**
- Creating ExtendedMemberForm that inherits from MemberForm
- Adding new field (phone) in subclass
- All parent fields are automatically included

**Code location:**
- Extended form class: `app/forms.py:47-56`
- Route: `app/routes.py:131-183`
- Template: `app/templates/submit_extended.html`

**How to test:**
1. Open browser: `http://localhost:5000/submit-extended`
2. Notice the phone field (not in basic form)
3. Submit form with or without phone (it's optional)

### Feature 2: Deleting Fields

**Location:** `app/routes.py:141-143` (commented out)

**Code example:**
```python
del form.email  # This removes the email field entirely
# Or: form.email = None
```

Uncomment these lines to see the email field disappear from the form.

### Feature 3: Dynamic Form (Already implemented above)

The dynamic choices for SelectField is already demonstrated in Phase 2.

---

## Phase 4: Method Views and Generic List View

### Feature 1: MethodView (Class-based views)

**Endpoint:** `/api/members`

**What it demonstrates:**
- Using MethodView class for cleaner code organization
- Different methods for different HTTP verbs (get, post)
- Returning JSON responses
- Request validation

**How to test with Postman:**

**GET Request:**
```
Method: GET
URL: http://localhost:5000/api/members
```
Response will show all members in JSON format.

**POST Request:**
```
Method: POST
URL: http://localhost:5000/api/members
Headers: Content-Type: application/json
Body (raw JSON):
{
    "name": "John Doe",
    "email": "john@example.com",
    "role": "Member"
}
```
Response will show the newly created member.

**Code location:**
- MethodView class: `app/routes.py:190-237`
- Registration: `app/routes.py:243-247`

### Feature 2: Generic ListView Base Class

**Endpoints:** `/api/roles` and `/api/members-list`

**What it demonstrates:**
- Creating a reusable base class (ListView)
- Subclasses only need to set `data_source` and `item_name`
- Code reusability and DRY principle

**How to test with Postman:**

**Get Roles:**
```
Method: GET
URL: http://localhost:5000/api/roles
```

**Get Members (alternative endpoint):**
```
Method: GET
URL: http://localhost:5000/api/members-list
```

**Code location:**
- Generic ListView: `app/routes.py:254-278`
- RolesListView: `app/routes.py:282-293`
- MembersListView: `app/routes.py:297-308`

---

## Summary of All Routes

### HTML Routes (Browser):
- `/` - Homepage
- `/about` - About page
- `/members` - Members list with for/if loops
- `/user` or `/user/<name>` - User page with path variable
- `/search` - Search with query parameters
- `/submit` - Add member with validations (GET/POST)
- `/submit-extended` - Extended form with phone field (GET/POST)

### API Routes (Postman/JSON):
- `GET /api/members` - Get all members (MethodView)
- `POST /api/members` - Add new member (MethodView)
- `GET /api/roles` - Get all roles (Generic ListView)
- `GET /api/members-list` - Get all members (Generic ListView)

---

## Testing Checklist

- [x] Template loops work (`/members`)
- [x] Template conditionals work (colored badges)
- [x] Form validations work (`/submit`)
- [x] Flash messages appear on success/error
- [x] CSRF protection enabled (forms have hidden token)
- [x] Dynamic SelectField choices work
- [x] Extended form shows phone field (`/submit-extended`)
- [x] MethodView GET returns JSON
- [x] MethodView POST creates member
- [x] Generic ListView works for roles
- [x] Generic ListView works for members-list

---

## Key Concepts Learned

1. **Jinja2 Templates**: for loops, if conditionals, template inheritance
2. **Flask-WTF Forms**: Form classes, validators, CSRF protection
3. **Form Validation**: Field validators, error handling
4. **Flash Messages**: User feedback, categories
5. **Dynamic Forms**: Runtime choice population
6. **Form Subclassing**: Extending forms, adding/removing fields
7. **MethodView**: Class-based views, organized HTTP verb handling
8. **Generic Views**: Reusable base classes, DRY principle
9. **JSON APIs**: jsonify, HTTP status codes, Postman testing

---

## Next Steps

To continue learning Flask, you could add:
- Database integration (SQLAlchemy)
- User authentication and sessions
- File uploads
- Pagination for large lists
- API authentication (JWT tokens)
- Unit tests
