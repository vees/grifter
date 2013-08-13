from exo.models import PictureSimple

print """*.avi
*.dat
*.pl
*.py
*.sh
*.tmp
*.WAV
*.ZIP
*.CTG
*.psd
*.tml
*.tif
*.TXT
*.MOV
*.txt
*.mov
*.PNG
*.AVI
*.THM
*.xvpics*
*.html
"""

def main():
    excluded=PictureSimple.objects.filter(private=True)
    for p in excluded:
        print p.directory+'/'+p.filename
    return True

