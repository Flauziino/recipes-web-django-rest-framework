from django.utils.text import slugify
from random import SystemRandom
import string


def random_letters(k=5):
    return ''.join(SystemRandom().choices(
        string.ascii_letters + string.digits, k=k
    ))


def new_slug(text):
    return slugify(text) + '-' + random_letters(3)
