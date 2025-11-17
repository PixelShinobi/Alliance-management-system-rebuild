from app import ma
from app.models import User, Member, TokenBlocklist
from marshmallow import fields, validates, validates_schema, ValidationError
from flask import url_for
import re

# Member Schema with hyperlinked field and nested creator
class MemberSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Member model with hyperlink and nested creator"""
    class Meta:
        model = Member
        load_instance = True
        include_fk = True

    # Hyperlinked field - generates URL to member detail
    url = fields.Method("get_url")

    # Nested field using backref - shows creator/user info for this member
    creator = fields.Nested(lambda: UserSchema(only=('id', 'username', 'role')))

    def get_url(self, obj):
        """Generate hyperlinked URL for member"""
        return url_for('get_member', member_id=obj.id, _external=True)

    # Custom validation using @validates decorator
    @validates('email')
    def validate_email(self, value):
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise ValidationError('Invalid email format')

    @validates('phone')
    def validate_phone(self, value):
        """Validate phone number format"""
        if value and len(value) > 15:
            raise ValidationError('Phone number too long (max 15 characters)')


# User Schema (simplified - for nested use in MemberSchema)
class UserSchema(ma.SQLAlchemyAutoSchema):
    """Schema for User model (used as nested field in MemberSchema)"""
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)  # Never expose password hash


# Registration Schema with @validates_schema
class RegisterSchema(ma.Schema):
    """Schema for user registration with password validation"""
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    confirm_password = fields.Str(required=True, load_only=True)
    role = fields.Str(load_default='user')  # Default to 'user'

    @validates('username')
    def validate_username(self, value):
        """Validate username"""
        if len(value) < 3:
            raise ValidationError('Username must be at least 3 characters')
        if not value.isalnum():
            raise ValidationError('Username must be alphanumeric')

    @validates('password')
    def validate_password(self, value):
        """Validate password strength"""
        if len(value) < 6:
            raise ValidationError('Password must be at least 6 characters')

    @validates('role')
    def validate_role(self, value):
        """Validate role is either 'user' or 'admin'"""
        if value not in ['user', 'admin']:
            raise ValidationError('Role must be either "user" or "admin"')

    @validates_schema
    def validate_passwords_match(self, data, **kwargs):
        """Validate that password and confirm_password match"""
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError('Passwords do not match', field_name='confirm_password')


# Login Schema
class LoginSchema(ma.Schema):
    """Schema for user login"""
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

    @validates('username')
    def validate_username(self, value):
        """Validate username not empty"""
        if not value.strip():
            raise ValidationError('Username is required')

    @validates('password')
    def validate_password(self, value):
        """Validate password not empty"""
        if not value:
            raise ValidationError('Password is required')


# Initialize schemas
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
register_schema = RegisterSchema()
login_schema = LoginSchema()
