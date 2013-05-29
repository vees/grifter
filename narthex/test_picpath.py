from regatta.models import Old_Picture
p=Old_Picture.objects.get(pk=1042)
print "/local/img/"+p.theme.directory+"/"+p.filename+".jpg"

