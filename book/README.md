# Physical AI & Humanoid Robotics Book

This Docusaurus-based book provides comprehensive coverage of Physical AI and Humanoid Robotics, covering topics from ROS2 fundamentals to Vision-Language-Action systems.

## Prerequisites

- Node.js (version 18 or higher)
- npm or yarn package manager

## Installation

1. Navigate to the book directory:
```bash
cd book
```

2. Install dependencies:
```bash
npm install
```
Or if you prefer using yarn:
```bash
yarn
```

## Local Development

1. Start the development server:
```bash
npm start
```
Or with yarn:
```bash
yarn start
```

This command starts a local development server and opens a browser window. Most changes are reflected live without having to restart the server.

## Build

To build the static site for production:

```bash
npm run build
```
Or with yarn:
```bash
yarn build
```

The static files will be generated in the `build/` folder.

## Deployment

The site can be deployed to various platforms:

### GitHub Pages
1. Configure the deployment settings in `docusaurus.config.js`
2. Use the `deploy` script to build and deploy:
```bash
npm run deploy
```
Or with yarn:
```bash
yarn deploy
```

### Other Platforms
The built static files in the `build/` directory can be deployed to any static hosting service.

## Project Structure

- `/docs`: Contains all the book content organized by modules
- `/src`: Custom React components and site-specific code
- `/static`: Static assets like images
- `docusaurus.config.js`: Site configuration
- `sidebars.ts`: Navigation sidebar configuration
- `package.json`: Project dependencies and scripts

## Available Scripts

- `npm start` or `yarn start`: Start local development server
- `npm run build` or `yarn build`: Build static site for production
- `npm run serve` or `yarn serve`: Serve the built site locally for testing
- `npm run deploy` or `yarn deploy`: Deploy to configured platform (e.g., GitHub Pages)

## Book Content Overview

This book covers four main modules:

1. **Module 1: ROS2** - The Robotic Nervous System
2. **Module 2: Simulation (Gazebo & Unity)** - The Digital Twin
3. **Module 3: NVIDIA Isaac** - The AI-Robot Brain
4. **Module 4: Vision-Language-Action (VLA)** - Vision-Language-Action systems

Plus a comprehensive capstone project on autonomous humanoid development.

## Contributing

To add new content:
1. Create a new markdown file in the appropriate `/docs` subdirectory
2. Add the file to the sidebar configuration in `sidebars.ts`
3. Use Docusaurus markdown features for enhanced content

## Troubleshooting

If you encounter issues:
1. Make sure all dependencies are installed: `npm install` or `yarn`
2. Clear cache if needed: `npm run clear` or `yarn clear`
3. Check the Docusaurus documentation for additional help
