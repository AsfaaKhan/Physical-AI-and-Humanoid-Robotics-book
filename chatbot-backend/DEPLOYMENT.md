# Deployment Guide for Physical AI & Humanoid Robotics RAG Chatbot

This guide provides instructions for deploying the RAG chatbot system to various platforms.

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   FastAPI        │───▶│   Qdrant        │
│   (Docusaurus)  │    │   Backend        │    │   Vector DB     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                       ┌──────────────────┐
                       │   PostgreSQL     │
                       │   (Neon)         │
                       └──────────────────┘
```

## Deployment Options

### Option 1: Local Development

1. **Prerequisites:**
   - Python 3.11+
   - Docker and Docker Compose
   - OpenAI API key

2. **Setup:**
   ```bash
   # Clone the repository
   git clone <your-repo-url>
   cd chatbot-backend

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Environment Configuration:**
   ```bash
   # Copy and edit environment variables
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

4. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

5. **Access the API:**
   - API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

### Option 2: Deploy to Render

1. **Create a Render account** at [https://render.com](https://render.com)

2. **Create a new Web Service:**
   - Connect to your GitHub repository
   - Choose the `chatbot-backend` directory
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables:**
   - OPENAI_API_KEY
   - DATABASE_URL (connect to Neon PostgreSQL)
   - SECRET_KEY
   - QDRANT_URL (if using Qdrant Cloud)

4. **For Qdrant, create a separate Web Service** using the official Qdrant image

### Option 3: Deploy to Railway

1. **Create a Railway account** at [https://railway.app](https://railway.app)

2. **Deploy from GitHub:**
   - Connect your GitHub account
   - Select your repository
   - Choose the `chatbot-backend` directory

3. **Set Environment Variables:**
   - OPENAI_API_KEY
   - DATABASE_URL
   - SECRET_KEY
   - QDRANT_URL (if using cloud)

4. **Add a PostgreSQL database** from the Marketplace

### Option 4: Deploy to Fly.io

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login and create app:**
   ```bash
   fly auth login
   fly launch
   ```

3. **Deploy:**
   ```bash
   fly deploy
   ```

4. **Set secrets:**
   ```bash
   fly secrets set OPENAI_API_KEY=your_key_here
   fly secrets set SECRET_KEY=your_secret_here
   ```

## Service Configuration

### Neon PostgreSQL Setup

1. **Create a Neon account** at [https://neon.tech](https://neon.tech)
2. **Create a new project**
3. **Get the connection string** from Project Settings
4. **Use in your environment as DATABASE_URL**

### Qdrant Setup

You can use either:
- **Local Qdrant** (via Docker Compose)
- **Qdrant Cloud** (for production)

If using Qdrant Cloud:
1. Create an account at [https://cloud.qdrant.io](https://cloud.qdrant.io)
2. Create a cluster
3. Get the URL and API key
4. Use in environment variables

## Environment Variables

Required:
- `OPENAI_API_KEY` - Your OpenAI API key
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key

Optional:
- `QDRANT_URL` - Qdrant cloud URL (omit for local)
- `QDRANT_API_KEY` - Qdrant API key (if using cloud)
- `QDRANT_HOST` - Qdrant host (default: localhost)
- `QDRANT_PORT` - Qdrant port (default: 6333)
- `EMBEDDING_MODEL` - Embedding model (default: text-embedding-ada-002)
- `AGENT_MODEL` - Agent model (default: gpt-4o)
- `API_HOST` - API host (default: 0.0.0.0)
- `API_PORT` - API port (default: 8000)
- `DEBUG` - Debug mode (default: false)

## CORS Configuration

For production, update the CORS settings in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Frontend Integration

The chatbot widget is automatically integrated into all Docusaurus pages through the Layout override in `src/theme/Layout.js`.

## Health Checks

The API provides a health endpoint at:
- `GET /api/v1/health`

## API Endpoints

- `POST /api/v1/ask` - Ask questions about the book
- `POST /api/v1/embed` - Embed documents into the vector store
- `GET /api/v1/health` - Health check
- `POST /api/v1/chat-history` - Save chat history

## Scaling Recommendations

1. **Database:** Use Neon's autoscaling features
2. **Vector Store:** Qdrant handles scaling automatically
3. **API:** Deploy multiple instances behind a load balancer
4. **Frontend:** Serve through CDN (GitHub Pages for Docusaurus)

## Security Best Practices

1. **Never commit .env files** to version control
2. **Use strong, unique API keys**
3. **Enable HTTPS** in production
4. **Implement rate limiting** (built into the API)
5. **Monitor API usage** regularly
6. **Rotate keys** periodically

## Troubleshooting

### Common Issues

1. **Database Connection Errors:**
   - Check `DATABASE_URL` format
   - Verify database credentials

2. **Qdrant Connection Errors:**
   - Check Qdrant URL and API key
   - Verify network connectivity

3. **OpenAI API Errors:**
   - Check API key validity
   - Verify account billing status

4. **Embedding Errors:**
   - Ensure documents are accessible
   - Check file formats are supported

### Logs

Check application logs:
- Local: Console output from `docker-compose logs`
- Render/Railway: Dashboard logs
- Fly.io: `fly logs`

## Monitoring

Monitor these key metrics:
- API response times
- Error rates
- Database connection pool usage
- Vector store query performance
- OpenAI API usage

## Updating the System

1. **Pull latest code:**
   ```bash
   git pull origin main
   ```

2. **Update dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Redeploy** using your chosen platform's update process

## Rollback Procedure

If issues occur after deployment:
1. Keep a backup of the previous working version
2. Use platform-specific rollback features (available on most platforms)
3. Revert to the previous deployment version

## Cost Estimation

Estimated monthly costs (varies by usage):
- **OpenAI API:** $20-200+ depending on usage
- **Neon PostgreSQL:** $5-50 depending on plan
- **Qdrant Cloud:** $10-100 depending on plan
- **Hosting (Render/Railway/Fly):** $5-50 depending on plan
- **Total estimated:** $40-400/month

## Support

For issues with deployment, check:
1. The platform-specific documentation
2. The application logs
3. The API documentation at `/docs`
4. Open an issue in the repository