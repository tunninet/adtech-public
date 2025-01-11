# Use Node.js 20 (latest available) with Alpine
FROM node:20.18.1-alpine3.21 as build

# Set environment variable to avoid OpenSSL issues
ENV NODE_OPTIONS="--openssl-legacy-provider"

# Set the working directory
WORKDIR /app

# Copy the package.json file
COPY package.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the React app
RUN npm run build

# Use a minimal Node.js image to serve the app
FROM nginx:alpine

# Copy the build output to the Nginx HTML directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose the port Nginx is running on
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
