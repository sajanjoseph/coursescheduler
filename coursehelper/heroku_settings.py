
DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
#login url added by sajan
LOGIN_URL='/account/login/'
LOGIN_REDIRECT_URL='/'

SITE_ID = 3

import os.path
parentpath=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
currentpath = os.path.dirname(os.path.abspath(__file__))

MEDIA_ROOT = os.path.join(parentpath,'coursescheduler/media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'


TEMPLATE_DIRS = (

os.path.join(parentpath,'coursescheduler/templates'),

)

REGISTRATION_OPEN = False
import dj_database_url
DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}
