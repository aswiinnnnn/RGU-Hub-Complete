# RGU Hub Backend Documentation

## Overview

RGU Hub Backend is a Django REST Framework API that provides study materials and recruitment opportunities for Rahul Gandhi University students. The system supports multiple academic programs with flexible term structures (semesters/years) and comprehensive material management.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Setup Instructions](#setup-instructions)
3. [Database Models](#database-models)
4. [API Endpoints](#api-endpoints)
5. [API Testing Guide](#api-testing-guide)
6. [Query Examples](#query-examples)
7. [Cloudinary Integration](#cloudinary-integration)
8. [Development Guidelines](#development-guidelines)

## Project Structure

```
rguHub Backend/
├── manage.py                 # Django management script
├── db.sqlite3               # SQLite database
├── rguHub/                  # Main Django project
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── resources/               # Study materials app
│   ├── models.py            # Database models
│   ├── views.py             # API views
│   ├── serializers.py       # Data serializers
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin interface
│   └── migrations/          # Database migrations
├── recruitment/             # Job postings app
│   ├── models.py            # Recruitment models
│   ├── views.py             # Recruitment API views
│   ├── serializers.py       # Recruitment serializers
│   ├── urls.py              # Recruitment URLs
│   └── admin.py             # Admin interface
└── uploads/                 # Local file uploads
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rguHub-Backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## Database Models

### Core Models Hierarchy

```
Program (BSCN, BPT, etc.)
  └── Syllabus (CBCS 2022, etc.)
      └── Term (Semester 1, Year 1, etc.)
          └── Subject (BN101, BN102, etc.)
              └── SubjectMaterial (PDFs, documents)
```

### Model Details

#### Program
- **Purpose**: Academic programs (B.Sc Nursing, BPT, etc.)
- **Key Fields**: `name`, `short_name`, `duration_years`
- **Usage**: Filter subjects and recruitments by program

#### Syllabus
- **Purpose**: Curriculum versions (CBCS 2022, RGUHS 2020, etc.)
- **Key Fields**: `program`, `name`, `effective_from`, `effective_to`
- **Usage**: Organize subjects by academic regulation

#### Term
- **Purpose**: Flexible academic terms (Semesters or Years)
- **Key Fields**: `syllabus`, `term_number`, `term_type`, `slug`
- **Usage**: Group subjects by academic period

#### Subject
- **Purpose**: Individual courses/subjects
- **Key Fields**: `term`, `code`, `name`, `subject_type`, `slug`
- **Usage**: Organize study materials by subject

#### MaterialType
- **Purpose**: Categories of study materials
- **Key Fields**: `name`, `slug`, `description`, `icon`, `color`
- **Usage**: Filter materials by type (Notes, PYQ, etc.)

#### SubjectMaterial
- **Purpose**: Actual study material files
- **Key Fields**: `subject`, `material_type`, `title`, `file`, `url`, `year`, `month`
- **Usage**: Store and serve study materials via Cloudinary

#### Recruitment
- **Purpose**: Job postings and opportunities
- **Key Fields**: `program`, `company_name`, `position`, `job_type`, `deadline`
- **Usage**: Display job opportunities for students

## API Endpoints

### Base URL
```
http://127.0.0.1:8000/
```

### Resources App Endpoints

#### Material Types
- `GET /material-types/` - List all material types
- `GET /material-types/{id}/` - Get specific material type

#### Subjects
- `GET /subjects/` - List all subjects
- `GET /subjects/?course=BSCN` - Filter by program
- `GET /subjects/?course=BSCN&sem=1` - Filter by program and semester
- `GET /subjects/?course=BSCN&year=1` - Filter by program and year
- `GET /subjects/{id}/` - Get specific subject

#### Materials
- `GET /materials/` - List all materials
- `GET /materials/?subject=bn101-anatomy-physiology` - Filter by subject
- `GET /materials/?type=notes` - Filter by material type
- `GET /materials/?subject=bn101&type=pyq` - Combined filtering
- `POST /materials/` - Create new material
- `PUT /materials/{id}/` - Update material
- `PATCH /materials/{id}/` - Partial update material
- `DELETE /materials/{id}/` - Delete material

### Recruitment App Endpoints

#### Job Postings
- `GET /recruitments/` - List all job postings
- `GET /recruitments/?program=BSCN` - Filter by program
- `GET /recruitments/{id}/` - Get specific job posting

#### Latest Updates
- `GET /latest-updates/` - Get recent materials and job postings

## API Testing Guide

### Using Django REST Framework Browsable API

1. **Start the server**
   ```bash
   python manage.py runserver
   ```

2. **Open browser and navigate to**
   ```
   http://127.0.0.1:8000/
   ```

3. **Browse available endpoints**
   - Click on any endpoint to see available operations
   - Use the "GET" button to test GET requests
   - Use forms for POST/PUT/PATCH requests

### Using cURL Commands

#### Test Material Types
```bash
# List all material types
curl -X GET "http://127.0.0.1:8000/material-types/"

# Get specific material type
curl -X GET "http://127.0.0.1:8000/material-types/1/"
```

#### Test Subjects with Filtering
```bash
# List all subjects
curl -X GET "http://127.0.0.1:8000/subjects/"

# Filter by program
curl -X GET "http://127.0.0.1:8000/subjects/?course=BSCN"

# Filter by program and semester
curl -X GET "http://127.0.0.1:8000/subjects/?course=BSCN&sem=1"

# Filter by program and year
curl -X GET "http://127.0.0.1:8000/subjects/?course=BSCN&year=1"
```

#### Test Materials with Filtering
```bash
# List all materials
curl -X GET "http://127.0.0.1:8000/materials/"

# Filter by subject slug
curl -X GET "http://127.0.0.1:8000/materials/?subject=bn101-anatomy-physiology"

# Filter by material type
curl -X GET "http://127.0.0.1:8000/materials/?type=notes"

# Combined filtering
curl -X GET "http://127.0.0.1:8000/materials/?subject=bn101&type=pyq"
```

#### Test Recruitment
```bash
# List all job postings
curl -X GET "http://127.0.0.1:8000/recruitments/"

# Filter by program
curl -X GET "http://127.0.0.1:8000/recruitments/?program=BSCN"

# Get latest updates
curl -X GET "http://127.0.0.1:8000/latest-updates/"
```

### Using Postman

1. **Create a new collection** called "RGU Hub API"

2. **Add requests for each endpoint**:
   - Set method to GET
   - Set URL to `http://127.0.0.1:8000/endpoint/`
   - Add query parameters as needed

3. **Test different scenarios**:
   - Valid requests
   - Invalid parameters
   - Non-existent resources

## Query Examples

### Common Query Patterns

#### Get Subjects for B.Sc Nursing 1st Semester
```
GET /subjects/?course=BSCN&sem=1
```

#### Get All Notes for Anatomy Subject
```
GET /materials/?subject=bn101-anatomy-physiology&type=notes
```

#### Get PYQ Materials for 2023
```
GET /materials/?type=pyq&year=2023
```

#### Get Job Postings for B.Sc Nursing
```
GET /recruitments/?program=BSCN
```

#### Get Latest Updates (Homepage)
```
GET /latest-updates/
```

### Advanced Filtering

#### Multiple Subject Materials
```
GET /materials/?subject=bn101-anatomy-physiology&subject=bn102-pharmacology
```

#### Materials by Year Range
```
GET /materials/?year=2023&year=2024
```

#### Job Postings by Type
```
GET /recruitments/?program=BSCN&job_type=FT
```

## Cloudinary Integration

### Configuration

The system uses Cloudinary for file storage. Configuration is in `settings.py`:

```python
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "your_cloud_name",
    "API_KEY": "your_api_key", 
    "API_SECRET": "your_api_secret",
}
```

### File Upload Process

1. **Upload via Admin Interface**:
   - Go to `http://127.0.0.1:8000/admin/`
   - Navigate to Subject Materials
   - Create new material and upload file
   - File automatically uploads to Cloudinary

2. **Upload via API**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/materials/" \
        -H "Content-Type: multipart/form-data" \
        -F "subject=1" \
        -F "material_type=1" \
        -F "title=anatomy_notes.pdf" \
        -F "file=@/path/to/file.pdf" \
        -F "description=Comprehensive anatomy notes"
   ```

### File Access

- Files are accessible via Cloudinary URLs
- URLs are auto-generated and stored in the `url` field
- Direct download links are provided in API responses

## Development Guidelines

### Adding New Models

1. **Define model** in appropriate app's `models.py`
2. **Create migration**: `python manage.py makemigrations`
3. **Apply migration**: `python manage.py migrate`
4. **Create serializer** in `serializers.py`
5. **Create viewset** in `views.py`
6. **Add URL routing** in `urls.py`
7. **Register in admin** in `admin.py`

### Adding New API Endpoints

1. **Create viewset** in `views.py`
2. **Add URL pattern** in `urls.py`
3. **Test endpoint** using DRF browsable API
4. **Document endpoint** in this README

### Database Management

#### Create Migration
```bash
python manage.py makemigrations
```

#### Apply Migrations
```bash
python manage.py migrate
```

#### Reset Database (Development Only)
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Admin Interface

Access the admin interface at `http://127.0.0.1:8000/admin/`

- **Programs**: Manage academic programs
- **Syllabi**: Manage curriculum versions
- **Terms**: Manage semesters/years
- **Subjects**: Manage individual subjects
- **Material Types**: Manage material categories
- **Subject Materials**: Manage study materials
- **Recruitments**: Manage job postings

### Logging

The system includes logging for debugging API requests:

```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"Request received with parameters: {params}")
```

### Error Handling

- **400 Bad Request**: Invalid query parameters
- **404 Not Found**: Resource doesn't exist
- **500 Internal Server Error**: Server-side error

### CORS Configuration

CORS is configured to allow all origins in development:

```python
CORS_ALLOW_ALL_ORIGINS = True
```

For production, configure specific origins:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourdomain.com",
]
```

## Troubleshooting

### Common Issues

1. **Migration Errors**:
   ```bash
   python manage.py migrate --fake-initial
   ```

2. **CORS Issues**:
   - Ensure `corsheaders` is in `INSTALLED_APPS`
   - Check `CORS_ALLOW_ALL_ORIGINS = True`

3. **Cloudinary Upload Issues**:
   - Verify Cloudinary credentials
   - Check file size limits
   - Ensure proper file format

4. **API Not Responding**:
   - Check if server is running
   - Verify URL endpoints
   - Check Django logs

### Debug Mode

Enable debug mode in `settings.py`:

```python
DEBUG = True
```

This provides detailed error pages and additional logging.

## Production Deployment

### Environment Variables

Set these environment variables for production:

```bash
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=your-database-url
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### Security Considerations

1. **Change SECRET_KEY** in production
2. **Set DEBUG=False** in production
3. **Configure ALLOWED_HOSTS** properly
4. **Use HTTPS** in production
5. **Implement proper CORS** configuration
6. **Add authentication** if needed
7. **Rate limiting** for API endpoints

## Support

For questions or issues:

1. Check this documentation
2. Review Django REST Framework documentation
3. Check Cloudinary documentation for file upload issues
4. Create an issue in the project repository

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Author**: RGU Hub Development Team
