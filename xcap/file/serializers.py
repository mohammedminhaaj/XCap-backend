
from rest_framework.serializers import ModelSerializer, Serializer, FileField, ListField
from .models import File
from rest_framework.exceptions import ValidationError
from .models import File
from .tasks import process_xml


class FileSerializer(ModelSerializer):
    """Serializer to get File data"""
    class Meta:
        model = File
        fields = ["id", "status", "duration",
                  "file_name", "upload_time", "error_message", "processed_file_path"]


class FileUploadSerializer(Serializer):
    """Serializer to upload file data"""
    files = ListField(child=FileField())  # Defining a list of files

    def __init__(self, instance=None, data=..., **kwargs):
        # Getting current user from key word arguments
        self.current_user = kwargs.pop("current_user", None)

        # Throw a validation error if user is None
        if not self.current_user:
            raise ValidationError("No user available")
        super().__init__(instance, data, **kwargs)

    def validate(self, attrs):
        """Custom validation for uploaded files"""
        files = attrs.get('files', [])
        # Check if files are present in the request
        if not files:
            raise ValidationError("No files provided")

        # Check the file extension
        for file in files:
            name: str = file.name
            if not name.endswith(".xml"):
                # Throw a validation error if any unsupported file is supplied
                raise ValidationError("File type not supported")
        return super().validate(attrs)

    def create(self, validated_data):
        """Function to save the file and start processing"""
        files_obj = [File(user=self.current_user, upload_path=file)
                     for file in validated_data["files"]]
        # Bulk creating to save additional queries
        files = File.objects.bulk_create(files_obj)
        # Async execution using celery
        process_xml.delay(files)
        
        return files
