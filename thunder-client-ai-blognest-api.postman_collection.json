{
  "info": {
    "name": "AI BlogNest API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "description": "Thunder Client / Postman collection for AI BlogNest API endpoints."
  },
  "item": [
    {
      "name": "Register User",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"John Doe\",\n  \"email\": \"john@example.com\",\n  \"password\": \"123456\"\n}"
        },
        "url": {"raw": "{{base_url}}/api/auth/register", "host": ["{{base_url}}"], "path": ["api", "auth", "register"]}
      }
    },
    {
      "name": "Login User",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"john@example.com\",\n  \"password\": \"123456\"\n}"
        },
        "url": {"raw": "{{base_url}}/api/auth/login", "host": ["{{base_url}}"], "path": ["api", "auth", "login"]}
      }
    },
    {
      "name": "Get Profile",
      "request": {
        "method": "GET",
        "header": [{"key": "Authorization", "value": "Bearer {{token}}"}],
        "url": {"raw": "{{base_url}}/api/auth/profile", "host": ["{{base_url}}"], "path": ["api", "auth", "profile"]}
      }
    },
    {
      "name": "Create Blog",
      "request": {
        "method": "POST",
        "header": [
          {"key": "Content-Type", "value": "application/json"},
          {"key": "Authorization", "value": "Bearer {{token}}"}
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"title\": \"My First AI Blog\",\n  \"content\": \"This is a sample AI-generated blog post content.\",\n  \"category\": \"Technology\"\n}"
        },
        "url": {"raw": "{{base_url}}/api/blogs", "host": ["{{base_url}}"], "path": ["api", "blogs"]}
      }
    },
    {
      "name": "Get All Blogs",
      "request": {
        "method": "GET",
        "url": {"raw": "{{base_url}}/api/blogs", "host": ["{{base_url}}"], "path": ["api", "blogs"]}
      }
    },
    {
      "name": "Get Blog By ID",
      "request": {
        "method": "GET",
        "url": {"raw": "{{base_url}}/api/blogs/{{blogId}}", "host": ["{{base_url}}"], "path": ["api", "blogs", "{{blogId}}"]}
      }
    },
    {
      "name": "Update Blog",
      "request": {
        "method": "PUT",
        "header": [
          {"key": "Content-Type", "value": "application/json"},
          {"key": "Authorization", "value": "Bearer {{token}}"}
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"title\": \"Updated AI Blog Title\",\n  \"content\": \"Updated content for the blog post.\",\n  \"category\": \"Education\"\n}"
        },
        "url": {"raw": "{{base_url}}/api/blogs/{{blogId}}", "host": ["{{base_url}}"], "path": ["api", "blogs", "{{blogId}}"]}
      }
    },
    {
      "name": "Delete Blog",
      "request": {
        "method": "DELETE",
        "header": [{"key": "Authorization", "value": "Bearer {{token}}"}],
        "url": {"raw": "{{base_url}}/api/blogs/{{blogId}}", "host": ["{{base_url}}"], "path": ["api", "blogs", "{{blogId}}"]}
      }
    },
    {
      "name": "Generate AI Blog",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"topic\": \"Artificial Intelligence\"\n}"
        },
        "url": {"raw": "{{base_url}}/api/ai/generate-blog", "host": ["{{base_url}}"], "path": ["api", "ai", "generate-blog"]}
      }
    },
    {
      "name": "Summarize Blog Content",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"content\": \"This is a long blog post content that needs a short summary.\"\n}"
        },
        "url": {"raw": "{{base_url}}/api/ai/summarize", "host": ["{{base_url}}"], "path": ["api", "ai", "summarize"]}
      }
    }
  ]
}
