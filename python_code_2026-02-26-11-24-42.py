from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    courses = relationship('Course', secondary='enrollments', back_populates='students')

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    capacity = Column(Integer)
    students = relationship('Student', secondary='enrollments', back_populates='courses')

class Enrollment(Base):
    __tablename__ = 'enrollments'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)

class EnrollStudentRequest(BaseModel):
    student_id: int
    course_id: int

class EnrollStudentResponse(BaseModel):
    message: str

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

engine = create_engine('sqlite:///university.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.post('/enroll', response_model=EnrollStudentResponse)
def enroll_student(request: EnrollStudentRequest, db: Session = Depends(get_db)):
    student = db.get(Student, request.student_id)
    course = db.get(Course, request.course_id)

    if not student or not course:
        raise HTTPException(status_code=404, detail='Student or course not found')

    if len(course.students) >= course.capacity:
        raise HTTPException(status_code=400, detail='Course is at maximum capacity')