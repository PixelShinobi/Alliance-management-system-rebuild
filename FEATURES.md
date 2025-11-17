# Alliance Management System - Features

A simple Flask application for managing alliance members with authentication and role-based access control.

---

## 🔐 Authentication & Authorization

### Web Login (Session-based)
- **Login Page:** `/login`
- **Logout:** `/logout`
- **Features:**
  - Username/password authentication
  - Session management with Flask-Login
  - Role-based access (admin vs user)
  - Protected routes requiring login

### API Authentication (JWT-based)
- **Login Endpoint:** `POST /auth/register` and `POST /auth/login`
- **Features:**
  - JWT token authentication (2 hour expiry)
  - Token blocklist for logout
  - Role claims in JWT tokens
  - Protected API endpoints

**Default Accounts:**
- Admin: `admin` / `admin123`
- User: `user` / `user123`

---

## 👥 Member Management

### View Members (All Users)
- **Route:** `/members`
- **Access:** Login required
- **Features:**
  - Bootstrap table displaying all members
  - Colored role badges (Leader, Officer, Member, Recruit)
  - Empty state message if no members

### Add Members (Admin Only)
- **Route:** `/submit`
- **Access:** Admin only
- **Features:**
  - Form with validations (name, email, role)
  - CSRF protection
  - Flash messages for success/error
  - Saves to SQLite database

### Extended Form (Admin Only)
- **Route:** `/submit-extended`
- **Access:** Admin only
- **Features:**
  - Demonstrates form subclassing
  - Includes phone field
  - Email field removed (demonstrates field deletion)

---

## 🎨 Templates & UI

### Bootstrap Components
- All templates use Bootstrap 5.3
- No inline styles or plain HTML
- Components used:
  - Navbar with login/logout
  - Cards for homepage
  - Forms with validation styling
  - Tables with badges
  - Alerts for flash messages
  - List groups

### Dynamic Navigation
- Shows username when logged in
- "Add Member" link only for admins
- Login/Logout toggle based on auth status

---

## 🔧 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Get JWT token
- `POST /auth/logout` - Invalidate token

### Members (JWT Protected)
- `GET /api/members` - View all members (all users)
- `POST /api/members` - Add member (admin only)
- `PUT /api/members/<id>` - Update member (admin only)
- `DELETE /api/members/<id>` - Delete member (admin only)

---

## 📊 Database

### Models (SQLAlchemy)
1. **User** - Login credentials, roles
2. **Member** - Alliance member information
3. **TokenBlocklist** - Revoked JWT tokens

### Relationship
- User → Members (one-to-many with backref)
- Each member has a `creator` (the user who added them)

### Location
- **Database:** `instance/alliance.db` (SQLite)

---

## ✅ Marshmallow Schemas

### MemberSchema
- **Hyperlinked field:** `url` field using `fields.Method`
- **Nested field:** `creator` field showing user info (backref)
- **Validations:** `@validates` for email and phone

### RegisterSchema
- **Cross-field validation:** `@validates_schema` for password matching
- **Field validations:** Username, email, password requirements

---

## 🎯 Role-Based Access Control

### User Role (View Only)
- ✅ View members
- ❌ Add members
- ❌ Edit members
- ❌ Delete members

### Admin Role (Full Access)
- ✅ View members
- ✅ Add members
- ✅ Edit members (API only)
- ✅ Delete members (API only)

---

## 📁 Project Structure

```
Alliance-management-system-rebuild/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── routes.py            # Web & API routes
│   ├── auth.py              # Authentication routes (Blueprint)
│   ├── models.py            # Database models
│   ├── schemas.py           # Marshmallow schemas
│   ├── forms.py             # WTForms
│   └── templates/           # HTML templates (Bootstrap)
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── members.html
│       ├── submit.html
│       └── submit_extended.html
├── instance/
│   └── alliance.db          # SQLite database
├── run.py                   # Server entry point
├── requirements.txt         # Dependencies
└── .env                     # Environment variables

```

---

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run server:**
   ```bash
   python run.py
   ```

3. **Access application:**
   - Web: http://localhost:5000
   - Login with: `admin` / `admin123`

4. **Test API (Postman):**
   - See `POSTMAN_TESTING_GUIDE.md`

---

## 🔑 Key Technologies

- **Flask 3.0** - Web framework
- **Flask-Login** - Session management
- **Flask-JWT-Extended** - JWT authentication
- **Flask-SQLAlchemy** - Database ORM
- **Flask-Marshmallow** - Schema serialization
- **Flask-WTF** - Forms and validation
- **Flask-Bcrypt** - Password hashing
- **Bootstrap 5.3** - UI components
- **SQLite** - Database
