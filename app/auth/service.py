from app.db.firebase import user_exists, create_user_in_db, get_user, get_product_id
from app.core.security import hash_password, verify_password
from app.core.exceptions import AuthError, BadRequestError
from app.auth.models import UserSignUp, UserSignIn


class AuthService:
    @staticmethod
    def signup(user_data: UserSignUp) -> dict:
        """Register a new user in the Firebase Realtime Database."""
        # Check if user already exists
        if user_exists(user_data.username):
            raise BadRequestError(f"Username {user_data.username} already exists")

        # Hash the password
        hashed_password = hash_password(user_data.password)

        # Create user node in Firebase
        user_data_dict = {
            "email": user_data.email,
            "password": hashed_password,
            "product_id": user_data.product_id
        }

        # Add to database
        create_user_in_db(user_data.username, user_data_dict)

        # Return success without sensitive information
        return {
            "message": "User created successfully",
            "username": user_data.username
        }

    @staticmethod
    def signin(user_data: UserSignIn) -> dict:
        """Authenticate a user and return a JWT token."""
        # Get user from database
        user = get_user(user_data.username)

        if not user:
            raise AuthError("Invalid username or password")

        # Verify password
        if not verify_password(user_data.password, user['password']):
            raise AuthError("Invalid username or password")

        # Generate access token
        #access_token = create_access_token({"sub": user_data.username})

        return {
            #"access_token": access_token,
            #"token_type": "bearer",
            "username": user_data.username,
            "product_id": get_product_id(user_data.username)
        }