from drf_spectacular.extensions import OpenApiFilterExtension
from drf_spectacular.plumbing import build_basic_type

# The main filtering is now done through SCHEMA_PATH_PREFIX in settings.py
# This class is kept for additional customization if needed
class CustomSchemaFilter(OpenApiFilterExtension):
    """
    Additional filter for API schema customization
    """
    target_class = 'rest_framework.views.APIView'
    priority = 0