from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile, Paper, Question
from django.utils.timezone import get_current_timezone
from datetime import datetime
from django.utils.dateparse import parse_date
from django.http import HttpResponse
from django.db.models import Max
from django.contrib.auth import logout


def get_user_role(request):
    user = request.session['user']
    profile = list(Profile.objects.filter(user__username=user).values())[0]
    return profile.get('role')


def login(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        password = request.POST.get('pass', '')
        user = authenticate(username=name, password=password)
        request.session['user'] = name
        profile = list(Profile.objects.filter(user=user).values())[0]
        # if profile.get('role') == 'Teacher':
        return redirect(papers)

    return render(request, 'authentication-login.html', {})


def logout_session(request):
    logout(request)
    return redirect('login')


def create_user(request):
    user_role = get_user_role(request)
    if request.method == 'POST':
        name = request.POST.get('username', '')
        password = request.POST.get('password', '')
        role = request.POST.get('role', '')
        print(name, password, role)
        user = User.objects.create_user(username=name, password=password)
        profile = Profile.objects.create(user=user, role=role)
        return redirect(users)
    return render(request, 'create_user.html', {'user_role': user_role})


def papers(request):
    user_role = get_user_role(request)
    papers = list(Paper.objects.all().values())
    return render(request, 'papers_tables.html', {'papers': papers, 'user_role': user_role})


def users(request):
    user_role = get_user_role(request)
    if user_role != 'SuperUser':
        return redirect(login)
    profiles = list(Profile.objects.filter().values_list('user__username', 'role'))
    users_list = []
    for i in range(len(profiles)):
        if profiles[i][1] != 'SuperUser':
            user_dict = {
                'user': profiles[i][0],
                'role': profiles[i][1]
            }
            users_list.append(user_dict)

    return render(request, 'users_tables.html', {'user_role': user_role, 'user_list': users_list})


def create_papers(request):
    user_role = get_user_role(request)
    username = request.session['user']
    if request.method == 'POST':
        profile = list(Profile.objects.filter(user__username=username))[0]
        print(profile)
        name = request.POST.get('name', '')
        date = request.POST.get('date', '')
        starting_time = request.POST.get('start_time', '')
        ending_time = request.POST.get('end_time', '')
        temp_date = parse_date(date)
        start_time = starting_time
        s_time = int(start_time.split(':')[0])
        if s_time == 12:
            s_time_am_pm_checker = 'P.M.'
        elif s_time == 0:
            s_time += 12
            s_time_am_pm_checker = 'A.M.'
        else:
            if s_time >= 13:
                s_time -= 12
                s_time_am_pm_checker = 'P.M.'
            else:
                s_time_am_pm_checker = 'A.M.'

        s_time_am_pm = str(s_time) + ':' + start_time.split(':')[1] + ' ' + str(s_time_am_pm_checker)
        end_time = ending_time
        print(end_time)
        e_time = int(end_time.split(':')[0])
        if e_time == 12:
            e_time_am_pm_checker = 'P.M.'
        elif e_time == 0:
            e_time += 12
            e_time_am_pm_checker = 'A.M.'
        else:
            if e_time >= 13:
                e_time -= 12
                e_time_am_pm_checker = 'P.M.'
            else:
                e_time_am_pm_checker = 'A.M.'

        e_time_am_pm = str(e_time) + ':' + end_time.split(':')[1] + ' ' + str(e_time_am_pm_checker)
        paper = Paper.objects.create(paper_name=name, date=temp_date, start_time=s_time_am_pm, end_time=e_time_am_pm, teacher=profile)
        return redirect(papers)
    return render(request, 'createpaper.html', {'user_role': user_role})


def questions(request):
    user_role = get_user_role(request)
    if user_role == 'Student':
        return redirect(login)
    qry = list(Paper.objects.all().values('paper_id', 'paper_name'))
    if request.method == 'POST':
        paper_id = request.POST.get('paper_name', '')
        paper = list(Paper.objects.filter(paper_id=paper_id).values('paper_name', 'date', 'start_time', 'end_time'))[0]
        question = list(Question.objects.filter(paper_id__paper_id=paper_id).values('question_id'))
        questions_id = set()
        for item in question:
            questions_id.add(item.get('question_id'))
        questions = []
        que = {}
        for question_id in questions_id:
            question = list(Question.objects.filter(question_id=question_id).values('question', 'choice', 'answer'))
            que = {
                'question_name': question[0].get('question'),
                'choices': [],
                'answer': []
            }
            choice = []
            answer = []
            for item in question:
                choice.append(item.get('choice'))
                if item.get('answer') == 'Correct':
                    answer.append(item.get('choice'))
            que['choices'] = choice
            que['answer'] = answer
            questions.append(que)
        print(questions)
        return render(request, 'questions_tables.html', {'user_role': user_role, 'paper_list': qry, 'paper': paper, 'questions': questions})

    return render(request, 'questions_tables.html', {'user_role': user_role, 'paper_list': qry})


def create_question(request):
    user_role = get_user_role(request)
    username = request.session['user']
    if request.method == 'POST':
        profile = list(Profile.objects.filter(user__username=username))[0]

        # if profile.get('role') == 'Teacher':
        total = int(request.POST.get('total', ''))
        paper_id = request.POST.get('hidden_paper_id', '')
        print(paper_id)
        paper = list(Paper.objects.filter(paper_id=int(paper_id)))[0]
        print(paper)
        question = request.POST.get('question', '')
        max_question_id = Question.objects.aggregate(Max('question_id'))
        max_question_id = max_question_id.get('question_id__max')
        if max_question_id is None:
            max_question_id = 1
        count = 1
        while 1:
            answer = request.POST.get('answer_' + str(count), '')
            correct = request.POST.get('correct_' + str(count), '')
            Question.objects.create(question_id=max_question_id+1,
                                    paper_id=paper,
                                    question=question,
                                    choice=answer,
                                    answer=correct)
            count += 1
            if count >= total + 1:
                break

    qry = list(Paper.objects.all().values('paper_id', 'paper_name'))
    return render(request, 'createquestion.html', {'paper_list': qry, 'user_role': user_role})


def papers_list(request):
    user_role = get_user_role(request)
    data = int(request.GET['id'])
    qry = Paper.objects.filter(paper_id=data).values_list('date', 'start_time', 'end_time', )
    paper = Paper.objects.filter(paper_id=data)
    qry_list = list(qry)
    date = qry_list[0][0]
    date_time = date.strftime("%m/%d/%Y")
    start_time = qry_list[0][1]
    end_time = qry_list[0][2]
    print(start_time, end_time)
    data = str(date_time) + ',' + start_time + ',' + end_time
    return HttpResponse(data)
