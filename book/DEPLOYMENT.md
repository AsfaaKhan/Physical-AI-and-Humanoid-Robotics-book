# Deployment Guide

This guide explains how to deploy the Docusaurus-based book with the RAG chatbot to GitHub Pages.

## Prerequisites

- Node.js (version >= 18.0)
- Git
- GitHub account
- A GitHub repository for the project

## Environment Configuration

Before building for production, configure the environment variables:

1. Copy `.env` file and customize for production:
   ```bash
   cp .env .env.production
   ```

2. Update the `REACT_APP_CHATBOT_API_URL` in `.env.production` to point to your production backend API:
   ```env
   REACT_APP_CHATBOT_API_URL=https://your-production-backend.com
   ```

## GitHub Pages Deployment

### Method 1: Using GitHub Actions (Recommended)

1. Create a `.github/workflows/deploy.yml` file in your repository:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    name: Deploy to GitHub Pages
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: yarn

      - name: Install dependencies
        run: |
          cd book
          yarn install --frozen-lockfile
      - name: Build website
        run: |
          cd book
          yarn build

      # Popular action to deploy to GitHub Pages:
      # Docs: https://github.com/peaceiris/actions-gh-pages#%EF%B8%8F-docusaurus
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          # Build output to publish to the `gh-pages` branch:
          publish_dir: ./book/build
```

### Method 2: Manual Deployment

1. Set the correct environment variables:
   ```bash
   cd book
   export REACT_APP_CHATBOT_API_URL=https://your-production-backend.com
   ```

2. Build the site:
   ```bash
   yarn build
   # or
   npm run build
   ```

3. Deploy using the Docusaurus command:
   ```bash
   GIT_USER=<Your GitHub username> yarn deploy
   ```

## Configuration Notes

- The `baseUrl` in `docusaurus.config.ts` should match your repository name: `/repository-name/`
- The `organizationName` and `projectName` in `docusaurus.config.ts` should match your GitHub account and repository
- The backend API must be accessible from the deployed site (CORS configured)
- For security reasons, avoid hardcoding API keys in the frontend

## Backend API Considerations

For the chatbot to work in production:

1. Ensure your backend API is deployed and accessible
2. Configure CORS to allow requests from your GitHub Pages URL
3. Set up proper authentication if required
4. Ensure the backend API is secured and rate-limited appropriately

## Troubleshooting

### Common Issues

- **CORS errors**: Ensure your backend API allows requests from your GitHub Pages domain
- **API URL issues**: Verify `REACT_APP_CHATBOT_API_URL` is set correctly for production
- **Base URL issues**: Check that `baseUrl` in `docusaurus.config.ts` matches your GitHub Pages path

### Debugging Production Build

To test the production build locally:
```bash
cd book
yarn build
yarn serve
```

Visit `http://localhost:3000` to test the production build locally.