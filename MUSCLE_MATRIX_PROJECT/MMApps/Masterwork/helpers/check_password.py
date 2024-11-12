import re
 
def is_valid_password(password):

    if len(password) < 8:
        return False,"Password must be at least 8 characters long."
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit."
    
    # Check for at least one special character from "#@._"
    if not re.search(r'[#@._]', password):
        return False, "Password must contain at least one special character from '#@._'."
    
    return True, ""