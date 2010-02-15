from django.db import models

# Create your models here.

class Rating(models.Model):
	# Picture
	# User
	# Rating
	# Stamp
	pass

class Location(models.Model):
	# Venue
	# Geotag
	# Neighborhood
	# City
	# State
	# Country
	pass

class Venue(models.Model):
	pass

class Moment(models.Model):
	def best_guess(self):
		if (self.userdatetime):
			return self.userdatetime
		if (self.exim):
			return self.exim
		if (self.ctime):
			return self.ctime
		if (self.range_guess_start and self.range_guess_end):
			return (self.range_guess_start, self.range_guess_end)
		if (self.range_guess_start):
			return self.range_guess_start
		if (self.range_guess_end):
			return self.range_guess_end

	userdatetime = models.DateTimeField(null=True)
	atime = models.DateTimeField(null=True)
	ctime = models.DateTimeField(null=True)
	exim = models.DateTimeField(null=True)
	range_guess_start = models.DateTimeField(null=True)
	range_guess_end = models.DateTimeField(null=True)

class Album(models.Model):
	pass

class Rotation(models.Model):
	pass

class EXIF(models.Model):
	pass

# Event has location, in case where photo has event but no location, assign to event
class Event(models.Model):
	pass

class Copyright(models.Model):
	# - [ ] None (All rights reserved)
	# - [ ] Attribution-NonCommercial-ShareAlike Creative Commons 
	# - [ ] Attribution-NonCommercial Creative Commons 
	# - [ ] Attribution-NonCommercial-NoDerivs Creative Commons 
	# - [ ] Attribution Creative Commons 
	# - [ ] Attribution-ShareAlike Creative Commons 
	# - [ ] Attribution-NoDerivs Creative Commons
	description = models.CharField(max_length=200)
	url = models.URLField(max_length=200)

class GeoTag(models.Model):
	# Long
	# Lat
	# Alt
	# Diameter
	pass

class Camera(models.Model):
	manufacturer = models.CharField(max_length=200)
	model = models.CharField(max_length=200)

class Person(models.Model):
	first = models.CharField(max_length=200)
	last = models.CharField(max_length=200)
	email = models.EmailField()

class Photographer(models.Model):
	person = models.ForeignKey(Person)

class Tag(models.Model):
	pass

class Comment(models.Model):
	pass

class Situation(models.Model):
	description = models.CharField(max_length=200)

class Picture(models.Model):
	directory = models.CharField(max_length=200)
	filename = models.CharField(max_length=200) 
	file_hash = models.CharField(max_length=200)
	# Points back to vees.net/g2/{old_id}.html
	old_id = models.IntegerField(null=True)
	# http://flickr.com/photos/vees/4116008755/
	flickr_id = models.CharField(max_length=200, null=True) 
	better_version_id = models.IntegerField(null=True)
	taken_on = models.ForeignKey(Moment)
	subject_can_id = models.IntegerField(null=True)
	subject_no_id = models.IntegerField(null=True)
	#photographer = models.ForeignKey(Photographer)
	photographer_permission = models.BooleanField()

class Subject(models.Model):
	person = models.ForeignKey(Person)
	picture = models.ForeignKey(Picture)
	model_permission = models.BooleanField()

class Old_Camera(models.Model):
	#old_id = models.IntegerField(null=False)
	manufacturer = models.CharField(max_length=50)
	model = models.CharField(max_length=50)

class Old_Location(models.Model):
	#old_id = models.IntegerField(null=False)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=2)

class Old_Photographer(models.Model):
	#old_id = models.IntegerField(null=False)
	first = models.CharField(max_length=200)
	last = models.CharField(max_length=200)
	email = models.EmailField()
	nick = models.CharField(max_length=200)
	url = models.URLField(verify_exists=True, max_length=200, null=True)

class Old_Theme(models.Model):
	#old_id = models.IntegerField(null=False)
	server = models.CharField(max_length=200)
	directory = models.CharField(max_length=200)
	description = models.CharField(max_length=200)

class Old_Picture(models.Model):
	def __unicode__(self):
		return self.filename + ": " + self.title + " in " + self.theme.description + " " + str(self.stamp)
	#old_id = models.IntegerField(null=False)
	filename = models.CharField(max_length=200)
	theme = models.ForeignKey(Old_Theme)
	title = models.CharField(max_length=200)
	location = models.ForeignKey(Old_Location)
	stamp = models.DateTimeField(null=False)
	photographer = models.ForeignKey(Old_Photographer)
	special = models.CharField(max_length=2000)
	description = models.CharField(max_length=2000)
	camera = models.ForeignKey(Old_Camera)
	counter = models.IntegerField(null=False)
	block = models.BooleanField()


