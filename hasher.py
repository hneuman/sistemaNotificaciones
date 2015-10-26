import functools
import hashlib
from django.utils.encoding import smart_str

from django.utils.crypto import (pbkdf2, constant_time_compare, get_random_string)



UNUSABLE_PASSWORD = '!'  # This will never be a valid encoded hash
MAXIMUM_PASSWORD_LENGTH = 4096  # The maximum length a password can be to prevent DoS
HASHERS = None  # lazily loaded from PASSWORD_HASHERS
PREFERRED_HASHER = None  # defaults to first item in PASSWORD_HASHERS

def test_hasher():
    print "funciona"

def password_max_length(max_length):
    def inner(fn):
        @functools.wraps(fn)
        def wrapper(self, password, *args, **kwargs):
            if len(password) > max_length:
                raise ValueError("Invalid password; Must be less than or equal"
                                 " to %d bytes" % max_length)
            return fn(self, password, *args, **kwargs)
        return wrapper
    return inner

def make_password(password, salt=None, hasher='default'):
    """
    Turn a plain-text password into a hash for database storage

    Same as encode() but generates a new random salt.  If
    password is None or blank then UNUSABLE_PASSWORD will be
    returned which disallows logins.
    """
    if not password:
        return UNUSABLE_PASSWORD

    #~ hasher = get_hasher(hasher)
    hasher = PBKDF2PasswordHasher()
    password = smart_str(password)
    if not salt:
        salt = hasher.salt()
    salt = smart_str(salt)
    return hasher.encode(password, salt)

class BasePasswordHasher(object):
    """
    Abstract base class for password hashers

    When creating your own hasher, you need to override algorithm,
    verify(), encode() and safe_summary().

    PasswordHasher objects are immutable.
    """
    algorithm = None
    library = None

    def _load_library(self):
        if self.library is not None:
            if isinstance(self.library, (tuple, list)):
                name, mod_path = self.library
            else:
                name = mod_path = self.library
            try:
                module = importlib.import_module(mod_path)
            except ImportError:
                raise ValueError("Couldn't load %s password algorithm "
                                 "library" % name)
            return module
        raise ValueError("Hasher '%s' doesn't specify a library attribute" %
                         self.__class__)

    def salt(self):
        """
        Generates a cryptographically secure nonce salt in ascii
        """
        return get_random_string()

    def verify(self, password, encoded):
        """
        Checks if the given password is correct
        """
        raise NotImplementedError()

    def encode(self, password, salt):
        """
        Creates an encoded database value

        The result is normally formatted as "algorithm$salt$hash" and
        must be fewer than 128 characters.
        """
        raise NotImplementedError()

    def safe_summary(self, encoded):
        """
        Returns a summary of safe values

        The result is a dictionary and will be used where the password field
        must be displayed to construct a safe representation of the password.
        """
        raise NotImplementedError()



class PBKDF2PasswordHasher(BasePasswordHasher):
    """
    Secure password hashing using the PBKDF2 algorithm (recommended)

    Configured to use PBKDF2 + HMAC + SHA256 with 10000 iterations.
    The result is a 64 byte binary string.  Iterations may be changed
    safely but you must rename the algorithm if you change SHA256.
    """
    algorithm = "pbkdf2_sha256"
    iterations = 10000
    digest = hashlib.sha256

    @password_max_length(MAXIMUM_PASSWORD_LENGTH)
    def encode(self, password, salt, iterations=None):
        assert password
        assert salt and '$' not in salt
        if not iterations:
            iterations = self.iterations
        hash = pbkdf2(password, salt, iterations, digest=self.digest)
        hash = hash.encode('base64').strip()
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)

    @password_max_length(MAXIMUM_PASSWORD_LENGTH)
    def verify(self, password, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt, int(iterations))
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        return SortedDict([
            (_('algorithm'), algorithm),
            (_('iterations'), iterations),
            (_('salt'), mask_hash(salt)),
            (_('hash'), mask_hash(hash)),
        ])
