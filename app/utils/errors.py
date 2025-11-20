class InvalidAuthError(Exception):
    pass

class ArticleNotFoundError(Exception):
    pass

class ArticleDisabledError(Exception):
    pass

class InvalidArticleIdError(Exception):
    pass

class QuestionNotFoundError(Exception):
    pass

class QuestionDisabledError(Exception):
    pass

class QuestionAlreadyAnsweredError(Exception):
    pass

class QuestionForbiddenError(Exception):
    pass

class NotAuthorizedToAnswerError(Exception):
    pass

class AnswerNotFoundError(Exception):
    pass