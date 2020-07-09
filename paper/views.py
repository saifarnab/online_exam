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


def login(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        password = request.POST.get('pass', '')
        user = authenticate(username=name, password=password)
        request.session['user'] = name
        profile = list(Profile.objects.filter(user=user).values())[0]
        # if profile.get('role') == 'Teacher':
        return redirect(papers)

    return render(request, 'login.html', {})


def logout_session(request):
    logout(request)
    return redirect('login')


def create_user(request):
    if request.method == 'POST':
        name = request.POST.get('username', '')
        password = request.POST.get('password', '')
        role = request.POST.get('role', '')
        print(name, password, role)
        user = User.objects.create_user(username=name, password=password)
        profile = Profile.objects.create(user=user, role=role)
    return render(request, 'create_user.html', {})


def papers(request):
    papers = list(Paper.objects.all().values())
    paper_list = []
    for paper in papers:
        date = paper.get('date')
        date_time = date.strftime("%m/%d/%Y")
        json = {
            'paper_name': paper.get('paper_name'),
            'date': date_time,
            'start_time': paper.get('start_time'),
            'end_time': paper.get('end_time'),
        }
        paper_list.append(json)
    return render(request, 'papers.html', {'papers': paper_list})


def create_papers(request):
    username = request.session['user']
    if request.method == 'POST':
        profile = list(Profile.objects.filter(user__username=username))[0]
        print(profile)
        name = request.POST.get('name', '')
        date = request.POST.get('date', '')
        starting_time = request.POST.get('start_time', '')
        ending_time = request.POST.get('end_time', '')
        temp_date = parse_date(date)
        print(temp_date)
        print(name, date, starting_time, ending_time)
        paper = Paper.objects.create(paper_name=name, date=temp_date, start_time=starting_time, end_time=ending_time, teacher=profile)
        return redirect(papers)
    return render(request, 'createpaper.html', {})


def create_question(request):
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
    return render(request, 'createquestion.html', {'paper_list': qry})


def papers_list(request):
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
