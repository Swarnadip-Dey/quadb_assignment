# Stage 1: Build the frontend app using Node.js
FROM node:16 AS build

WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Build the frontend app
RUN npm run build

# Stage 2: Set up the nginx server to serve the app
FROM nginx:alpine

# Copy the build from the previous stage into nginx's default directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose the port that nginx will run on
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
