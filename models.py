import random
from resources import Resources
import string
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime

from config import Config

### SQLAlchemy INIT  ###

from sqlalchemy import create_engine
from sqlalchemy.orm import column_property, relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

#########################


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    chatId = Column(Integer, unique=True, primary_key=True)

    admin = Column(Boolean, default=False, nullable=False)
    banned = Column(Boolean, default=False, nullable=False)

    name = Column(String(50))
    surname = Column(String(50))
    email = Column(String(50))
    nickname = Column(String(50))
    age = Column(Integer)
    city = Column(String(50))
    school = Column(String(50))
    grade = Column(Integer)

    signUpStage = Column(Integer)

    def signUpUser(self) -> None:
        session.add(self)
        session.commit()

    def deleteUser(self) -> None:
        session.delete(self)
        session.commit()

    def toAdmin(self) -> None:
        self.is_admin = True
        session.commit()

    def isAdmin(self) -> bool:
        return self.admin

    def ban(self) -> None:
        self.banned = True
        session.commit()

    def unban(self) -> None:
        self.banned = True
        session.commit()

    def isBanned(self) -> bool:
        return self.banned


def findUserByChatID(chatId: int) -> User:
    found = session.query(User).filter(User.chatId == chatId)
    if found:
        return found.first()
    else:
        return None


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)

    name = Column(String)
    description = Column(String)
    value = Column(Integer)
    category = Column(String)

    visible = Column(Boolean, default=True)

    flag = Column(String(50))

    def addTask(self) -> None:
        session.add(self)
        session.commit()

    def deleteTask(self) -> None:
        session.delete(self)
        session.commit()

    def isVisible(self) -> bool:
        return self.visible

    def makeVisible(self) -> None:
        self.visible = True
        session.commit()

    def makeInvisible(self) -> None:
        self.visible = False
        session.commit()

    def changeValue(self, val: int) -> None:
        self.value = val
        self.commit()


def getAllTasks() -> list[Task]:
    return session.query(Task).all()


def getTasksCallback() -> list[str]:
    return [
        Resources.TASK_CALLBACK_FORMAT.format(t.category, t.name) for t in getAllTasks()
    ]


def getCategories() -> list[str]:
    tasks = session.query(Task).distinct(Task.category).all()
    return [task.category for task in tasks]


def getCategoriesCallback() -> list[str]:
    return [Resources.CATEGORY_CALLBACK_FORMAT.format(ctg) for ctg in getCategories()]


def getTasksByCategory(category: str) -> list[Task]:
    tasks = session.query(Task).filter(Task.category == category).all()
    return tasks


def getTaskByNameCategory(name: str, category: str) -> Task:
    task = (
        session.query(Task)
        .filter(Task.category == category)
        .filter(Task.name == name)
        .first()
    )
    return task


class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)

    attempt = Column(String(50))

    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    task = relationship("Task", foreign_keys=[task_id], lazy="select")
    user = relationship("User", foreign_keys=[user_id], lazy="select")

    def add(self) -> None:
        session.add(self)
        if self.attempt == self.task.flag:
            solve = Solve()
            solve.solved(self)
        session.add(self)
        session.commit()


class Solve(Submission):
    __tablename__ = "solves"

    id = Column(
        None,
        ForeignKey("submissions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    task_id = column_property(
        Column(Integer, ForeignKey(
            "tasks.id", ondelete="CASCADE"), nullable=False),
        Submission.task_id,
    )

    user_id = column_property(
        Column(Integer, ForeignKey(
            "users.id", ondelete="CASCADE"), nullable=False),
        Submission.user_id,
    )

    task = relationship("Task", foreign_keys=[task_id], lazy="select")
    user = relationship("User", foreign_keys=[user_id], lazy="select")

    def solved(self, subm: Submission) -> None:
        self.task_id = subm.task_id
        self.user_id = subm.user_id
        self.date = subm.date

        session.add(self)
        session.commit()


def getUserSolves(user: User) -> list[Solve]:
    solves = session.query(Solve).filter(Solve.user_id == user.id)
    return solves.all()


def getUserScore(user: User) -> int:
    solves = getUserSolves(user)
    score = sum([solve.Task.score for solve in solves])
    return score


def getSolvedInCategory(user: User, category: str) -> list[Solve]:
    return [solve for solve in getUserSolves(user) if solve.category == category]


def getCategoriesSolvedAll(user: User) -> list[tuple]:
    # returns list of triples (category, solved_cnt, all_cnt)
    res = list()
    categories = getCategories()
    for ctg in categories:
        solved = len(getSolvedInCategory(user, ctg))
        all = len(getTasksByCategory(ctg))
        res.append((ctg, solved, all))

    return res


def solved(user: User, task: Task) -> bool:
    userSolves = getUserSolves(user)
    return any(solution.task_id == Task.id for solution in userSolves)


def submit(user: User, task: Task, flag: str) -> None:
    # Task solved already
    if solved(user, task):
        return

    sumb = Submission(task_id=task.id, user_id=user.id, attempt=flag)

    sumb.add()


def randTasks(n: int) -> None:
    for _ in range(n):
        name = "".join(random.choices(string.ascii_letters, k=10))
        description = name
        value = 10
        category = random.choice(string.ascii_lowercase[:5])
        flag = name

        t = Task(
            name=name,
            description=description,
            value=value,
            category=category,
            flag=flag,
        )

        t.addTask()


Base.metadata.create_all(engine)
session.commit()
