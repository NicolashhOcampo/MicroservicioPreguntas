from pydantic import BaseModel

class QuestionCreateRequest(BaseModel):
    text: str
    article_id: str
    
class QuestionUpdateRequest(BaseModel):
    text: str