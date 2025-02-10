# Step 1: Build stage - Using Node.js to build the frontend
FROM node:16 AS build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) to install dependencies
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend application code
COPY frontend/ .

# Build the frontend application for production
RUN npm run build

# Step 2: Production stage - Using Nginx to serve the built frontend
FROM nginx:alpine

# Copy the built application from the build stage into the Nginx directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for the web server
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
