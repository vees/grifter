from grifter.regatta.models import Picture, Moment, Old_Picture, PictureSimple
from django.contrib import admin
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

class PictureSimpleAdmin(admin.ModelAdmin):
	list_display = ('filename','directory','imgtag','rotation','stamp')
	list_editable = ('rotation',)
	list_filter = ('rotation',)
	radio_fields = {"rotation": admin.HORIZONTAL}
	list_per_page = 15
	save_on_top = True
	actions_on_top = True
	actions = ['rotate_90_cw','rotate_90_ccw']	
	def rotate_90_cw(self, request, queryset):
		queryset.update(rotation=90)
		return HttpResponseRedirect("/admin/regatta/picturesimple/?rotation__exact=180")
	def rotate_90_ccw(self, request, queryset):
		queryset.update(rotation=270)
		return HttpResponseRedirect("/admin/regatta/picturesimple/?rotation__exact=180")
	rotate_90_cw.short_description = "Rotate 90 CW"
	rotate_90_ccw.short_description = "Rotate 90 CCW"

admin.site.register(Picture)
admin.site.register(Moment)
admin.site.register(Old_Picture)
admin.site.register(PictureSimple, PictureSimpleAdmin)

