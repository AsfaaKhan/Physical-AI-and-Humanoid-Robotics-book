# Data Model: User Authentication with Background-Aware Personalization

**Feature**: 003-user-auth-personalization
**Created**: 2025-12-16
**Status**: Complete

## Entity: User

### Description
Core user entity managed by Better Auth but referenced in our system for profile data.

### Fields
- **user_id** (string, required): Unique identifier from Better Auth system
- **email** (string, required): User's email address, validated format
- **created_at** (datetime, required): Account creation timestamp
- **updated_at** (datetime, required): Last update timestamp
- **is_verified** (boolean, optional): Email verification status

### Relationships
- One-to-One: UserProfile (user_id → user_id)

## Entity: UserProfile

### Description
Extended user profile containing background information for personalization.

### Fields
- **user_id** (string, required): Foreign key to User entity
- **software_experience** (enum, required): ["beginner", "intermediate", "expert"]
- **programming_background** (enum, required): ["none", "basic", "intermediate", "advanced"]
- **hardware_knowledge** (enum, required): ["none", "basic", "intermediate", "advanced"]
- **created_at** (datetime, required): Profile creation timestamp
- **updated_at** (datetime, required): Last profile update timestamp
- **profile_completed** (boolean, required): Whether background info is complete

### Validation Rules
- software_experience must be one of the defined enum values
- programming_background must be one of the defined enum values
- hardware_knowledge must be one of the defined enum values
- user_id must reference an existing User
- All background fields are required during initial profile creation

### Relationships
- One-to-One: User (user_id → user_id)

## Entity: UserSession

### Description
Session management for authenticated users, tracking active sessions.

### Fields
- **session_id** (string, required): Unique session identifier
- **user_id** (string, required): Reference to authenticated user
- **token_hash** (string, required): Hashed session token for security
- **created_at** (datetime, required): Session creation timestamp
- **expires_at** (datetime, required): Session expiration timestamp
- **last_accessed** (datetime, required): Last activity timestamp
- **user_agent** (string, optional): Client information for security
- **ip_address** (string, optional): IP address for security tracking

### Validation Rules
- session_id must be unique
- expires_at must be in the future when created
- user_id must reference an existing User
- token_hash must be properly hashed using secure algorithm

### Relationships
- Many-to-One: User (user_id → user_id)

## Entity: PersonalizationLog

### Description
Optional entity to track personalization interactions for analytics and improvement.

### Fields
- **log_id** (string, required): Unique log identifier
- **user_id** (string, required): Reference to user
- **content_id** (string, required): Identifier for content that was personalized
- **background_used** (json, required): Background information used for personalization
- **timestamp** (datetime, required): When personalization occurred
- **content_version** (string, optional): Version of content served

### Validation Rules
- user_id must reference an existing User
- content_id must be non-empty
- background_used must be valid JSON with background information

### Relationships
- Many-to-One: User (user_id → user_id)

## Database Schema

### PostgreSQL Tables

```sql
-- Users table (referenced from Better Auth)
CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE
);

-- User profiles table
CREATE TABLE user_profiles (
    user_id VARCHAR(255) PRIMARY KEY REFERENCES users(user_id),
    software_experience VARCHAR(20) NOT NULL CHECK (software_experience IN ('beginner', 'intermediate', 'expert')),
    programming_background VARCHAR(20) NOT NULL CHECK (programming_background IN ('none', 'basic', 'intermediate', 'advanced')),
    hardware_knowledge VARCHAR(20) NOT NULL CHECK (hardware_knowledge IN ('none', 'basic', 'intermediate', 'advanced')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    profile_completed BOOLEAN DEFAULT FALSE
);

-- User sessions table
CREATE TABLE user_sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(user_id),
    token_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_agent TEXT,
    ip_address INET
);

-- Personalization logs table (optional)
CREATE TABLE personalization_logs (
    log_id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(user_id),
    content_id VARCHAR(255) NOT NULL,
    background_used JSONB NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    content_version VARCHAR(50)
);

-- Indexes for performance
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_expires_at ON user_sessions(expires_at);
CREATE INDEX idx_personalization_logs_user_id ON personalization_logs(user_id);
CREATE INDEX idx_personalization_logs_timestamp ON personalization_logs(timestamp);
```

## State Transitions

### User Profile State Transitions
1. **Profile Creation**: When user registers → profile_completed = false
2. **Profile Completion**: When user fills background info → profile_completed = true
3. **Profile Update**: When user updates background → updated_at updated
4. **Profile Incomplete**: When required background info is missing → profile_completed = false

### Session State Transitions
1. **Session Creation**: When user authenticates → session created with expiration
2. **Session Activity**: When user interacts → last_accessed updated
3. **Session Expiration**: When expires_at reached → session becomes invalid
4. **Session Termination**: When user signs out → session removed

## Data Validation

### Input Validation
- Email format validation using standard email regex
- Background information validation against enum values
- Session token validation and security checks
- Rate limiting to prevent abuse

### Data Integrity
- Foreign key constraints to maintain referential integrity
- Check constraints for enum value validation
- Timestamp validation to prevent invalid dates
- Unique constraints where appropriate

## Security Considerations

### Data Protection
- Passwords never stored in our system (handled by Better Auth)
- Session tokens stored as secure hashes
- Background information encrypted at rest if required
- Proper access controls for profile data

### Privacy
- User background data only used for personalization
- Clear data retention and deletion policies
- Compliance with privacy regulations
- Minimal data collection principle