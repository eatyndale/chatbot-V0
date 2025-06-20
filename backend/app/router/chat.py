from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User as UserModel
from app.services import auth_service, llm_handler, chat_service
from app.models.chat import ChatMessageRequest, ChatMessageResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/message", response_model=ChatMessageResponse)
def post_message(
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(auth_service.get_current_user)
):
    # Get or create the conversation
    conversation = chat_service.get_or_create_conversation(
        db, user_id=current_user.id, conversation_id=request.conversation_id
    )
    
    # Get conversation history
    history = chat_service.get_conversation_history(db, conversation.id)
    
    # Add user's message to history
    chat_service.add_message_to_history(db, conversation.id, "user", request.message)
    
    # Get LLM response
    llm_reply = llm_handler.get_llm_response(request.message, history)
    
    # Add LLM's reply to history
    chat_service.add_message_to_history(db, conversation.id, "assistant", llm_reply)
    
    return ChatMessageResponse(reply=llm_reply, conversation_id=conversation.id)
