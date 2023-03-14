from flask import Blueprint, render_template, request, redirect, url_for, send_file
from flask_login import current_user, login_required
from io import BytesIO
from flask_qa.extensions import db
from flask_qa.models import Question, User

main = Blueprint('main', __name__)


@main.route('/home')
def home():
    questions = reversed(Question.query.filter(Question.answer != None).all())

    context = {
        'questions' : questions
    }

    return render_template('home.html', **context)

@main.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    if request.method == 'POST':
        question = request.form['question']
        file = request.files['file']

        question = Question(
            question=question, 
            image_filename = file.filename, 
            image_data = file.read(),
            asked_by_id=current_user.id
        )

        db.session.add(question)
        db.session.commit()
        print(f'Uploaded: {file.filename}')
        return redirect(url_for('main.home'))





    return render_template('ask.html')

@main.route('/answer/<int:question_id>', methods=['GET', 'POST'])
@login_required
def answer(question_id):
    if not current_user.expert:
        if not current_user.admin:
            return redirect(url_for('main.home'))

    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        question.answer = request.form['answer']
        question.ans_data = request.files['file'].read()
        question.ans_filename = request.files['file'].filename
        question.expert_id = current_user.id
        db.session.commit()

        return redirect(url_for('main.home'))

    context = {
        'question' : question
    }

    return render_template('answer.html', **context)

@main.route('/question/<int:question_id>')
def question(question_id):
    question = Question.query.get_or_404(question_id)

    context = {
        'question' : question
    }

    return render_template('question.html', **context)


@main.route('/download/<int:question_id>')
def download(question_id):
    im = Question.query.filter_by(id=question_id).first()
    return send_file(BytesIO(im.image_data), attachment_filename=im.image_filename, as_attachment=True)

@main.route('/ans_download/<int:question_id>')
def ans_download(question_id):
    im = Question.query.filter_by(id=question_id).first()
    return send_file(BytesIO(im.ans_data), attachment_filename=im.ans_filename, as_attachment=True)


@main.route('/unanswered')
@login_required
def unanswered():
    if not current_user.expert:
        if not current_user.admin:
            return redirect(url_for('main.index'))

    unanswered_questions = Question.query\
        .filter(Question.answer == None)\
        .all()

    context = {
        'unanswered_questions' : unanswered_questions
    }

    return render_template('unanswered.html', **context)

@main.route('/users')
@login_required
def users():

    if not current_user.admin:
        return redirect(url_for('main.index'))

    users = User.query.filter_by(admin=False).all()

    context = {
        'users' : users
    }

    return render_template('users.html', **context)

@main.route('/promote/<int:user_id>')
@login_required
def promote(user_id):
    if not current_user.admin:
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)

    user.expert = True
    db.session.commit()

    return redirect(url_for('main.users'))


@main.route('/demote/<int:user_id>')
@login_required
def demote(user_id):
    if not current_user.admin:
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)

    user.expert = False
    db.session.commit()

    return redirect(url_for('main.users'))


@main.route('/delusers')
@login_required
def delusers():

    if not current_user.admin:
        return redirect(url_for('main.index'))

    users = User.query.filter_by(admin=False).all()

    context = {
        'users' : users
    }

    return render_template('delusers.html', **context)

@main.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    if not current_user.admin:
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('main.delusers'))


@main.route('/delques')
@login_required
def delques():

    if not current_user.admin:
        return redirect(url_for('main.index'))

    questions = reversed(Question.query.all())

    context = {
        'questions' : questions
    }

    return render_template('delques.html', **context)

@main.route('/delete_ques/<int:question_id>')
@login_required
def delete_ques(question_id):
    if not current_user.admin:
        return redirect(url_for('main.index'))

    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()

    return redirect(url_for('main.delques'))


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return render_template('profiles.html')
    else:
        return render_template("welcome.html")


@main.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profiles.html')