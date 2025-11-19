from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from app.config.db import get_session
from app.services.questions import QuestionService
from app.schemas.questions import QuestionCreateRequest, QuestionUpdateRequest
from app.utils.articles import getArticle
from app.utils.errors import ArticleNotFound, InvalidAuth, InvalidArticleId

router = APIRouter(prefix="/questions", tags=["questions"])


    
@router.get("/")
def get_questions(session: Session = Depends(get_session)):
    questions = QuestionService.get_questions(session)
    return questions


@router.post("/", status_code=201)
def create_question(request: Request, question: QuestionCreateRequest, session: Session = Depends(get_session)):
    try:
        user = request.state.user
        article = getArticle(request.headers.get("Authorization", ""), question.article_id)
        
        if(article["enabled"] == False):
            raise HTTPException(status_code=400, detail="Cannot add question to a disabled article")
        
        created_question = QuestionService.create_question(session, question, user["id"])
        return created_question
    except InvalidAuth:
        raise HTTPException(status_code=401, detail="Invalid authorization")
    except InvalidArticleId:
        raise HTTPException(status_code=400, detail="Invalid article ID")
    except ArticleNotFound:
        raise HTTPException(status_code=404, detail="Article not found")
    
@router.get("/{question_id}")
def get_question(question_id: int, session: Session = Depends(get_session)):
    question = QuestionService.get_question_by_id(session, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.get("/article/{article_id}")
def get_questions_by_article(article_id: str, session: Session = Depends(get_session)):
    questions = QuestionService.get_questions_by_article(session, article_id)
    return questions

@router.put("/{question_id}")
def update_question(question_id: int, questionUpdate: QuestionUpdateRequest, session: Session = Depends(get_session)):
    updated_question = QuestionService.update_question(session, question_id, questionUpdate.text)
    if not updated_question:
        raise HTTPException(status_code=404, detail="Question not found")
    return updated_question
