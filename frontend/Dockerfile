# Use official Node.js image from DockerHub
FROM node:16

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of your application files
COPY . .

# Expose the React app port (default: 3000)
EXPOSE 3000

# Run the React app
CMD ["npm", "start"]
