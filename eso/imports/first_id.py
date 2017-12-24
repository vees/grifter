from regatta.models import Old_Picture
print(Old_Picture.objects.filter(id__gt=1)[0].id)


