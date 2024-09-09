from django.contrib import admin
from .models import File

# Register your models here.

# To display in admin panel
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ["user", "upload_path", "upload_time",
                    "status", "duration", "processed_file_path", "error_message"]
