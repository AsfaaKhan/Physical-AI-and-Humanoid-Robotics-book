# API Contract: Authentication Service

**Feature**: 003-user-auth-personalization
**Version**: 1.0.0
**Base URL**: `/api/v1/auth`

## Authentication Endpoints

### POST /auth/signup
Register a new user with background information

#### Request
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "background": {
    "software_experience": "intermediate",
    "programming_background": "basic",
    "hardware_knowledge": "intermediate"
  }
}
```

#### Request Validation
- `email`: Required, valid email format
- `password`: Required, minimum 8 characters
- `background.software_experience`: Required, enum ["beginner", "intermediate", "expert"]
- `background.programming_background`: Required, enum ["none", "basic", "intermediate", "advanced"]
- `background.hardware_knowledge`: Required, enum ["none", "basic", "intermediate", "advanced"]

#### Responses
- **201 Created**: User successfully registered
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "session_token": "jwt-token",
  "profile_complete": true,
  "background": {
    "software_experience": "intermediate",
    "programming_background": "basic",
    "hardware_knowledge": "intermediate"
  }
}
```

- **400 Bad Request**: Invalid input data
- **409 Conflict**: Email already exists
- **500 Internal Server Error**: Server error

### POST /auth/signin
Authenticate existing user

#### Request
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

#### Request Validation
- `email`: Required, valid email format
- `password`: Required

#### Responses
- **200 OK**: Authentication successful
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "session_token": "jwt-token",
  "background": {
    "software_experience": "intermediate",
    "programming_background": "basic",
    "hardware_knowledge": "intermediate"
  }
}
```

- **400 Bad Request**: Invalid input format
- **401 Unauthorized**: Invalid credentials
- **500 Internal Server Error**: Server error

### POST /auth/signout
End current user session

#### Headers
```
Authorization: Bearer {session_token}
```

#### Responses
- **200 OK**: Session terminated successfully
- **401 Unauthorized**: Invalid or expired token
- **500 Internal Server Error**: Server error

### GET /auth/profile
Get current user profile

#### Headers
```
Authorization: Bearer {session_token}
```

#### Responses
- **200 OK**: Profile retrieved successfully
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "background": {
    "software_experience": "intermediate",
    "programming_background": "basic",
    "hardware_knowledge": "intermediate"
  },
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z",
  "profile_completed": true
}
```

- **401 Unauthorized**: Invalid or expired token
- **500 Internal Server Error**: Server error

### PUT /auth/profile
Update user profile including background information

#### Headers
```
Authorization: Bearer {session_token}
```

#### Request
```json
{
  "background": {
    "software_experience": "expert",
    "programming_background": "intermediate",
    "hardware_knowledge": "advanced"
  }
}
```

#### Request Validation
- `background.software_experience`: Optional, enum ["beginner", "intermediate", "expert"]
- `background.programming_background`: Optional, enum ["none", "basic", "intermediate", "advanced"]
- `background.hardware_knowledge`: Optional, enum ["none", "basic", "intermediate", "advanced"]

#### Responses
- **200 OK**: Profile updated successfully
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "background": {
    "software_experience": "expert",
    "programming_background": "intermediate",
    "hardware_knowledge": "advanced"
  },
  "updated_at": "2024-01-03T00:00:00Z"
}
```

- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Invalid or expired token
- **500 Internal Server Error**: Server error

## Session Management Endpoints

### POST /auth/refresh
Refresh authentication token

#### Headers
```
Authorization: Bearer {current_token}
```

#### Responses
- **200 OK**: Token refreshed successfully
```json
{
  "session_token": "new-jwt-token"
}
```

- **401 Unauthorized**: Invalid or expired token
- **500 Internal Server Error**: Server error

## Error Response Format

All error responses follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "specific field with error",
      "reason": "reason for the error"
    }
  }
}
```

## Common Error Codes
- `INVALID_INPUT`: Request data doesn't match validation rules
- `UNAUTHORIZED`: Authentication token is invalid or expired
- `USER_NOT_FOUND`: Requested user doesn't exist
- `EMAIL_EXISTS`: Email already registered
- `INVALID_CREDENTIALS`: Signin credentials are incorrect
- `RATE_LIMITED`: Too many requests from same source
- `INTERNAL_ERROR`: Server-side error occurred

## Security Headers
All responses should include:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`