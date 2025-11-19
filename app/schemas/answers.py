from pydantic import BaseModel

class AnswerCreateRequest(BaseModel):
    text: str
    question_id: int