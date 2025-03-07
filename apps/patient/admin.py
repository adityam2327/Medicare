from django.contrib import admin





from .models import CommunityUpdate
from django.utils.html import format_html

@admin.register(CommunityUpdate)
class CommunityUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'image_preview')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"


from .models import HealthcareProfessional
@admin.register(HealthcareProfessional)
class HealthcareProfessionalAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'experience', 'availability', 'profile_image_preview')
    list_filter = ('specialization', 'availability')
    search_fields = ('name', 'specialization')

    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;"/>', obj.profile_image.url)
        return "No Image"
    profile_image_preview.short_description = "Profile Image"



from .models import MedicalInfo
from django.utils.html import format_html

@admin.register(MedicalInfo)
class MedicalInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'image_preview')
    list_filter = ('category', 'published_at')
    search_fields = ('title', 'category', 'content')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image"



