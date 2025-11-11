from app.models.user import User

def test_password_hash_and_verify():
    password = "Secure123"
    hashed = User.hash_password(password)
    assert hashed != password
    assert User.verify_password(User(password_hash=hashed), password)

def test_user_repr_and_string_methods():
    user = User(username="tester", email="tester@example.com", password_hash="abc123")
    assert "tester" in str(user)
