from main import hash_password, verify_password

def test_hash_password_creates_different_output():
    hashed = hash_password("mypassword123")
    assert hashed != "mypassword123"

def test_verify_correct_password():
    hashed = hash_password("mypassword123")
    assert verify_password("mypassword123", hashed) == True

def test_verify_wrong_password():
    hashed = hash_password("mypassword123")
    assert verify_password("wrongpassword", hashed) == False