from apps import db
from datetime import datetime


class Subject(db.Model):
    __tablename__ = 'Subject'

    Professor_name = db.Column(db.String(64)) #교수명
    Subject_name = db.Column(db.String(64)) #과목명
    Subject_code = db.Column(db.String(64), primary_key=True) #과목코드
    Semester = db.Column(db.String(64))  #년도-학기 ex)2022-1학기 (과연 이걸 string으로 받아도 될까?)

    #Start_time = db.Column(db.DateTime()) #강의시작시간(주차별관리에서 사용)
    #End_time = db.Column(db.DateTime()) #강의종료시간(주차별관리에서 사용)

    def __repr__(self): #대표로 호출해야하는 것을 불러옴 / 다 불러와도 상관 없음(예시는 밑에 있음)
        return str(f"{self.Professor_name}, {self.Subject_name}, {self.Subject_code}, {self.Semester}")
    #왜 안될까.


