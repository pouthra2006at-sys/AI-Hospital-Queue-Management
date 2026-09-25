# AI BlogNest API

AI BlogNest API is a RESTful backend built with Node.js, Express, MongoDB, Mongoose, JWT authentication, bcrypt, and Gemini-powered AI content generation.

## Features

- User registration and login
- JWT-protected routes
- Blog creation, reading, updating, deleting
- AI blog content generation
- AI summarization
- MVC architecture

## Getting Started

1. Copy `.env.example` to `.env`
2. Install dependencies:

```bash
npm install
```

3. Start the app:

```bash
npm run dev
```

## Environment Variables

- `PORT`
- `MONGO_URI`
- `JWT_SECRET`
- `GEMINI_API_KEY`
- `GEMINI_MODEL`

## API Endpoints

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/profile`

### Blogs
- `POST /api/blogs`
- `GET /api/blogs`
- `GET /api/blogs/:id`
- `PUT /api/blogs/:id`
- `DELETE /api/blogs/:id`

### AI
- `POST /api/ai/generate-blog`
- `POST /api/ai/summarize`

## Testing with Thunder Client

Use the above endpoints in Thunder Client or Postman with JSON body payloads.

Example request bodies are included in the repository documentation.
