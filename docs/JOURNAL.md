Fri Aug  9 13:41:32 PDT 2013

Problem:

On my local machine I have 45000 pictures, some of which I would not 
to upload to any machine acting as a server.

Objective:

1. Get a list of every image file stored on my private computer.
2. Find and record the MD5 hash to remove any duplicates

Sat Aug 10 22:45:33 EDT 2013

Next objective:

Finish editing views.py to link to PictureSimple and base32 to 
render a random small image to the test server for proof of concept.

Tue Aug 13 10:33:50 EDT 2013

Odd cases:

ahnrb81b9qmertxyjym31pa7nm  appears to be rotated already
http://10.160.40.158:8000/file/7xkgskph1f4kvn700tm9p8kx0g same thing

Thu May 28 22:06:02 EDT 2015

runfile('/media/dev/projects/narthex/manage.py', wdir=r'/media/dev/projects/narthex', args='shell')

runfile('/Users/rob/Projects/narthex/manage.py', 
wdir=r'/Users/rob/Projects/narthex/', args='shell')

>>> runfile('/Users/rob/Projects/narthex/manage.py', 
... wdir=r'/Users/rob/Projects/narthex/', args='shell')
Python 2.7.10 |Anaconda 2.2.0 (x86_64)| (default, May 28 2015, 17:04:42) 
Type "copyright", "credits" or "license" for more information.

IPython 3.2.0 -- An enhanced Interactive Python.
Anaconda is brought to you by Continuum Analytics.
Please check out: http://continuum.io/thanks and https://anaconda.org
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: 

In [1]: from exo.models import PictureSimple

In [2]: p=PictureSimple.objects.all()

In [3]: p[1]

OperationalError: unable to open database file

Here's a great discussion on how to split up the settings file
into secret and non-secret parts for checking into source control:
https://code.djangoproject.com/wiki/SplitSettings


Setting up the database
===

https://docs.djangoproject.com/en/1.8/topics/migrations/

love:narthex rob$ python manage.py sqlall exo
CommandError: App 'exo' has migrations. Only the sqlmigrate and sqlflush commands can be used when an app has migrations.

love:narthex rob$ python manage.py makemigrations
love:narthex rob$ python manage.py makemigrations
Migrations for 'exo':
  0004_auto_20150704_1242.py:
    - Alter field email on old_photographer
    - Alter field email on person
love:narthex rob$ python manage.py migrate
Operations to perform:
  Synchronize unmigrated apps: staticfiles, admindocs, messages
  Apply all migrations: exo, contenttypes, sites, auth, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
  Installing custom SQL...
Running migrations:
  Rendering model states... DONE
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying exo.0001_initial... OK
  Applying exo.0002_masterfile_old_picture... OK
  Applying exo.0003_auto_20150528_2058... OK
  Applying exo.0004_auto_20150704_1242... OK
  Applying sessions.0001_initial... OK
  Applying sites.0001_initial... OK


Playing Around
====


Bypassing manage.py

If you’d rather not use manage.py, no problem. Just set the DJANGO_SETTINGS_MODULE environment variable to mysite.settings, start a plain Python shell, and set up Django:

>>> import django
>>> django.setup()
If this raises an AttributeError, you’re probably using a version of Django that doesn’t match this tutorial version. You’ll want to either switch to the older tutorial or the newer Django version.

You must run python from the same directory manage.py is in, or ensure that directory is on the Python path, so that import mysite works.


== Playing around

>>> import os
>>> os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
'exo.settings'
>>> import django
>>> django.setup()
>>> from exo.models import *
>>> ContentContainer()
<ContentContainer: ContentContainer object>
>>> c=ContentContainer()
>>> c
<ContentContainer: ContentContainer object>
>>> c.server = "love"
>>> c.drive = "love"
>>> c.path = "/Users/rob/Desktop"
>>> c.save()
>>> ContentContainer.objects.all()
[<ContentContainer: ContentContainer object>]
>>> ContentContainer.objects.all()[0]
<ContentContainer: ContentContainer object>
>>> cc=ContentContainer.objects.all()
>>> cc
[<ContentContainer: ContentContainer object>]
>>> cc[1]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/rob/anaconda/lib/python2.7/site-packages/django/db/models/query.py", line 201, in __getitem__
    return list(qs)[0]
IndexError: list index out of range
>>> cc[0]
<ContentContainer: ContentContainer object>
>>> 


== JSON stuff

serializers.serialize("json", ContentContainer.objects.all())
https://docs.djangoproject.com/en/1.8/topics/serialization/

