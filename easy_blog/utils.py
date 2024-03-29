# borrowed from django-sugar by Kevin Fricovsky:
# https://github.com/montylounge/django-sugar

from datetime import datetime, timedelta, tzinfo
import re

try:
    from hashlib import md5
except ImportError:
    import md5

try:
    import pytz
except ImportError:
    pytz = None

from django.db.models.manager import Manager
from django.conf import settings
from django.utils import formats
from django.utils.dateformat import format
from django.utils.encoding import smart_str
try:
    from django.utils.timezone import now
except ImportError:
    pass
from django.utils.translation import ugettext


def clean_cache_key(key):
    '''Replace spaces with '-' and hash if length is greater than 250.'''

    #logic below borrowed from http://richwklein.com/2009/08/04/improving-django-cache-part-ii/
    cache_key = re.sub(r'\s+', '-', key)
    cache_key = smart_str(cache_key)

    if len(cache_key) > 250:
        m = md5()
        m.update(cache_key)
        cache_key = cache_key[:200] + '-' + m.hexdigest()

    return cache_key

def create_cache_key(klass, field=None, field_value=None):
    '''
    Helper to generate standard cache keys.

    Concepts borrowed from mmalone's django-caching:
    http://github.com/mmalone/django-caching/blob/ef7dd47e9beff39496e6a28ae129bae1b5f9ed71/app/managers.py

    Required Arguments
    ------------------
        'klass'
            Model or Manager

        'field'
            string, the specific Model field name used to create a more
            specific cache key. If you specify a field, it is used for the
            lookup to grab the value.

         'field_value'
            value, unique value used to generate a distinct key. Often
            this will be the ID, slug, name, etc.

            *Note: could be optimized/restricted to pk lookup only

    Returns
    -------
        'key'
            The key name.

    Example
    --------
        >> from blog.models import Post
        >> slug_val = 'test-foo'
        >> mykey = create_cache_key(Post, 'slug', slug_val)
        >> obj = cache.get(mykey)
    '''

    key_model = "%s.%s.%s:%s"
    key = ''

    if field and field_value:
        if isinstance(klass, Manager):
            key = key_model % (klass.model._meta.app_label, klass.model._meta.module_name, field, field_value)
        else:
            key = key_model % (klass._meta.app_label, klass._meta.module_name, field, field_value)

    if not key:
        raise Exception('Cache key cannot be empty.')

    return clean_cache_key(key)


def colloquial_date(d, fmt):
    if not isinstance(d, datetime):
        d = datetime(d.year, d.month, d.day)
    delta = (now() - d)
    since = delta.days
    if since <= 0:
        # d is in the future compared to now, stop processing.
        return ugettext('Today')
    elif since <= 1:
        return ugettext('Yesterday')
    elif 2 <= since <= 6:
        return ugettext('Last %(weekday)s') % { "weekday": format(d, "l") }
    try:
        return formats.date_format(d, fmt)
    except AttributeError:
        try:
            return format(d, fmt)
        except AttributeError:
            return ''


ZERO = timedelta(0)

class UTC(tzinfo):
    """
    UTC implementation taken from Python's docs.

    Used only when pytz isn't available.
    """

    def __repr__(self):
        return "<UTC>"

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


utc = pytz.utc if pytz else UTC()


def now():
    """
    Returns an aware or naive datetime.datetime, depending on settings.USE_TZ.
    """
    if getattr(settings, "USE_TZ", False):
        # timeit shows that datetime.now(tz=utc) is 24% slower
        return datetime.utcnow().replace(tzinfo=utc)
    else:
        return datetime.now()
