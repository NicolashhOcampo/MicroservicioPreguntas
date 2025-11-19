from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from app.config.db import get_session
from app.services.answers import AnswerService
from app.services.questions import QuestionService
from app.schemas.answers import AnswerCreateRequest
from app.utils.articles import getArticle
from app.utils.errors import ArticleNotFound, InvalidAuth, InvalidArticleId

router = APIRouter(prefix="/answers", tags=["answers"])

@router.post("/", status_code=201)
def create_answer(request: Request, answer: AnswerCreateRequest, session: Session = Depends(get_session)):
    try:
        user = request.state.user
        question = QuestionService.get_question_by_id(session, answer.question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        if question.enabled == False:
            raise HTTPException(status_code=400, detail="Cannot answer a disabled question")
    
        article = getArticle(request.headers.get("Authorization", ""), question.article_id)
        print(article)
        if(article["userId"] != user["id"]):
            print("Article userId:", article["userId"])
            print("Request userId:", user["id"])
            raise HTTPException(status_code=403, detail="Not authorized to answer this question")
        
        answer_created = AnswerService.create_answer(session, answer, user["id"])
        return answer_created
    
    except InvalidAuth:
        raise HTTPException(status_code=401, detail="Invalid authorization")
    except InvalidArticleId:
        raise HTTPException(status_code=400, detail="Invalid article ID")
    except ArticleNotFound:
        raise HTTPException(status_code=404, detail="Article not found")
    
@router.get("/")
def get_answers(session: Session = Depends(get_session)):
    answers = AnswerService.get_answers(session)
    return answers

@router.get("/{answer_id}")
def get_answer(answer_id: int, session: Session = Depends(get_session)):
    answer = AnswerService.get_answer_by_id(session, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer