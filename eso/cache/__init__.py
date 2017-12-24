from PIL import Image
from exo.models import PictureSimple

def main():
    unchecked=PictureSimple.objects.filter(private=None).order_by('directory','filename')
    for p in unchecked:
        print(p.b32md5)
        image_cache(p.get_local_path(), p.b32md5)

def image_cache(path_to_original, output_filename):
    im = Image.open(path_to_original)
    size = 500,375,180
    im.thumbnail(size, Image.ANTIALIAS)
    im.save('/media/dev/cache/'+output_filename+'.jpg', format= 'JPEG')

main()

