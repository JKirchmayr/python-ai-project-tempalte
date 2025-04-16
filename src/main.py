from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from openai import OpenAI
import os
import logging
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

app = FastAPI()

# Request model
class PromptRequest(BaseModel):
    user_id: str
    prompt: str

def get_or_create_session(user_id: str) -> str:
    """Get active session or create new one for user"""
    try:
        # Check for active session
        response = supabase.table("sessions") \
            .select("session_id") \
            .eq("user_id", user_id) \
            .eq("is_active", True) \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()
        
        if response.data:
            return response.data[0]["session_id"]
        
        # Create new session
        session_id = str(uuid.uuid4())
        supabase.table("sessions").insert({
            "user_id": user_id,
            "session_id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_active": datetime.utcnow().isoformat(),
            "is_active": True
        }).execute()
        
        return session_id
        
    except Exception as e:
        logger.error(f"Session error: {str(e)}")
        raise HTTPException(status_code=500, detail="Session management error")

@app.post("/chat")
async def chat(request: PromptRequest):
    try:
        # Get or create session
        session_id = get_or_create_session(request.user_id)
        
        # Update session last active time
        supabase.table("sessions") \
            .update({"last_active": datetime.utcnow().isoformat()}) \
            .eq("session_id", session_id) \
            .execute()

        # 1. Fetch conversation history
        response = supabase.table("conversations") \
            .select("*") \
            .eq("user_id", request.user_id) \
            .eq("session_id", session_id) \
            .order("created_at", desc=False) \
            .execute()
        
        history = response.data if response.data else []

        # 2. Format messages for OpenAI
        messages = [{"role": "system", "content": "You are a helpful assistant. Remember and use information from previous messages."}]
        
        # Add conversation history
        for entry in history:
            messages.append({"role": "user", "content": entry["prompt"]})
            messages.append({"role": "assistant", "content": entry["response"]})
        
        # Add current prompt
        messages.append({"role": "user", "content": request.prompt})

        # 3. Call OpenAI
        chat_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = chat_response.choices[0].message.content

        # 4. Save conversation
        supabase.table("conversations").insert({
            "user_id": request.user_id,
            "session_id": session_id,
            "prompt": request.prompt,
            "response": reply
        }).execute()

        return {"response": reply}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))