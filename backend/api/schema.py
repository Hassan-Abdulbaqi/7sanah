"""
Schema customization for DRF Spectacular.
This module contains hooks to customize the OpenAPI schema generation.
"""

def spectacular_preprocessing_hook(endpoints):
    """
    Filter endpoints to only show Hijri calendar and Qibla direction public APIs.
    This hook runs before the schema is generated.
    """
    # Define the list of public endpoints we want to show
    public_endpoint_patterns = [
        '/api/hijri-calendar/',
        '/api/hijri-months/',
        '/api/hijri-events/',
        '/api/astronomical-events/',
        '/api/qibla-direction/',
        # Include schema endpoints
        '/api/schema/',
        '/api/schema/swagger-ui/',
    ]
    
    # Filter endpoints
    filtered_endpoints = []
    for path, path_regex, method, callback in endpoints:
        # Check if the path matches any of our public endpoint patterns
        is_public = any(public_pattern in path for public_pattern in public_endpoint_patterns)
        
        # Include the endpoint if it's public
        if is_public:
            filtered_endpoints.append((path, path_regex, method, callback))
    
    return filtered_endpoints

def spectacular_postprocessing_hook(result, generator, request, public):
    """
    Customize the generated schema after it's been created.
    This hook runs after the schema is generated.
    """
    # You can modify the schema here if needed
    if 'tags' in result:
        # Keep only relevant tags
        public_tags = ['hijri-months', 'hijri-events', 'astronomical-events', 'qibla-direction']
        result['tags'] = [tag for tag in result['tags'] if tag['name'] in public_tags]
    
    return result
