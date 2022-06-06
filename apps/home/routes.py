from apps.home import blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.models import Student
from apps.home.forms import StudentListForm
from datetime import datetime
from apps import db



@blueprint.route('/')
def route_default():
    return render_template('home/choice.html', segment='choice')

@blueprint.route('/AdminMain')
@login_required
def index():
    return render_template('home/AdminMain.html', segment='index')

@blueprint.route('/Capture')
def capture():
    return render_template('home/Capture.html', segment='Capture')


# 학생목록
@blueprint.route('/Student_lists')
@login_required
def Student_list():
    student_List = Student.query.all()
    return render_template('/Student_lists', Student=student_List )

# 학생등록
@blueprint.route('/StudentList_Create')
@login_required
def StudentList_Create():
    form = StudentListForm(request.form)
    if request.method == "POST":
        studentlist = Student()
        studentlist.StudentId = form.StudentList.data
        studentlist.StudentName = form.StudentList.data
        db.session.add(studentlist)
        db.session.commit()
        return redirect('home_blueprint.StudentList')
    return render_template('/home/StudentList_Create.html', form=form)







@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None