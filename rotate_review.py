from regatta.models import PictureSimple

for rotation in [0,90,180,270]:
	ps=PictureSimple.objects.filter(rotation=rotation)
	print rotation, ps.count()
#	for p in ps:
#		print p.id,p.directory,p.filename

