# How to Run test_editorjs_integration.py

## Overview
The `test_editorjs_integration.py` file is a comprehensive test script that verifies the Editor.js integration in your Django admin interface.

## Prerequisites
- Python 3.6+
- Django project properly configured
- All dependencies installed

## Method 1: Direct Python Execution

### Step 1: Navigate to the project directory
```bash
cd beyondcode_project
```

### Step 2: Run the test script
```bash
python test_editorjs_integration.py
```

## Method 2: Using Django's Test Framework

### Step 1: Navigate to the project directory
```bash
cd beyondcode_project
```

### Step 2: Run using Django's test runner
```bash
python manage.py test test_editorjs_integration
```

## Method 3: Using Python Module Execution

### Step 1: Navigate to the parent directory
```bash
cd ..
```

### Step 2: Run as a Python module
```bash
python -m beyondcode_project.test_editorjs_integration
```

## Expected Output

When the test runs successfully, you should see output similar to:

```
============================================================
Editor.js Integration Test Suite
============================================================
Testing Editor.js Widget Configuration...
✓ EditorJSAdminWidget created successfully
✓ Widget media configured with 1 CSS files and 3 JS files
✓ PageForm and PostForm created successfully
✓ PageForm uses EditorJSAdminWidget for blocks_json
✓ PostForm uses EditorJSAdminWidget for blocks_json

Widget configuration test completed!
Testing Static Files...
✓ marketing/css/editorjs-custom.css exists
✓ marketing/js/editorjs-widget.js exists
✓ marketing/js/editorjs-drag-drop.js exists

Static files test completed!
Testing Admin Templates...
✓ marketing/templates/admin/marketing/page/change_form.html exists
✓ marketing/templates/admin/marketing/post/change_form.html exists

Admin templates test completed!
Testing Models...
✓ Page model has blocks_json field
✓ Post model has blocks_json field

Models test completed!

============================================================
All tests completed!
Editor.js integration appears to be properly configured.

Next steps:
1. Run 'python manage.py collectstatic' to collect static files
2. Run 'python manage.py runserver' to start the development server
3. Navigate to Django admin and test the Page and Post forms
4. Verify that Editor.js loads properly with drag-and-drop functionality
============================================================
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Django Settings Error
**Error**: `django.core.exceptions.ImproperlyConfigured: Requested setting USE_I18N, but settings are not configured.`
**Solution**: Make sure you're running from the correct directory and Django settings are properly configured.

#### 2. Module Import Error
**Error**: `ModuleNotFoundError: No module named 'marketing'`
**Solution**: Ensure you're in the correct directory and the Django app is properly installed.

#### 3. Database Connection Error
**Error**: `django.db.utils.OperationalError: unable to open database file`
**Solution**: Run migrations first:
```bash
python manage.py migrate
```

#### 4. Static Files Missing
**Error**: Static files not found
**Solution**: Collect static files:
```bash
python manage.py collectstatic
```

## What the Test Checks

### 1. Widget Configuration
- Verifies that `EditorJSAdminWidget` can be created
- Checks that widget media (CSS and JS files) is properly configured
- Ensures that PageForm and PostForm use the Editor.js widget

### 2. Static Files
- Verifies that all required CSS and JS files exist
- Checks for: `editorjs-custom.css`, `editorjs-widget.js`, `editorjs-drag-drop.js`

### 3. Admin Templates
- Ensures that Django admin templates exist for Page and Post models
- These templates integrate Editor.js into the admin interface

### 4. Model Fields
- Verifies that Page and Post models have the `blocks_json` field
- This field stores the Editor.js content as JSON

## After Running Tests Successfully

### 1. Collect Static Files
```bash
python manage.py collectstatic
```

### 2. Start Development Server
```bash
python manage.py runserver
```

### 3. Test in Browser
1. Navigate to `http://localhost:8000/admin/`
2. Log in with your admin credentials
3. Go to Pages or Posts section
4. Create or edit a page/post
5. Verify that Editor.js loads properly with drag-and-drop functionality

## Additional Testing

### Test the Simple Block Editor
You can also test the new simple block editor:
```bash
python test_simple_block_editor.py
```

### Test URL Configuration
```bash
python test_urls.py
```

## Notes
- The test script is self-contained and doesn't require a database connection for most checks
- It verifies the integration at the configuration level
- For full functional testing, you'll need to run the Django development server and test in a browser
- Make sure all dependencies from `requirements.txt` are installed