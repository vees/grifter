[veesprod@skymaster]$ cd /home/veesprod/env/lib/python2.7/site-packages/PIL/
[veesprod@skymaster]$ python 
Python 2.7.4rc1 (default, Apr 24 2013, 11:17:50) 
[GCC 4.4.5] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import PIL
>>> from PIL import Image
>>> 

[veesprod@skymaster]$ cd
[veesprod@skymaster]$ python
Python 2.7.4rc1 (default, Apr 24 2013, 11:17:50) 
[GCC 4.4.5] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import PIL
>>> from PIL import Image
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/veesprod/env/lib/python2.7/site-packages/PIL/Image.py", line 29, in <module>
    from PIL import VERSION, PILLOW_VERSION, _plugins
ImportError: cannot import name VERSION
>>> 

[veesprod@skymaster]$ rm -rf PIL
[veesprod@skymaster]$ rm -rf Pillow-2.7.0-py2.7.egg-info/
[veesprod@skymaster]$ pwd
/home/veesprod/env/lib/python2.7/site-packages
[veesprod@skymaster]$ ls
Django-1.7.3-py2.7.egg-info	   _mysql.so		  django	     python_dateutil-2.1-py2.7.egg  six-1.3.0-py2.7.egg
MySQL_python-1.2.5-py2.7.egg-info  _mysql_exceptions.py   easy-install.pth   setuptools-0.6c11-py2.7.egg
MySQLdb				   _mysql_exceptions.pyc  pip-1.3-py2.7.egg  setuptools.pth
[veesprod@skymaster]$ easy_install pillow
Searching for pillow
Reading http://pypi.python.org/simple/pillow/
Best match: Pillow 2.7.0
Downloading https://pypi.python.org/packages/source/P/Pillow/Pillow-2.7.0.zip#md5=da10ee9d0c0712c942224300c2931a1a
Processing Pillow-2.7.0.zip
Running Pillow-2.7.0/setup.py -q bdist_egg --dist-dir /tmp/easy_install-tvNXCA/Pillow-2.7.0/egg-dist-tmp-KIGEBw
Building using 4 processes
Building using 4 processes
Building using 4 processes
Building using 4 processes
--------------------------------------------------------------------
PIL SETUP SUMMARY
--------------------------------------------------------------------
version      Pillow 2.7.0
platform     linux2 2.7.4rc1 (default, Apr 24 2013, 11:17:50)
             [GCC 4.4.5]
--------------------------------------------------------------------
*** TKINTER support not available
--- JPEG support available
*** OPENJPEG (JPEG2000) support not available
--- ZLIB (PNG/ZIP) support available
--- LIBTIFF support available
--- FREETYPE2 support available
*** LITTLECMS2 support not available
*** WEBP support not available
*** WEBPMUX support not available
--------------------------------------------------------------------
To add a missing option, make sure you have the required
library, and set the corresponding ROOT variable in the
setup.py script.

To check the build, run the selftest.py script.

Exception in thread Thread-1 (most likely raised during interpreter shutdown):
 Traceback (most recent call last):Exception in thread Thread-2 (most likely raised during interpreter shutdown):

Traceback (most recent call last):  File "/home/veesprod/lib/python2.7/threading.py", line 810, in __bootstrap_inner
  File "/home/veesprod/lib/python2.7/threading.py", line 810, in __bootstrap_inner

  File "/home/veesprod/lib/python2.7/threading.py", line 763, in run  File "/home/veesprod/lib/python2.7/threading.py", line 763, in run

  File "/home/veesprod/lib/python2.7/multiprocessing/pool.py", line 330, in _handle_workers
<type 'exceptions.TypeError'>: 'NoneType' object is not callable
  File "/home/veesprod/lib/python2.7/multiprocessing/pool.py", line 357, in _handle_tasks
Adding Pillow 2.7.0 to easy-install.pth file
<type 'exceptions.TypeError'>: 'NoneType' object is not callable
Installing pildriver.py script to /home/veesprod/env/bin
Installing pilconvert.py script to /home/veesprod/env/bin
Installing pilfont.py script to /home/veesprod/env/bin
Installing pilfile.py script to /home/veesprod/env/bin
Installing pilprint.py script to /home/veesprod/env/bin

Installed /home/veesprod/env/lib/python2.7/site-packages/Pillow-2.7.0-py2.7-linux-x86_64.egg
Processing dependencies for pillow
Finished processing dependencies for pillow
[veesprod@skymaster]$ 

ANSWER HERE
http://stackoverflow.com/a/26370486/682915

