from sqlmodel import Session, select
from app.models import Question
from app.schemas.questions import QuestionCreateRequest
from app.utils.errors import QuestionNotFoundError, QuestionDisabledError, QuestionAlreadyAnsweredError, QuestionForbiddenError, ArticleDisabledError, ArticleNotFoundError
from app.utils.articles import getArticle

class QuestionService:
    
    @staticmethod
    def create_question(session: Session, question_data: QuestionCreateRequest, user_id: str, token: str):
        
        article = getArticle(token, question_data.article_id)
        
        
        if(article["enabled"] == False):
            raise ArticleDisabledError()
        
        new_question = Question(
            text=question_data.text,
            user_id=user_id,
            article_id=question_data.article_id
        )
        session.add(new_question)
        session.commit()
        session.refresh(new_question)
        return new_question
    
    @staticmethod
    def get_questions(session: Session):
        statement = select(Question)
        results = session.exec(statement)
        return results.all()
    
    @staticmethod
    def get_question_by_id(session: Session, question_id: int):
        question = session.get(Question, question_id)
        if question is None:
            raise QuestionNotFoundError()
        return question
    
    @staticmethod
    def get_questions_by_article(session: Session, article_id: str):
        statement = select(Question).where(Question.article_id == article_id)
        results = session.exec(statement)
        return results.all()
    
    @staticmethod
    def update_question(session: Session, question_id: int, new_text: str, user_id: str):
        question = session.get(Question, question_id)
        if question is None:
            raise QuestionNotFoundError()
        
        if not question.enabled:
            raise QuestionDisabledError()
        
        if question.answer is not None:
            raise QuestionAlreadyAnsweredError()
        
        if question.user_id != user_id:
            raise QuestionForbiddenError()
        
        question.text = new_text
        session.commit()
        session.refresh(question)
        return question
    
    @staticmethod
    def delete_questions_by_article(session: Session, article_id: str):
        statement = select(Question).where(Question.article_id == article_id)
        results = session.exec(statement)
        questions = results.all()
        for question in questions:
            question.enabled = False
            session.add(question)
        session.commit()