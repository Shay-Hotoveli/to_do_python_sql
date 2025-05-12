from app.services import user_service
import uuid

def test_create_user_and_retrieve(db, clean_user_db):
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"
    password = "hashed_password"
    gender = "male"
    user_service.create_user(username, password, email, gender)
    user = user_service.get_user_by_username(username)
    assert user is not None
    assert user["user_name"] == username
    assert user["email"] == email

def test_user_exists_positive(db, clean_user_db):
    username = f"exist_{uuid.uuid4().hex[:6]}"
    email = f"{username}@test.com"
    password = "dummy"
    gender = "female"
    user_service.create_user(username, password, email, gender)
    assert user_service.user_exists(username, email) is not None

def test_check_valid_register_info_valid(db, clean_user_db):
    username = f"newuser_{uuid.uuid4().hex[:6]}"
    email = f"{username}@email.com"
    result, message = user_service.check_valid_register_info(username, email)
    assert result is True

def test_check_valid_register_info_invalid_email():
    result, message = user_service.check_valid_register_info("testuser", "invalid-email")
    assert result is False or "Invalid email" in message
