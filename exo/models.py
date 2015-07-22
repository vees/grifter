from django.db import models

#from django.conf import settings
#from django.core.urlresolvers import reverse
#
#from eso.base32 import base32
#
#import binascii

ROTATION = (
    (90, '90 CW'),
    (270, '90 CCW'),
    (0, 'None'),
    (180, '180'),
)

class ContentKey(models.Model):
    def __unicode__(self):
        return "%s|%s" % (self.id, self.key)
    key = models.CharField(max_length=4, null=False, unique=True)

class Tag(models.Model):
    slug = models.CharField(max_length=32, null=False)
    description = models.CharField(max_length=64, null=True)

class Redirect(ContentKey):
    '''
    If you'd prefer Django didn't create a backwards relation, 
set related_name to '+'. For example, this will ensure that the User model 
won't get a backwards relation to this model:
    '''
    destination = models.ForeignKey(ContentKey, null=False, related_name='+')

class ContentSignature(models.Model):
    def __unicode__(self):
        return "%s|%s|%s|%s" % (self.id, self.md5, self.sha2, self.content_size)    
    md5 = models.CharField(max_length=32)
    sha2 = models.CharField(max_length=64)
    content_size = models.IntegerField()
    content_key = models.ForeignKey(ContentKey, null=True)

class ContentContainer(models.Model):
    def __unicode__(self):
        return "%s|%s|%s|%s" % (self.id, self.server, self.drive, self.path)
    server = models.CharField(max_length=64)
    drive = models.CharField(max_length=64)
    path = models.CharField(max_length=200)
    class Meta:
        unique_together = ["server", "drive", "path"]
    
class ContentInstance(models.Model):
    def __unicode__(self):
        return "%s|%s|%s|%s" % (self.id, self.filename, self.relpath, self.content_signature.id)    
#    def __str__(self):
#        return self.get_local_path()
#    def get_absolute_url(self):
#        return reverse('exo.views.page_by_base32', args=[str(self.b32md5)])
#    def get_local_path(self):
#        return "%s/%s/%s" % (
#            settings.NARTHEX_PHOTO_PATH, self.directory, self.filename)
#    @property
#    def b32md5(self):
#        return base32.b32encode(binascii.unhexlify(self.file_hash))
    filename = models.CharField(max_length=200)
    content_container = models.ForeignKey(ContentContainer, null=False)
    relpath = models.CharField(max_length=200)
    stat_hash = models.BigIntegerField(null=True)
    first_seen = models.DateTimeField(null=True)
    verified_on = models.DateTimeField(null=True)
    content_signature = models.ForeignKey(ContentSignature, null=True)

class Picture(models.Model):
    '''
    Need to add NSFW tag
    '''
    signature = models.OneToOneField(ContentSignature, primary_key=True)
    rotation = models.IntegerField(choices=ROTATION, null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    taken_on = models.DateTimeField(null=True)

class PictureSimple(models.Model):
    filename = models.CharField(max_length=200)
    directory = models.CharField(max_length=200)
    stamp = models.DateTimeField(null=False)
    file_hash = models.CharField(max_length=200)
    rotation = models.IntegerField(default=0, choices=ROTATION, null=False)
    private = models.NullBooleanField(null=True)