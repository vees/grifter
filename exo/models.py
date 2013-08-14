from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from eso.base32 import base32

import binascii

# Create your models here.

ROTATION = (
    (90, '90 CW'),
    (270, '90 CCW'),
    (0, 'None'),
    (180, '180'),
)

class Rating(models.Model):
    # Picture
    # User
    # Rating
    # Stamp
    pass

class Location(models.Model):
    # Venue
    # Geotag
    # Neighborhood
    # City
    # State
    # Country
    pass

class Venue(models.Model):
    pass

class Moment(models.Model):
    def best_guess(self):
        if (self.userdatetime):
            return self.userdatetime
        if (self.exim):
            return self.exim
        if (self.ctime):
            return self.ctime
        if (self.range_guess_start and self.range_guess_end):
            return (self.range_guess_start, self.range_guess_end)
        if (self.range_guess_start):
            return self.range_guess_start
        if (self.range_guess_end):
            return self.range_guess_end

    userdatetime = models.DateTimeField(null=True)
    atime = models.DateTimeField(null=True)
    ctime = models.DateTimeField(null=True)
    exim = models.DateTimeField(null=True)
    range_guess_start = models.DateTimeField(null=True)
    range_guess_end = models.DateTimeField(null=True)

class Album(models.Model):
    pass

class Rotation(models.Model):
    pass

class EXIF(models.Model):
    pass

# Event has location, in case where photo has event but no location, assign to event
class Event(models.Model):
    pass

class Copyright(models.Model):
    # - [ ] None (All rights reserved)
    # - [ ] Attribution-NonCommercial-ShareAlike Creative Commons 
    # - [ ] Attribution-NonCommercial Creative Commons 
    # - [ ] Attribution-NonCommercial-NoDerivs Creative Commons 
    # - [ ] Attribution Creative Commons 
    # - [ ] Attribution-ShareAlike Creative Commons 
    # - [ ] Attribution-NoDerivs Creative Commons
    description = models.CharField(max_length=200)
    url = models.URLField(max_length=200)

class GeoTag(models.Model):
    # Long
    # Lat
    # Alt
    # Diameter
    pass

class Camera(models.Model):
    """Since its always possible to derive the manufacturer
from the EXIF model string, that string is sufficient to store.
We'll still use a normalized table for it to make searches
and presentation easier"""
    #manufacturer = models.CharField(max_length=200)
    exif_string = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

class Person(models.Model):
    first = models.CharField(max_length=200)
    last = models.CharField(max_length=200)
    email = models.EmailField()

class Photographer(models.Model):
    person = models.ForeignKey(Person)

class Tag(models.Model):
    pass

class Comment(models.Model):
    pass

class Situation(models.Model):
    description = models.CharField(max_length=200)

class Picture(models.Model):
    """The old_id would point back to vees.net/g2/{old_id}.html.
The Flickr_id would point to http://flickr.com/photos/vees/4116008755/.

Rotation on import uses the EXIF rotation field to determine if an image was
taken while in portrait mode. Since older model cameras or those with the
orientation sensor disabled by settings will show as landscape mode regardless,
when the image is not explicitly set as rotated, we'll save None and treat this
value the same as no rotation in presentation. If a human being confirms that
the image is not rotated, the value of 0 will be used instead.

While it's tempting to leave the file_timestamp as a nullable value, but if we
have a file to display we should know as much as possible about it. It will be
the first possible value of taken_on, in combination with other fields.

The commented out fields of subject_can_id and subject_no_id are for a count of
people portrayed in the image.  At some point we'd like to see if we could
identify individuals in the photograph, at the very least to restrict anything
with people in it.
"""
    directory = models.CharField(max_length=200)
    file_name = models.CharField(max_length=200)
    file_hash = models.CharField(max_length=200)
    file_size = models.IntegerField(null=False)
    file_timestamp = models.DateTimeField(null=False)
    old_g2_id = models.IntegerField(null=True)
    flickr_id = models.CharField(max_length=200, null=True)
    rotation = models.IntegerField(choices=ROTATION, null=True)
    private = models.NullBooleanField(null=True)
    #taken_on = models.ForeignKey(Moment)
    #subject_can_id = models.IntegerField(null=True)
    #subject_no_id = models.IntegerField(null=True)
    #photographer = models.ForeignKey(Photographer)
    #photographer_permission = models.BooleanField()

class ServerInstance(models.Model):
    """The challenge with this table becomes the sharing of data between instances of
this program on various servers. The file_hash will be the primary detection of
duplicates. Each server should know its own instance name and directory tree.
These values are stored in NARTHEX_INSTANCE AND NARTHEX_PHOTO_PATH.

In the long run this may wind up being a mistake since the current instance
will need to be calculated on every page load and used as a filter in every
query, which will add to the complexity. It's possible that we can use a global
settings object to perform this query on startup and hold the variable somehow.
"""
    name = models.CharField(max_length=200)
    #photopath = models.CharField(max_length=200)
    pass

class Subject(models.Model):
    person = models.ForeignKey(Person)
    picture = models.ForeignKey(Picture)
    model_permission = models.BooleanField()

class Old_Camera(models.Model):
    #old_id = models.IntegerField(null=False)
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

class Old_Location(models.Model):
    #old_id = models.IntegerField(null=False)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2)

class Old_Photographer(models.Model):
    #old_id = models.IntegerField(null=False)
    first = models.CharField(max_length=200)
    last = models.CharField(max_length=200)
    email = models.EmailField()
    nick = models.CharField(max_length=200)
    url = models.URLField(verify_exists=True, max_length=200, null=True)

class Old_Theme(models.Model):
    #old_id = models.IntegerField(null=False)
    server = models.CharField(max_length=200)
    directory = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

#class Old_Picture(models.Model):
#    def __unicode__(self):
#        return "%s: %s in %s %s" % (
#            self.filename, self.title, self.theme.description, str(self.stamp) )
#    #old_id = models.IntegerField(null=False)
#    filename = models.CharField(max_length=200)
#    theme = models.ForeignKey(Old_Theme)
#    title = models.CharField(max_length=200)
#    location = models.ForeignKey(Old_Location)
#    stamp = models.DateTimeField(null=False)
#    photographer = models.ForeignKey(Old_Photographer)
#    special = models.CharField(max_length=2000)
#    description = models.CharField(max_length=2000)
#    camera = models.ForeignKey(Old_Camera)
#    counter = models.IntegerField(null=False)
#    block = models.BooleanField()

class PictureSimple(models.Model):
    def __str__(self):
        return self.get_local_path()
    def get_absolute_url(self):
        return reverse('exo.views.page_by_base32', args=[str(self.b32md5)])
    def get_local_path(self):
        return "%s/%s/%s" % (
            settings.NARTHEX_PHOTO_PATH, self.directory, self.filename)
    @property
    def b32md5(self):
        return base32.b32encode(binascii.unhexlify(self.file_hash))
    filename = models.CharField(max_length=200)
    directory = models.CharField(max_length=200)
    stamp = models.DateTimeField(null=False)
    file_hash = models.CharField(max_length=200)
    rotation = models.IntegerField(default=0, choices=ROTATION, null=False)
    private = private = models.NullBooleanField(null=True)

