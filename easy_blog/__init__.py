"""
django_easy_blog - A simple easy to use pluggable application that provides blog capabilities to your Django project.
"""
VERSION = (0, 2, 0, 'a', 0) # following PEP 386

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3] != 'f':
        version = '%s%s%s' % (version, VERSION[3], VERSION[4])
    return version
