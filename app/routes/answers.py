from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from app.config.db import get_session
from app.services.answers import AnswerService
from app.services.questions import QuestionService
from app.schemas.answers import AnswerCreateRequest
from app.utils.articles import getArticle
from app.utils.errors import AnswerNotFoundError, ArticleNotFoundError, InvalidAuthError, InvalidArticleIdError, QuestionDisabledError, NotAuthorizedToAnswerError, QuestionNotFoundError, QuestionAlreadyAnsweredError
from app.models import Answer


router = APIRouter(prefix="/answers", tags=["answers"])

@router.post("/", status_code=201, response_model=Answer)
def create_answer(request: Request, answer: AnswerCreateRequest, session: Session = Depends(get_session)):
    try:
        user = request.state.user
        token = request.headers.get("Authorization", "")        
        answer_created = AnswerService.create_answer(session, answer, user["id"], token)
        return answer_created
    
    except InvalidAuthError:
        raise HTTPException(status_code=401, detail="Invalid authorization")
    except InvalidArticleIdError:
        raise HTTPException(status_code=400, detail="Invalid article ID")
    except ArticleNotFoundError:
        raise HTTPException(status_code=404, detail="Article not found")
    except QuestionNotFoundError:
        raise HTTPException(status_code=404, detail="Question not found")
    except QuestionDisabledError:
        raise HTTPException(status_code=400, detail="Cannot answer a disabled question")
    except NotAuthorizedToAnswerError:
        raise HTTPException(status_code=403, detail="Not authorized to answer this question")
    except QuestionAlreadyAnsweredError:
        raise HTTPException(status_code=400, detail="Question has already been answered")
    
@router.get("/")
def get_answers(session: Session = Depends(get_session)):
    answers = AnswerService.get_answers(session)
    return answers

@router.get("/{answer_id}")
def get_answer(answer_id: int, session: Session = Depends(get_session)):
    try:
        answer = AnswerService.get_answer_by_id(session, answer_id)
        return answer
    except AnswerNotFoundError:
        raise HTTPException(status_code=404, detail="Answer not found")
    
@router.get("/question/{question_id}")
def get_answer_by_question(question_id: int, session: Session = Depends(get_session)):
    try:
        answer = AnswerService.get_answer_by_question(session, question_id)
        return answer
    except AnswerNotFoundError:
        raise HTTPException(status_code=404, detail="Answer not found")