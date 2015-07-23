from django.conf.urls import patterns, include, url
from django.contrib import admin

#from django.conf.urls.defaults import *

#from django.contrib import admin
#admin.autodiscover()


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^grifter/', include('grifter.foo.urls')),

    #(r'^regatta/(?P<image_id>\d+)/$', 'grifter.regatta.views.index'),
    #(r'^regatta/image/(?P<image_id>\d+)/$', 'grifter.regatta.views.image'),
    #(r'^regatta/thumb/(?P<image_id>\d+)/$', 'grifter.regatta.views.thumbnail'),
    #(r'^regatta/(?P<image_id>\d+)/$', 'grifter.regatta.simple.index'),
    #(r'^regatta/image/(?P<image_id>\d+)/$', 'grifter.regatta.simple.image'),
    #(r'^regatta/thumb/(?P<image_id>\d+)/$', 'grifter.regatta.simple.thumbnail'),
    #(r'^regatta/contact/(?P<image_id>\d+)/$', 'grifter.regatta.simple.hundred'),
    #(r'^regatta/random/$', 'grifter.regatta.views.random'),
    #(r'^regatta/randomold/$', 'grifter.regatta.views.randomold'),
    #(r'^regatta/migration/(?P<image_id>\d+)$', 'grifter.regatta.migration.index'),
    #(r'^regatta/migration/oldthumb/(?P<image_id>\d+)$', 'grifter.regatta.migration.thumbnail_old'),
    #(r'^regatta/migration/newthumb/(?P<image_id>\d+)$', 'grifter.regatta.migration.thumbnail_new'),
    #(r'^regatta/migration/connect/(?P<original>\d+)/(?P<new>\d+)/$', 'grifter.regatta.migration.connect'),
    (r'^$', 'exo.views.random'),
    (r'^api/new/id$', 'exo.views.new_id'),
    (r'^api/id/space$', 'exo.views.remaining_id_space'),
    (r'^api/export$', 'exo.views.export'),
    (r'^api/tags/dumpall$', 'exo.views.api_tagdump'),
    (r'^api/tags/load$', 'exo.views.api_tagload'),
    (r'^api/rotation/dumpall$', 'exo.views.api_rotatedump'),
    (r'^api/rotation/load$', 'exo.views.api_rotateload'),
    (r'^api/photo/(?P<contentkey>[0123456789abcdefghjkmnpqrstvwxyz]{4})/(?P<action>\w+)/(?P<attribute>[0-9]+)/', 'exo.views.api_action'),
    (r'^api/photo/(?P<contentkey>[0123456789abcdefghjkmnpqrstvwxyz]{4})/(?P<action>\w+)/(?P<attribute>[\w,]+)/', 'exo.views.api_action'),
    (r'^api/photo/(?P<contentkey>[0123456789abcdefghjkmnpqrstvwxyz]{4})/(?P<action>\w+)/', 'exo.views.api_action'),
    #(r'^$', 'exo.views.privacy_unchecked'),
    (r'^random/$', 'exo.views.random'),
    (r'^(?P<contentkey>[0123456789abcdefghjkmnpqrstvwxyz]{4})/$', 'exo.views.page_by_contentkey'),  # 
    (r'^file/(?P<contentkey>[0123456789abcdefghjkmnpqrstvwxyz]{4})/$', 'exo.views.image_by_contentkey'),  # 
    (r'^meta/(?P<base32md5>[0123456789abcdefghjkmnpqrstvwxyz]{7,32})$', 'exo.views.page_by_base32'),
    (r'^file/(?P<base32md5>[0123456789abcdefghjkmnpqrstvwxyz]{7,32})$', 'exo.views.image_by_base32'),
#    (r'^action/(?P<actiontext>\w+)/(?P<md5list>[[0123456789abcdefghjkmnpqrstvwxyz,]+)$', 'exo.views.update_privacy'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
