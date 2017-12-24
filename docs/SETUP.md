Setup on local development environment

Assuming development is done on a Ubuntu 16.04 or better

Need to install the following libraries

* python-django
* python-pymysql (for ImportError: No module named pymysql)

Copy the settings module from an existing copy


    TEMPLATE_DEBUG = True

    EMAIL_HOST = 'box1.vees.net'
    EMAIL_PORT = 587

    ALLOWED_HOSTS = ['vees.net']

    ADMINS = (
         ('Rob Carlson', 'rob@vees.net'),
    )
