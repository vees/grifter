from django.db import models

ROTATION = (
    (90, '90 CW'),
    (270, '90 CCW'),
    (0, 'None'),
    (180, '180'),
)

RESILIENCY = (
    (1, 'Temporary'), (2, 'Sentimental'), (3, 'Destroy'), (4, 'Limited'),
)

class ContentKey(models.Model):
    def __str__(self):
        return "%s|%s" % (self.id, self.key)
    def __unicode__(self):
        return "%s|%s" % (self.id, self.key)
    key = models.CharField(max_length=4, null=False, unique=True)
    '''
    If you need to create a relationship on a model that has not yet been
defined, you can use the name of the model, rather than the model object
itself. Can also probably use a OneToOneKey instead of ForeignKey here.
    '''
    canonical = models.OneToOneField('ContentSignature', null=True,
        related_name='+', unique=True, on_delete=models.PROTECT)

class Tag2(models.Model):
    slug = models.CharField(max_length=32, null=False)
    description = models.CharField(max_length=64, null=True)

class Redirect(ContentKey):
    '''
    If you'd prefer Django didn't create a backwards relation,
set related_name to '+'. For example, this will ensure that the User model
won't get a backwards relation to this model:
    '''
    destination = models.ForeignKey(ContentKey, null=False,
        related_name='+', on_delete=models.PROTECT)

class ContentSignature(models.Model):
    def __str__(self):
        return "%s|%s|%s|%s" % (
            self.id, self.md5, self.sha2, self.content_size)
    def __unicode__(self):
        return "%s|%s|%s|%s" % (
            self.id, self.md5, self.sha2, self.content_size)
    def severity(self):
        instances=self.contentinstance_set.count()
        if instances==0:
            return "warning"
        elif instances==1:
            return "critical"
        elif instances==2:
            return "warning"
        elif instances<=3:
            return "good"
        elif instances>3:
            return "overkill"
        return "warning"
    md5 = models.CharField(max_length=32)
    sha2 = models.CharField(max_length=64)
    content_size = models.IntegerField()
    content_key = models.ForeignKey(ContentKey, null=True,
        on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag2)
    resiliency = models.IntegerField(choices=RESILIENCY, null=True)
    derived_from = models.ForeignKey('self', null=True,
        on_delete=models.PROTECT)

class ContentContainer(models.Model):
    def __str__(self):
        return "%s|%s|%s|%s" % (
            self.id, self.server, self.drive, self.path)
    def __unicode__(self):
        return u"%s|%s|%s|%s" % (
            self.id, self.server, self.drive, self.path)
    server = models.CharField(max_length=64)
    drive = models.CharField(max_length=64)
    path = models.CharField(max_length=200)
    class Meta:
        unique_together = ["server", "drive", "path"]

class ContentInstance(models.Model):
    def __str__(self):
        return "%s|%s|%s|%s" % (
            self.id, self.filename, self.relpath, self.content_signature.id)
    def __unicode__(self):
        return "%s|%s|%s|%s" % (
            self.id, self.filename, self.relpath, self.content_signature.id)
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
    content_container = models.ForeignKey(ContentContainer, null=False, on_delete=models.PROTECT)
    relpath = models.CharField(max_length=200)
    stat_hash = models.BigIntegerField(null=True)
    first_seen = models.DateTimeField(null=True)
    verified_on = models.DateTimeField(null=True)
    content_signature = models.ForeignKey(ContentSignature, null=True, on_delete=models.PROTECT)

class Picture(models.Model):
    signature = models.OneToOneField(ContentSignature, primary_key=True, on_delete=models.PROTECT)
    orientation = models.IntegerField(choices=ROTATION, null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    taken_on = models.DateTimeField(null=True)

class TransformedPicture(models.Model):
    signature = models.OneToOneField(ContentSignature, primary_key=True, on_delete=models.PROTECT)
    request_width = models.IntegerField(null=True)
    request_height = models.IntegerField(null=True)
    request_rotation = models.IntegerField(null=True)
    result_width = models.IntegerField(null=True)
    result_height = models.IntegerField(null=True)
    result_rotation = models.IntegerField(null=True)

#class PictureSimple(models.Model):
#    filename = models.CharField(max_length=200)
#    directory = models.CharField(max_length=200)
#    stamp = models.DateTimeField(null=False)
#    file_hash = models.CharField(max_length=200)
#    rotation = models.IntegerField(default=0, choices=ROTATION, null=False)
#    private = models.NullBooleanField(null=True)
