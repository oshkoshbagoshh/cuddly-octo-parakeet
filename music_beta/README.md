# Music Beta API Documentation

This document provides information about the RESTful API endpoints available in the Music Beta application.

## API Endpoints

The API is available at the `/api/` endpoint. All endpoints support standard HTTP methods (GET, POST, PUT, PATCH, DELETE) for CRUD operations.

### Authentication

Most endpoints require authentication for write operations. Read operations are generally available to unauthenticated users.

### Available Endpoints

#### Genres

- `GET /api/genres/` - List all genres
- `GET /api/genres/{id}/` - Retrieve a specific genre
- `POST /api/genres/` - Create a new genre (requires authentication)
- `PUT /api/genres/{id}/` - Update a genre (requires authentication)
- `DELETE /api/genres/{id}/` - Delete a genre (requires authentication)

#### Artists

- `GET /api/artists/` - List all artists
- `GET /api/artists/{id}/` - Retrieve a specific artist
- `POST /api/artists/` - Create a new artist (requires authentication)
- `PUT /api/artists/{id}/` - Update an artist (requires authentication)
- `DELETE /api/artists/{id}/` - Delete an artist (requires authentication)

#### Albums

- `GET /api/albums/` - List all albums
- `GET /api/albums/{id}/` - Retrieve a specific album
- `POST /api/albums/` - Create a new album (requires authentication)
- `PUT /api/albums/{id}/` - Update an album (requires authentication)
- `DELETE /api/albums/{id}/` - Delete an album (requires authentication)

#### Tracks

- `GET /api/tracks/` - List all tracks
- `GET /api/tracks/{id}/` - Retrieve a specific track
- `POST /api/tracks/` - Create a new track (requires authentication)
- `PUT /api/tracks/{id}/` - Update a track (requires authentication)
- `DELETE /api/tracks/{id}/` - Delete a track (requires authentication)

#### Users

- `GET /api/users/` - List all users (requires admin)
- `GET /api/users/{id}/` - Retrieve a specific user (requires admin)
- `POST /api/users/` - Create a new user (requires admin)
- `PUT /api/users/{id}/` - Update a user (requires admin)
- `DELETE /api/users/{id}/` - Delete a user (requires admin)

#### Ad Campaigns

- `GET /api/ad-campaigns/` - List all ad campaigns (requires authentication)
- `GET /api/ad-campaigns/{id}/` - Retrieve a specific ad campaign (requires authentication)
- `POST /api/ad-campaigns/` - Create a new ad campaign (requires authentication)
- `PUT /api/ad-campaigns/{id}/` - Update an ad campaign (requires authentication)
- `DELETE /api/ad-campaigns/{id}/` - Delete an ad campaign (requires authentication)

#### Copyrights

- `GET /api/copyrights/` - List all copyrights
- `GET /api/copyrights/{id}/` - Retrieve a specific copyright
- `POST /api/copyrights/` - Create a new copyright (requires authentication)
- `PUT /api/copyrights/{id}/` - Update a copyright (requires authentication)
- `DELETE /api/copyrights/{id}/` - Delete a copyright (requires authentication)

#### Service Requests

- `GET /api/service-requests/` - List all service requests (requires admin)
- `GET /api/service-requests/{id}/` - Retrieve a specific service request (requires admin)
- `POST /api/service-requests/` - Create a new service request (requires admin)
- `PUT /api/service-requests/{id}/` - Update a service request (requires admin)
- `DELETE /api/service-requests/{id}/` - Delete a service request (requires admin)

## Response Format

All responses are in JSON format. List endpoints return paginated results with the following structure:

```json
{
  "count": 123,
  "next": "http://api.example.org/api/resource/?page=4",
  "previous": "http://api.example.org/api/resource/?page=2",
  "results": [
    {
      "id": 1,
      "name": "Example",
      ...
    },
    ...
  ]
}
```

Detail endpoints return a single object:

```json
{
  "id": 1,
  "name": "Example",
  ...
}
```

## Error Handling

Errors are returned with appropriate HTTP status codes and a JSON response with details about the error:

```json
{
  "detail": "Not found."
}
```

## Testing

Tests for the API endpoints are available in the `test_api.py` file. Run the tests with:

```bash
python manage.py test music_beta.test_api
```