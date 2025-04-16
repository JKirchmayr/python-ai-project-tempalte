# Chatbot Backend with Session Management

A FastAPI-based chatbot backend that provides:

- OpenAI GPT integration
- Session management with Supabase
- Conversation history tracking
- Stateless API design

## Features

- Maintains conversation context across messages
- Session timeout management (30-minute default)
- Secure response format (no user IDs exposed)
- Database integration with Supabase

## Setup

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:

```
OPENAI_API_KEY=your_openai_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## API Endpoints

### POST /chat

Send a message to the chatbot.

Request:

```json
{
  "user_id": "user-uuid",
  "prompt": "Your message here"
}
```

Response:

```json
{
  "response": "Assistant's reply",
  "session_id": "session-uuid",
  "timestamp": "2024-03-14T20:30:07.123456+00:00"
}
```

## Testing

Run the test script:

```bash
python src/test_chatbot.py
```

## Database Schema

### Sessions Table

- session_id (UUID, primary key)
- user_id (UUID)
- created_at (timestamp with timezone)
- last_active (timestamp with timezone)
- is_active (boolean)

### Conversations Table

- id (UUID, primary key)
- user_id (UUID)
- session_id (UUID)
- prompt (text)
- response (text)
- created_at (timestamp with timezone)
