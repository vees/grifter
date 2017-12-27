# Custom Python 3.6.3

To install on Dreamhost, start with their
[instructions for custom version of Python 3](https://help.dreamhost.com/hc/en-us/articles/115000702772-Installing-a-custom-ve
rsion-of-Python-3) help page.

The instructions distill down to this:

    mkdir tmp
    cd tmp
    wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
    tar zxvf Python-3.6.3.tgz
    cd Python-3.6.3
    ./configure --prefix=$HOME/opt/python-3.6.3

At the end of the configuration process, the script will suggest using
 `--enable-optimizations` but doing this will cause the `make` installer to use
too much CPU and get killed by the shared host monitor, so just leave it off.

Once everything works,

    make
    make clean
    make install

At this point a copy of Python 3.6.3 is present in `$HOME/opt/python-3.6.3`
which can be verified like this:

    $ ~/opt/python-3.6.3/bin/python3 --version
    Python 3.6.3

Add the following statement to `$HOME/.bash_profile` to lock in this version
as the primary one for your SSH sessions.

    export PATH=$HOME/opt/python-3.6.3/bin:$PATH

# App-specific environment

A Python 3 virtual environment can be set up anywhere in relation to the
Python code files that will be using it.
Since Dreamhost user accounts can contain directories linking to multiple
hosted site domains, it makes the most sense to make a virtual environment in
the Django project directory.

A good starting point for a new Passenger-capable web directory on Dreamhost
will look like this:

    $ ls -1p
    passenger_wsgi.py
    public/
    tmp/

If the `tmp` dir doesn't exist, create it. It's a good place to add or touch
the `restart.txt` file to force Django to reload and preferable to using
`pkill python` which also resets other Passenger based web sites and other
Python processes running under the same user.

Since Passenger configured web sites will not present any files except those
under the `public` directory it's safe to add a virtual environment here.

    $ python3 -m venv env

This environment can be activated (and must be reactivated each time) by
calling:

    $ source env/bin/activate

# Pull in this code

    $ ln -s ~/projects/narthex/ narthex
    $ cd narthex

    (env) [richard-bassett]$ pip3 install -r requirements.txt
    Collecting Django==2.0 (from -r requirements.txt (line 1))
      Using cached Django-2.0-py3-none-any.whl
    Collecting olefile==0.44 (from -r requirements.txt (line 2))
      Using cached olefile-0.44.zip
    Collecting Pillow==4.3.0 (from -r requirements.txt (line 3))
      Using cached Pillow-4.3.0-cp36-cp36m-manylinux1_x86_64.whl
    Collecting pytz==2017.3 (from -r requirements.txt (line 4))
      Using cached pytz-2017.3-py2.py3-none-any.whl
    Installing collected packages: pytz, Django, olefile, Pillow
      Running setup.py install for olefile ... done
    Successfully installed Django-2.0 Pillow-4.3.0 olefile-0.44 pytz-2017.3

# passenger-wsgi.py

    #!/usr/bin/python
    from __future__ import print_function
    import sys, os
    cwd = os.getcwd()
    sys.path.append(cwd)
    sys.path.append(os.getcwd()+"/foo")


    #INTERP = "/home/robvees/opt/python-3.6.3/bin/python3.6"
    INTERP = "/home/robvees/newproject/test/bin/python3"

    #sys.stdout=open("/home/robvees/log.txt","a")
    #print("hello")

    #if sys.hexversion < 0x2060000: os.execl(INTERP, "python3.6", *sys.argv)

    if sys.executable != INTERP:
    	os.execl(INTERP, INTERP, *sys.argv)
    else:
    	#raise Exception(sys.path)
       pass

    #def application(environ, start_response):
    #    start_response('200 OK', [('Content-type', 'text/plain')])
    #    return ["Hello, world!", sys.executable, sys.argv]

    def application(environ, start_response):
        status = '200 OK'
        output = 'Hello World! Running Python version ' + sys.version + '\n\n'
        response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
        #raise("error")
        start_response(status, response_headers)
        return [output]

    #raise Exception(sys.executable)
    #raise Exception(sys.path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foo.settings")

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    #import django.core.handlers.wsgi
    #application = django.core.handlers.wsgi.WSGIHandler()

    #raise Exception(sys.path)
