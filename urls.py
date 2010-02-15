from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^grifter/', include('grifter.foo.urls')),

	 (r'^regatta/(?P<image_id>\d+)/$', 'grifter.regatta.views.index'),
	 (r'^regatta/image/(?P<image_id>\d+)/$', 'grifter.regatta.views.image'),
	 (r'^regatta/thumb/(?P<image_id>\d+)/$', 'grifter.regatta.views.thumbnail'),
	 (r'^regatta/random/$', 'grifter.regatta.views.random'),
	 (r'^regatta/randomold/$', 'grifter.regatta.views.randomold'),
	 (r'^regatta/migration/(?P<image_id>\d+)$', 'grifter.regatta.migration.index'),
	 (r'^regatta/migration/oldthumb/(?P<image_id>\d+)$', 'grifter.regatta.migration.thumbnail_old'),
	 (r'^regatta/migration/newthumb/(?P<image_id>\d+)$', 'grifter.regatta.migration.thumbnail_new'),
	 (r'^regatta/migration/connect/(?P<original>\d+)/(?P<new>\d+)/$', 'grifter.regatta.migration.connect'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)
