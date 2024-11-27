FROM node:18-alpine AS development
ENV NODE_ENV development
# Add a work directory
WORKDIR /app
# Cache and Install dependencies
COPY package*.json .
RUN npm install
# Copy app files
COPY . .
# Expose port
EXPOSE 4000
# Start the app
CMD [ "npm", "start" ]
