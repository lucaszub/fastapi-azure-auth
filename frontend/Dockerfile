# Stage 1: Build the Vite app
FROM node:16-alpine AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Vite app
RUN npm run build

# Stage 2: Serve the built files using http-server
FROM node:16-alpine

# Install http-server globally
RUN npm install -g http-server

# Copy the built files from the previous stage
COPY --from=builder /app/dist /usr/share/app

# Expose port 8080
EXPOSE 8080

# Start http-server
CMD ["http-server", "/usr/share/app", "-p", "8080"]
