from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from app.config.db import get_session
from app.services.questions import QuestionService
from app.schemas.questions import QuestionCreateRequest, QuestionUpdateRequest
from app.utils.articles import getArticle
from app.utils.errors import ArticleNotFoundError, ArticleDisabledError, InvalidAuthError, InvalidArticleIdError, QuestionNotFoundError, QuestionDisabledError, QuestionAlreadyAnsweredError, QuestionForbiddenError

router = APIRouter(prefix="/questions", tags=["questions"])


    
@router.get("/")
def get_questions(session: Session = Depends(get_session)):
    questions = QuestionService.get_questions(session)
    return questions


@router.post("/", status_code=201)
def create_question(request: Request, question: QuestionCreateRequest, session: Session = Depends(get_session)):
    try:
        user = request.state.user
        token = request.headers.get("Authorization", "")        
        
        created_question = QuestionService.create_question(session, question, user["id"], token)
        return created_question
    
    except InvalidAuthError:
        raise HTTPException(status_code=401, detail="Invalid authorization")
    except InvalidArticleIdError:
        raise HTTPException(status_code=400, detail="Invalid article ID")
    except ArticleNotFoundError:
        raise HTTPException(status_code=404, detail="Article not found")
    except ArticleDisabledError:
        raise HTTPException(status_code=400, detail="Cannot add question to a disabled article")
    
@router.get("/{question_id}")
def get_question(question_id: int, session: Session = Depends(get_session)):
    try:
        question = QuestionService.get_question_by_id(session, question_id)
        return question
    except QuestionNotFoundError:
        raise HTTPException(status_code=404, detail="Question not found")

@router.get("/article/{article_id}")
def get_questions_by_article(article_id: str, session: Session = Depends(get_session)):
    questions = QuestionService.get_questions_by_article(session, article_id)
    return questions

@router.put("/{question_id}")
def update_question(request:Request, question_id: int, questionUpdate: QuestionUpdateRequest, session: Session = Depends(get_session)):
    try:
        user = request.state.user
        updated_question = QuestionService.update_question(session, question_id, questionUpdate.text, user["id"])
        return updated_question
    except QuestionNotFoundError:
        raise HTTPException(status_code=404, detail="Question not found")
    except QuestionDisabledError:
        raise HTTPException(status_code=400, detail="Question is disabled")
    except QuestionAlreadyAnsweredError:
        raise HTTPException(status_code=400, detail="Question has already been answered")
    except QuestionForbiddenError:
        raise HTTPException(status_code=403, detail="Not authorized to update this question")