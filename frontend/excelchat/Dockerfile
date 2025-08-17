# Use official Node image
FROM node:18-slim

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json first for caching
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of your app
COPY . .


RUN npm run build

# Install a simple static server to serve build (like serve)
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Command to serve the app
CMD ["serve", "-s", "build", "-l", "3000"]
