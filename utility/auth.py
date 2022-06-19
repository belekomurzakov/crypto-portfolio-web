import hashlib


def password_hash(password):
    # Make a hash of the user's password to prevent storing plain text password in the database.
    # Hash is a one-way process. A hacker cannot get the original password from the hash.

    salt = "aaabbbcccaaabbbcccaaabbbccctreqw".encode('utf-8')  # A random string

    password_hash = hashlib.pbkdf2_hmac(
        'sha256',  # An up-to-date hash digest algorithm for HMAC (old ones are already hacked)
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000  # It is recommended to use at least 100,000 iterations of SHA-256
    ).hex()

    return password_hash
