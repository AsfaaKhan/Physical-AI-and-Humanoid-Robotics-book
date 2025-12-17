# Quickstart Guide: User Authentication with Background-Aware Personalization

**Feature**: 003-user-auth-personalization
**Created**: 2025-12-16

## Overview
This guide provides a quick setup and usage guide for the authentication system with background-aware personalization. The system allows users to register, sign in, and provide background information to enable personalized content experiences.

## Prerequisites
- Python 3.9+ installed
- PostgreSQL database (Neon Serverless recommended)
- Better Auth service configured
- Node.js for frontend development (Docusaurus)

## Environment Setup

### Backend Environment Variables
Create a `.env` file in the backend directory:

```bash
# Better Auth Configuration
BETTER_AUTH_URL=https://your-better-auth-instance.com
BETTER_AUTH_SECRET=your-better-auth-secret

# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database_name

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-here

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000
```

### Database Setup
1. Ensure PostgreSQL is running
2. Create the required tables using the schema from `data-model.md`
3. Run the migration scripts (to be created in implementation)

## Backend Setup

### 1. Install Dependencies
```bash
cd backend
pip install fastapi uvicorn python-multipart python-jose[cryptography] passlib[bcrypt] psycopg2-binary httpx python-dotenv
```

### 2. Start the Development Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

### 3. API Documentation
- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## Frontend Integration

### 1. Environment Configuration
Add to your Docusaurus `.env` file:
```bash
REACT_APP_AUTH_API_URL=http://localhost:8000/api/v1
```

### 2. Authentication Context Setup
```javascript
// Example React Context for authentication
import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Implementation details for signup, signin, etc.
  // Will be developed during implementation phase
};
```

## API Usage Examples

### 1. User Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "background": {
      "software_experience": "intermediate",
      "programming_background": "basic",
      "hardware_knowledge": "intermediate"
    }
  }'
```

### 2. User Sign In
```bash
curl -X POST http://localhost:8000/api/v1/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### 3. Get User Profile
```bash
curl -X GET http://localhost:8000/api/v1/auth/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 4. Update User Profile
```bash
curl -X PUT http://localhost:8000/api/v1/auth/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "background": {
      "software_experience": "expert",
      "programming_background": "intermediate",
      "hardware_knowledge": "advanced"
    }
  }'
```

## Frontend Integration Example

### 1. Signup Component
```jsx
import React, { useState } from 'react';
import { useAuth } from './AuthContext';

const SignupForm = () => {
  const { signup } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    software_experience: 'beginner',
    programming_background: 'none',
    hardware_knowledge: 'none'
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await signup(formData);
      // Handle successful signup
    } catch (error) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={formData.email}
        onChange={(e) => setFormData({...formData, email: e.target.value})}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={formData.password}
        onChange={(e) => setFormData({...formData, password: e.target.value})}
        placeholder="Password"
        required
      />
      {/* Background information selects */}
      <select
        value={formData.software_experience}
        onChange={(e) => setFormData({...formData, software_experience: e.target.value})}
      >
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="expert">Expert</option>
      </select>
      {/* Similar selects for programming_background and hardware_knowledge */}
      <button type="submit">Sign Up</button>
    </form>
  );
};
```

### 2. Protected Content Component
```jsx
import React from 'react';
import { useAuth } from './AuthContext';

const PersonalizedContent = ({ content }) => {
  const { user } = useAuth();

  if (!user) {
    return (
      <div>
        <p>Sign up to see personalized content based on your background!</p>
        {/* Sign up prompt */}
      </div>
    );
  }

  // Adjust content based on user background
  const adjustedContent = adjustContentForBackground(content, user.background);

  return <div>{adjustedContent}</div>;
};
```

## Testing the System

### 1. Unit Tests
Run backend tests:
```bash
cd backend
python -m pytest tests/
```

### 2. Integration Tests
Test the full authentication flow:
1. Register a new user with background information
2. Sign in with the new credentials
3. Verify profile information is accessible
4. Update profile information and verify changes

### 3. Frontend Tests
Test React components with Jest and React Testing Library:
```bash
cd book
npm test
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify `DATABASE_URL` is correct
   - Check that PostgreSQL is running
   - Ensure database credentials are valid

2. **Authentication Failures**
   - Verify Better Auth configuration
   - Check that JWT_SECRET matches between services
   - Ensure proper CORS settings

3. **Background Information Not Saving**
   - Verify enum values match expected values
   - Check that all required fields are provided

### Debugging Tips
- Enable detailed logging in development: `LOG_LEVEL=DEBUG`
- Check API response codes and error messages
- Verify environment variables are loaded correctly
- Use API documentation at `/docs` to test endpoints

## Next Steps

1. Complete the full implementation following the plan in `plan.md`
2. Set up proper error handling and validation
3. Implement comprehensive security measures
4. Add monitoring and logging
5. Deploy to production environment