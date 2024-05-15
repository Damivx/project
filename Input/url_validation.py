import re

def validate_url(url):
    """
    Validate the URL format to ensure it conforms to HTTP/HTTPS standards.

    Args:
    - url (str): The URL to validate.

    Returns:
    - bool: True if the URL is valid, False otherwise.
    """
    # Regular expression pattern for valid URL format with http or https
    url_pattern = r"^(http|https)://[a-zA-Z0-9.-]+.[a-zA-Z]{2,}(?::\d{1,5})?(/\S*)?$"

    # Check if URL matches the pattern
    if re.match(url_pattern, url):
        return True
    else:
        return False

# Prompt the user for input
input_url = input("Enter a URL to validate: ")

# Validate the input URL
if validate_url(input_url):
    print("URL is valid.")
else:
    print("Invalid URL format.")
