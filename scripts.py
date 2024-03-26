# from passlib.hash import bcrypt

# hash = bcrypt.hash("password")
# print(f"hashed: {hash}")
# print(f"verified: {bcrypt.verify('password', hash)}")


from email_validator import validate_email, EmailNotValidError

email = "prajin@gmail"

try:
    validate_email(email)
except EmailNotValidError as e:
    print(e)
