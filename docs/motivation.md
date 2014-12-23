#Motivation

So why create yet another content management system when so many others exist? As I explore the different requirements of this system I find myself again and again saying "Flickr has all these features" or "This is basically how Sitecore does things" or "This is the essence of Git." So why not just use a system like Sitecore or the open-source equivalent to publish my content? Why not find one of the multitude of projects on Github which meet 80% of my requirements and build from there? Why not just use the terabyte of data offered by Flickr for nothing.

The reason to avoid a system like Flickr should be obvious. Flickr has been on precarious footing on several occasions and I'm sure the future will bare out several more. I would like to be able to pick up my system from one web host or system and move it to another without having to change my URL paths and start all over again.

The reason not to reuse someone's existing code set is to better understand the motivations of the developers who design and produce content management systems. While I have acclimated myself in my daily work to doing things "The Sitecore Way" by using the provided API and design patterns to create my sites, it is like following a path that someone else has marked without really knowing why.

I'm hoping that my path through this design is less like reinventing the wheel and more like studying car designs and trying to create a vehicle that meets all of my needs without all the extra weight of a one-size-fits-all design.

To do this I will focus on the following aspects:

1. Caching
1. Permanent URL structure 
1. Simple tagging
1. Set logic
1. Access to original files
1. Responsive design
1. AJAX functionality
1. REST JSON API

## Caching

This ties into the URL structure. So we're going to start from a source file that is the original PDF, JPG, BMP, whatever.

	[veesprod@skymaster]$ pwd
	/home/veesprod/vees.net/photos/sd600-20080925
	[veesprod@skymaster]$ identify IMG_9362.JPG
	IMG_9362.JPG JPEG 2272x1704 2272x1704+0+0 8-bit DirectClass 1.002MB 0.000u 0:00.000
	[veesprod@skymaster]$ md5sum IMG_9362.JPG
	c67cbd95f6f9e09912f1b51fa2e111e8  IMG_9362.JPG
	veesprod@skymaster:~/tmp$ sha256sum IMG_9362.JPG 
	0055b0a8a697ced47f0f1b215ea800aa00ce83863bf835ac382fe735326d8438  IMG_9362.JPG

Lets assume that this is the primary representation of this image so it gets an ID of nxe7. The database row associated with this entry would look roughly like:

	ID: nxe7
	Dir: /home/veesprod/vees.net/photos/sd600-20080925
	File: IMG_9362.JPG
	MD5: c67cbd95f6f9e09912f1b51fa2e111e8
	ShortMd5: rsybv5fpz7g9j4qhpmft5r8hx0
	SHA2: 0055b0a8a697ced47f0f1b215ea800aa00ce83863bf835ac382fe735326d8438
	ShortSha2: 01av1a56jz7d8zrf3cgnxa00n80cx0w67fw3bb1r5zkkackdggw0
	IsPrimary: true
	Translation:

Since 2272 pixels wide does not work for most web applications, we're going to scale this image down to what we need. Assume that we have a 500 pixel wide layout for a set of images we're going to create a series of images that fit into it;

	https://vees.net/nxe7/rsybv5fpz7g9j4qhpmft5r8hx0/

would be the full sized image in this situation, so we'll render a few temporary images off of this one:

	https://vees.net/nxe7/rsybv5fpz7g9j4qhpmft5r8hx0/500x/

Which is roughly what happens when we run the following shell commands:

	veesprod@skymaster:~/tmp$ convert -geometry 500x IMG_9362.JPG 500x.jpg
	veesprod@skymaster:~/tmp$ ls -l 500x.jpg 
	-rw-rw-r-- 1 veesprod pg938548 54131 Dec 22 21:32 500x.jpg
	veesprod@skymaster:~/tmp$ md5sum 500x.jpg 
	6bc569718546721b1035c909ab864cbc  500x.jpg
	veesprod@skymaster:~/tmp$ sha256sum 500x.jpg 
	7727c3d56dba9d335272561c88953f857ea4afef22dd0fa3e00abbf7374fc5b7  500x.jpg

Which would result in a database row similar to:

	ID: nxe7
	Dir: /home/veesprod/vees.net/cache/
	File: df2pjwc58ss1p41ns44tq1jcqg.jpg
	MD5: 6bc569718546721b1035c909ab864cbc 
	ShortMd5: df2pjwc58ss1p41ns44tq1jcqg
	SHA2: 7727c3d56dba9d335272561c88953f857ea4afef22dd0fa3e00abbf7374fc5b7
	ShortSha2: ewkw7nbdqaek6mkjare8h59zgnza9bzf4begz8z01axzedtfrpvg
	Translation: 500x
	IsPrimary: false

This would create a file of 500 pixels wide and an arbitrary height. The original URL fetched by the user (500x/) would redirect to the resolved URL of;



## Permanent URL structure

I do pursue this a little more in the file urls.md.

## Simple tagging

## Set logic

## Access to original files
