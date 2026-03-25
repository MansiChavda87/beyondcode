# GrapesJS Image Upload Fixes

## Overview

This document outlines the comprehensive fixes implemented to resolve GrapesJS image upload issues where clicking "Add Image" does not open file picker and drag-drop is not working.

## Issues Fixed

1. **Click not opening file dialog** - Fixed by implementing manual file picker trigger
2. **Drag-drop not working** - Fixed by enabling dropzone and proper event handling
3. **Missing assetManager configuration** - Added complete assetManager configuration
4. **Missing HTML input element** - Added fallback HTML input creation
5. **CSS blocking clicks** - Added CSS fixes to prevent pointer-events issues

## Files Modified

### 1. `marketing/widgets.py`
**Changes:**
- Added complete `assetManager` configuration to `GrapesJSAdminWidget`
- Included upload endpoint, headers with CSRF token, and proper settings

**Key Configuration:**
```python
'assetManager': {
    'upload': '/admin/upload-image/',
    'uploadName': 'files',
    'autoAdd': True,
    'dropzone': True,
    'openAssetsOnDrop': True,
    'headers': {
        'X-CSRFToken': '{{ csrf_token }}'
    }
}
```

### 2. `marketing/templates/admin/marketing/page/change_form.html`
**Changes:**
- Added `getCSRFToken()` function for CSRF protection
- Enhanced `initializeGrapesJS()` function with assetManager configuration
- Added `fixImageUpload()` function with comprehensive fixes

**Key Fixes:**
- Manual file picker trigger on `asset:open` event
- Fallback HTML input element creation
- Drag-drop event listeners on editor container
- Proper asset manager configuration

### 3. `marketing/templates/admin/marketing/post/change_form.html`
**Changes:**
- Applied same fixes as page change form template
- Ensures consistency across all admin forms

### 4. `marketing/static/marketing/css/grapesjs-custom.css`
**Changes:**
- Added comprehensive CSS fixes to prevent click blocking
- Ensured proper z-index values for asset manager elements
- Fixed pointer-events issues

**Key CSS Rules:**
```css
.gjs-am-file-uploader {
    pointer-events: auto !important;
    z-index: 1000 !important;
}

.gjs-am-file-input {
    display: none !important;
}

.gjs-am-assets {
    z-index: 1000;
}

.gjs-am-modal {
    z-index: 2000;
}
```

### 5. `marketing/static/marketing/js/block-builder.js`
**Changes:**
- Enhanced `initGrapesJS()` function with assetManager configuration
- Added `fixImageUpload()` function for block builder
- Ensured consistency with admin template fixes

## Backend Requirements

### Upload Endpoint
The existing upload endpoint at `/admin/upload-image/` must return:
```json
{
  "data": [
    { "src": "/media/uploads/image.jpg" }
  ]
}
```

### CSRF Token
The backend must properly handle CSRF tokens in the headers:
```
X-CSRFToken: [token_value]
```

## Implementation Details

### Asset Manager Configuration
The assetManager is now properly configured with:
- **upload**: Django endpoint for image uploads
- **uploadName**: Parameter name for uploaded files
- **autoAdd**: Automatically add uploaded images to asset manager
- **dropzone**: Enable drag-drop functionality
- **openAssetsOnDrop**: Open asset manager when files are dropped
- **headers**: Include CSRF token for security

### File Picker Fix
When clicking "Add Image", the system now:
1. Listens for `asset:open` event
2. Programmatically triggers the hidden file input
3. Falls back to creating HTML input if not found

### Drag-Drop Fix
Drag-drop functionality now works by:
1. Enabling dropzone in asset manager configuration
2. Adding dragover/drop event listeners to editor container
3. Processing dropped files through the upload function

### CSS Fixes
CSS changes ensure:
- Asset manager buttons are clickable
- No z-index conflicts
- Proper pointer-events handling
- No overlay blocking issues

## Testing

A comprehensive test script `test_image_upload_fix.py` has been created to verify:
- Asset manager configuration
- CSS fixes
- JavaScript fixes
- Upload endpoint functionality

## Usage

After these fixes, users can:
1. Click "Add Image" in GrapesJS to open file picker
2. Drag and drop images directly onto the editor
3. Upload multiple images at once
4. See uploaded images automatically added to the asset manager

## Compatibility

These fixes are compatible with:
- GrapesJS v0.21.6+
- Django admin interface
- Existing upload endpoint
- All existing functionality (no breaking changes)

## Notes

- All changes maintain backward compatibility
- No modifications to database or existing data
- No changes to editor structure or other plugins
- CSRF protection is properly implemented
- File upload limits and validation remain unchanged