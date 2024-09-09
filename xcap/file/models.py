from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# Custom function to define upload file path


def xml_upload_path(instance, filename):
    return f"{instance.user.username}/xml_files/${filename}"

# Custom function to define processed file path


def xml_download_path(instance, filename):
    return f"{instance.user.username}/processed_files/${filename}"


class File(models.Model):
    """File Model to store information related to the xml files"""
    STATUS_CHOICES = {  # Choices which acts as Enums
        "UPLOADED": "Uploaded",
        "PROCESSING": "Processing",
        "COMPLETED": "Completed",
        "FAILED": "Failed",
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_path = models.FileField(upload_to=xml_upload_path)
    upload_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="UPLOADED")
    processing_start_time = models.DateTimeField(null=True, blank=True)
    processing_end_time = models.DateTimeField(null=True, blank=True)
    processed_file_path = models.FileField(
        upload_to=xml_download_path, null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ['-id']

    def file_name(self):
        """To extract file name from the path"""
        return self.upload_path.name.split("/")[-1]

    @property
    def duration(self):
        """To calculate the duration"""
        return (self.processing_end_time - self.processing_start_time) if self.processing_start_time and self.processing_end_time else 0
