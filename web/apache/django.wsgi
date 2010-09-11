import os
import sys

sys.path.append('/home/teju/Projects/webbed-feet/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

