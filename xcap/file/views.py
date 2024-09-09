from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from .models import File
from .serializers import FileSerializer, FileUploadSerializer
from xcap.utils import response_structure, SUCCESS_MESSAGE, SERVER_ERROR_MESSAGE
from rest_framework import status
from django.core.paginator import Paginator


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_files(request: Request):
    """Get user files with query params"""
    # Set the page
    page = request.query_params.get("page", 1)

    # Set the limit
    limit = request.query_params.get("limit", 9999)

    # Set the search param
    search = request.query_params.get("search", None)

    # If search param exists, create a dictionary so that it can be appended to the query
    search_term= {
        "upload_path__icontains": search} if search else {}
    
    # Get the files belonging to user
    files = File.objects.filter(user=request.user).filter(**search_term)
    
    # Create serailizer instance
    serializer = FileSerializer(files, many=True)

    # Create paginator instance for paginated response
    paginator = Paginator(serializer.data, int(limit))

    # Get the paginated response
    paginated_results = paginator.get_page(int(page)).object_list

    # Return the paged results along with the total count
    return response_structure(SUCCESS_MESSAGE, status.HTTP_200_OK, paginated_results, count=paginator.count)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_file(request: Request):
    """Function to handle file uploads"""
    # Create a serializer instance and pass the files
    serializer = FileUploadSerializer(data=request.FILES, current_user=request.user)

    # Check if the data is valid
    if serializer.is_valid():
        # Save the data
        serializer.save()
        return response_structure(SUCCESS_MESSAGE, code=status.HTTP_200_OK)
    return response_structure(SERVER_ERROR_MESSAGE, code=status.HTTP_400_BAD_REQUEST)
