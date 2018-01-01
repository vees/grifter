"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, re_path

from . import views

urlpatterns = [
    # Example:
    re_path(r'^$', views.random, name="main_page"),
    re_path(r'^api/new/id$', views.new_id),
    re_path(r'^api/id/space$', views.remaining_id_space),
    re_path(r'^api/export$', views.export),
    re_path(r'^api/tags/dumpall$', views.api_tagdump),
    re_path(r'^api/tags/load$', views.api_tagload),
    re_path(r'^api/rotation/dumpall$', views.api_rotatedump),
    re_path(r'^api/rotation/load$', views.api_rotateload),
    re_path(r'^api/photo/(?P<contentkey>[0123456789abcdefghjkmnpqrstvwxyz]{4})'
        r'/(?P<action>\w+)/(?P<attribute>[0-9]+)/',
        views.api_action, name="api_numeric_action"),
    re_path(r'^api/photo/(?P<contentkey>[0123456789abcdefghjkmnpqrstvwxyz]{4})'
        r'/(?P<action>\w+)/(?P<attribute>[\w:,]+)/',
        views.api_action, name="api_alpha_action"),
    re_path(r'^api/photo/(?P<contentkey>[0123456789abcdefghjkmnpqrstvwxyz]{4})'
        r'/(?P<action>\w+)/',
        views.api_action, name="api_bare_action"),
    re_path(r'^random/$', views.random),
    re_path(r'^tags/(?P<slug>[\w:]+)',
        views.tagbyslug, name='tags_by_slug'),
    re_path(r'^tags',
        views.taglist, name="tags_list"),
    re_path(r'^(?P<contentkey>[0123456789abcdefghjkmnpqrstvwxyz]{4})/$',
        views.page_by_contentkey, name='page_by_contentkey'),
    re_path(r'^file/(?P<contentkey>[0123456789abcdefghjkmnpqrstvwxyz]{4})/$',
        views.image_by_contentkey, name='image_by_contentkey'),
    re_path(r'^meta/(?P<base32md5>[0123456789abcdefghjkmnpqrstvwxyz]{7,32})$',
        views.page_by_base32),
    re_path(r'^file/(?P<base32md5>[0123456789abcdefghjkmnpqrstvwxyz]{7,32})$',
        views.image_by_base32),

    path('admin/', admin.site.urls),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # path(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    re_path(r'^admin/redundancy/(?P<offset>\d+)', views.redundancy),
    re_path(r'^admin/redundancy/', views.redundancy),
]
