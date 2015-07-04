Narthex Project

Yet another content management system.

This one is going to be located at vees.net so we're designing around 
urls that fit a short URL format and are "cool urls" that don't change 
over time.

References;

docs/motivation.md
docs/urls.md

[exo]
    excludelist
    finddump
    loadphotos
    mainmenu

[veesprod@skymaster]$ python manage.py sqlmigrate exo 0003
BEGIN;
ALTER TABLE `exo_picturesimple` ADD COLUMN `key` varchar(4) NULL;
ALTER TABLE `exo_picturesimple` ALTER COLUMN `key` DROP DEFAULT;

COMMIT;

