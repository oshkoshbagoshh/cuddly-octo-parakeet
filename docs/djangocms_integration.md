# Django CMS Integration

This document provides an overview of the Django CMS integration in the TFN CTV project.

## Changes Made

The following changes were made to integrate Django CMS:

1. **Updated settings.py**:
   - Added Django CMS apps to INSTALLED_APPS
   - Added Django CMS middleware
   - Added Django CMS context processors
   - Added language settings for Django CMS
   - Added CMS_TEMPLATES configuration

2. **Updated urls.py**:
   - Added Django CMS URLs
   - Moved music_beta URLs to /music/ path
   - Added i18n_patterns for internationalization

3. **Updated templates**:
   - Modified base.html to include Django CMS tags
   - Created cms_home.html, cms_page.html, and cms_sidebar.html templates
   - Created a custom menu template for Bootstrap styling

## Using Django CMS

### Initial Setup

After applying these changes, you need to run migrations to set up the Django CMS database tables:

```bash
python manage.py migrate
```

### Creating a Superuser

If you haven't already, create a superuser to access the Django admin:

```bash
python manage.py createsuperuser
```

### Accessing the CMS

1. Start the development server:

```bash
python manage.py runserver
```

2. Visit http://localhost:8000/ in your browser
3. Log in using the superuser credentials
4. You should see the Django CMS toolbar at the top of the page

### Creating Pages

1. Click on "Create" in the CMS toolbar
2. Select a template (Home Template, Content Page, or Page with Sidebar)
3. Fill in the page details (title, slug, etc.)
4. Click "Save" to create the page

### Adding Content

1. Navigate to a page
2. Click "Edit" in the CMS toolbar
3. Click on a placeholder (e.g., "content")
4. Add plugins (text, image, video, etc.)
5. Save your changes

### Managing the Menu

1. Go to the Django admin (http://localhost:8000/admin/)
2. Navigate to "Pages" under "CMS"
3. Use the page tree to organize your pages
4. The menu will automatically update based on the page structure

## Templates

### Home Template (cms_home.html)

A template with multiple content areas:
- Main content area
- Three column boxes
- Bottom content area

### Content Page (cms_page.html)

A simple template with:
- Main content area
- Additional content area

### Page with Sidebar (cms_sidebar.html)

A two-column template with:
- Main content area (8 columns)
- Sidebar (4 columns)

## Next Steps

1. Customize the templates to match your design requirements
2. Install additional Django CMS plugins as needed
3. Configure user permissions for content editing
4. Set up workflows for content approval