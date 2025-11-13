# Empire Genesis Backend

Backend API for Empire Genesis mobile game.

## Quick Start

```bash
# Install dependencies
npm install

# Start PostgreSQL and Redis
docker-compose up -d

# Copy environment variables
cp .env.example .env

# Run migrations
npm run migrate:up

# Seed database
npm run seed

# Start development server
npm run dev
```

Server will run on http://localhost:3000

## API Documentation

See `/docs/API_SPECIFICATION.md` for complete API documentation.

## Testing

```bash
npm test
```
