"""
Utility functions for GrapesJS integration
"""
import json


def render_grapesjs_content(content_data):
    """
    Render GrapesJS content with proper CSS styling for frontend display
    
    Args:
        content_data: Either a string (JSON) or dict containing GrapesJS data
        
    Returns:
        str: HTML content with embedded CSS for proper rendering
    """
    if not content_data:
        return ""
    
    # Parse content data if it's a string
    if isinstance(content_data, str):
        try:
            content_data = json.loads(content_data)
        except json.JSONDecodeError:
            return content_data  # Return as-is if it's not valid JSON
    
    # Get HTML and CSS from the content data
    html = content_data.get('html', '')
    css = content_data.get('css', '')
    
    if not html:
        return ""
    
    # Build the complete HTML with embedded CSS
    # Include the GrapesJS base CSS to ensure columns work properly
    base_css = """
    <style>
        .gjs-row {
            display: flex;
            flex-wrap: wrap;
            width: 100%;
        }

        .gjs-cell {
            flex: 1 1 0;
            min-width: 0;
            padding: 10px;
        }

        /* Ensure proper box sizing */
        .gjs-row > .gjs-cell {
            box-sizing: border-box;
        }

        /* Optional responsive improvement */
        @media (max-width: 768px) {
            .gjs-row {
                flex-direction: column;
            }
        }
    </style>
    """
    
    # Combine base CSS with any custom CSS from the editor
    combined_css = base_css
    if css:
        combined_css += f"<style>{css}</style>"
    
    # Return the complete HTML with embedded CSS
    return f"{combined_css}{html}"


def get_grapesjs_html(content_data):
    """
    Extract just the HTML from GrapesJS content data
    
    Args:
        content_data: Either a string (JSON) or dict containing GrapesJS data
        
    Returns:
        str: HTML content only
    """
    if not content_data:
        return ""
    
    # Parse content data if it's a string
    if isinstance(content_data, str):
        try:
            content_data = json.loads(content_data)
        except json.JSONDecodeError:
            return content_data  # Return as-is if it's not valid JSON
    
    return content_data.get('html', '')


def get_grapesjs_css(content_data):
    """
    Extract just the CSS from GrapesJS content data
    
    Args:
        content_data: Either a string (JSON) or dict containing GrapesJS data
        
    Returns:
        str: CSS content only
    """
    if not content_data:
        return ""
    
    # Parse content data if it's a string
    if isinstance(content_data, str):
        try:
            content_data = json.loads(content_data)
        except json.JSONDecodeError:
            return ""
    
    return content_data.get('css', '')