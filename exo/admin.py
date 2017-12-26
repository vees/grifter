from django.contrib import admin
from exo.models import *

admin.site.register(ContentKey)
admin.site.register(Tag2)
admin.site.register(Redirect)
admin.site.register(ContentSignature)
admin.site.register(ContentContainer)
admin.site.register(ContentInstance)
admin.site.register(Picture)
admin.site.register(TransformedPicture)

#class PictureSimpleAdmin(admin.ModelAdmin):
#	list_display = ('filename','directory','imgtag','rotation','stamp')
#	list_editable = ('rotation',)
#	list_filter = ('rotation',)
#	radio_fields = {"rotation": admin.HORIZONTAL}
#	list_per_page = 15
#	save_on_top = True
#	actions_on_top = True
#	actions = ['rotate_90_cw','rotate_90_ccw']
#	def rotate_90_cw(self, request, queryset):
#		queryset.update(rotation=90)
#		return HttpResponseRedirect("/admin/regatta/picturesimple/?rotation__exact=180")
#	def rotate_90_ccw(self, request, queryset):
#		queryset.update(rotation=270)
#		return HttpResponseRedirect("/admin/regatta/picturesimple/?rotation__exact=180")
#	rotate_90_cw.short_description = "Rotate 90 CW"
#	rotate_90_ccw.short_description = "Rotate 90 CCW"
