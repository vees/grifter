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
	# Date
	# Time
	ctime = models.DateTimeField(null=False)
	exim = models.DateTimeField(null=False)
	# File guess
	# EXIM guess
	# Best start guess
	# Best end guess

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
	flickr_id = models.CharField(max_length=200) 
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

