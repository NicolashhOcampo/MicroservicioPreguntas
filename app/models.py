from sqlmodel import SQLModel, Field, Relationship

class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str = Field(nullable=False, description="Question text")
    user_id: str = Field(nullable=False, description="User who created the question")
    article_id: str = Field(nullable=False, description="Article ID associated with the question")
    answer: "Answer" = Relationship(back_populates="question")
    enabled: bool = Field(default=True, description="Indicates if the question is enabled")

class Answer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str = Field(nullable=False, description="Answer text")
    user_id: str = Field(nullable=False, description="User who created the answer")
    question_id: int = Field(foreign_key="question.id")
    question: Question | None = Relationship(back_populates="answer")
    enabled: bool = Field(default=True, description="Indicates if the answer is enabled")