from xcap.utils import capitalize_xml
from file.models import File
from django.utils import timezone
from django.core.files.base import ContentFile
from celery import shared_task

@shared_task
def process_xml(file_id_list: list[int]):
    """ Function to process XML file """

    # Fetch all the files using the file ids
    files = File.objects.filter(id__in = file_id_list)
    # Put the files in processing stage and set the processing start time
    files.update(status='PROCESSING', processing_start_time=timezone.now())

    # Initialize lists for bulk update
    processed_files = []
    failed_files = []

    for file in files:
        try:
            # Process the XML file and get the in-memory file object
            processed_file = capitalize_xml(file.upload_path.path)

            # Define a new file name
            new_file_name: str = f"processed_{file.id}.xml"

            # Create a ContentFile to upload the processed XML as a new file
            processed_file_content = ContentFile(
                processed_file.read(), name=new_file_name)
            
            # Save the processed file content to a processed file location
            file.processed_file_path.save(
                new_file_name, processed_file_content)

            # Set the new status and processing end time
            file.status = 'COMPLETED'
            file.processing_end_time = timezone.now()

            # Collect the processed file for bulk update
            processed_files.append(file)

        except Exception as e:
            # Catch any error during the exception and mark the files as failed
            file.status = 'FAILED'
            file.error_message = str(e)
            failed_files.append(file)

    # Perform bulk update for completed files
    if processed_files:
        File.objects.bulk_update(
            processed_files, [
                'status', 'processing_end_time', 'processed_file_path']
        )

    # Perform bulk update for failed files
    if failed_files:
        File.objects.bulk_update(
            failed_files, ['status', 'error_message']
        )
