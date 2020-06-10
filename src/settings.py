import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA = os.path.join(BASE_DIR, 'media')

DATABASES = os.path.join(BASE_DIR, 'databases')

GECKODRIVER = os.path.join(BASE_DIR, 'geckodriver')