# Postman Testing Guide

Server: `http://localhost:5000`

---

## 1. Login (Get Token)

**POST** `/auth/login`

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Copy the `access_token` from response.

---

## 2. View Members

**GET** `/api/members`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

Returns all members with nested creator info.

---

## 3. Get Single Member

**GET** `/api/members/1`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

Returns one member by ID.

---

## 4. Add Member (Admin)

**POST** `/api/members`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

**Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "Member"
}
```

---

## 5. Test Validation

**POST** `/api/members`

```json
{
  "name": "Test",
  "email": "bad-email",
  "role": "Member"
}
```

Should return validation error.

---

## 6. Logout

**POST** `/auth/logout`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

Token gets blocklisted.

---

## 7. Test User Role

Login as user:
```json
{
  "username": "user",
  "password": "user123"
}
```

Try POST `/api/members` → Should get "Admin access required"

---

## 8. Register (Optional)

**POST** `/auth/register`

```json
{
  "username": "test",
  "email": "test@test.com",
  "password": "pass123",
  "confirm_password": "pass123"
}
```

---

## Features Tested

- JWT authentication (2hr expiry)
- Token blocklist
- Role-based access (admin vs user)
- Nested creator field (backref)
- Hyperlinked url field
- Marshmallow validation (@validates, @validates_schema)
- SQLAlchemy relationships
