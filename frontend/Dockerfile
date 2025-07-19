# Multi-stage Dockerfile for Therapist Bot Frontend
# Optimized for production deployment with Nginx

# ===============================================
# Stage 1: Build Stage
# ===============================================
FROM node:18-alpine as builder

# Set working directory
WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install all dependencies (including devDependencies for build)
RUN npm ci && npm cache clean --force

# Copy source code
COPY . .

# Build the application
RUN npm run build

# ===============================================
# Stage 2: Production Stage with Nginx
# ===============================================
FROM nginx:alpine as runtime

# Install additional packages for health checks
RUN apk add --no-cache curl

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Set proper permissions for existing nginx user
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d

# Touch and set permissions for nginx.pid
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# Switch to existing nginx user
USER nginx

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

# ===============================================
# Build Information
# ===============================================
LABEL maintainer="Therapist Bot Team" \
      description="CBT Therapist Bot Frontend - React TypeScript with session awareness" \
      version="1.0.0" \
      node.version="18" \
      nginx.version="alpine"