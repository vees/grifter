from django.db import models

ROTATION = (
    (90, '90 CW'),
    (270, '90 CCW'),
    (0, 'None'),
    (180, '180'),
)

class ContentKey(models.Model):
    key = models.CharField(max_length=4, null=False)

class ContentSignature(models.Model):
    md5 = models.CharField(max_length=32)
    sha2 = models.CharField(max_length=64)
    content_size = models.IntegerField()
    content_key = models.ForeignKey(ContentKey, null=True)

class ContentContainer(models.Model):
    def __unicode__(self):
        return "%s|%s|%s|%s" % (self.id, self.server, self.drive, self.path)
    server = models.CharField(max_length=200)
    drive = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    class Meta:
        unique_together = ["server", "drive", "path"]
    
class ContentInstance(models.Model):
    filename = models.CharField(max_length=200)
    content_container = models.ForeignKey(ContentContainer, null=False)
    relpath = models.CharField(max_length=200)
    stat_hash = models.IntegerField(null=True)
    first_seen = models.DateTimeField(null=True)
    verified_on = models.DateTimeField(null=True)
    content_signature = models.ForeignKey(ContentSignature, null=True)

