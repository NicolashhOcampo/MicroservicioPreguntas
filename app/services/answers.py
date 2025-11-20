from sqlmodel import Session, select
from app.models import Answer
from app.schemas.answers import AnswerCreateRequest
from app.utils.errors import AnswerNotFoundError, QuestionNotFoundError, QuestionDisabledError, NotAuthorizedToAnswerError, QuestionAlreadyAnsweredError
from app.utils.articles import getArticle
from app.services.questions import QuestionService
class AnswerService:
    
    @staticmethod
    def create_answer(session: Session, answer_data: AnswerCreateRequest, user_id: str, token: str):
        
        question = QuestionService.get_question_by_id(session, answer_data.question_id)
        if not question:
            raise QuestionNotFoundError()
        
        if not question.enabled:
            raise QuestionDisabledError()

        if question.answer is not None:
            raise QuestionAlreadyAnsweredError()
        
        article = getArticle(token, question.article_id)

        if article["userId"] != user_id:
            raise NotAuthorizedToAnswerError()

        new_answer = Answer(
            text=answer_data.text,
            user_id=user_id,
            question_id=answer_data.question_id
        )

        session.add(new_answer)
        session.commit()
        session.refresh(new_answer)
        return new_answer

    @staticmethod
    def get_answers(session: Session):
        statement = select(Answer)
        results = session.exec(statement)
        return results.all()

    @staticmethod
    def get_answer_by_id(session: Session, answer_id: int):
        answer = session.get(Answer, answer_id)
        if answer is None:
            raise AnswerNotFoundError()
        return answer

    @staticmethod
    def get_answers_by_question(session: Session, question_id: int):
        statement = select(Answer).where(Answer.question_id == question_id)
        results = session.exec(statement)
        return results.first()
    