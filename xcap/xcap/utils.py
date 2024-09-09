from typing import Any, Dict, Optional
from rest_framework.response import Response
from xml.etree import ElementTree as ET
import io

# Predefined messages for consistency across responses
SERVER_ERROR_MESSAGE = "Something went wrong!"
SUCCESS_MESSAGE = "Success"


def response_structure(
    message: str,
    code: int,
    data: Optional[Dict[str, Any]] = None,
    **kwargs: Any
) -> Response:
    """
    Constructs a standardized response structure for API responses.

    Args:
        message (str): The message to include in the response.
        code (int): The HTTP status code for the response.
        data (Optional[Dict[str, Any]]): Optional dictionary containing additional data to include in the response.
        **kwargs (Any): Additional keyword arguments to include in the response.

    Returns:
        Response: A Response object with the structured data.
    """
    # Construct the base response dictionary
    response_dict = {
        "message": message,
        **kwargs
    }

    # Add data to the response dictionary if provided
    if data is not None:
        response_dict["data"] = data

    # Return the Response object with the structured data and status code
    return Response(data=response_dict, status=code)


def capitalize_xml(input_file: str):
    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Function to convert text content to uppercase
    def convert_to_uppercase(element):
        # If the element has text content, convert it to uppercase
        if element.text:
            element.text = element.text.upper()
        # If the element has a text after the element, convert it to uppercase
        if element.tail:
            element.tail = element.tail.upper()
        # Recursively process all child elements
        for child in element:
            convert_to_uppercase(child)

    # Start processing from the root
    convert_to_uppercase(root)

    # Create an in-memory file object to hold the processed XML
    output = io.BytesIO()

    # Write the processed XML to the output file
    tree.write(output, encoding='utf-8', xml_declaration=True)

    # Reset the cursor of the file object to the beginning
    output.seek(0)

    return output
