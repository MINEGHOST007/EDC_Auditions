from django.shortcuts import render,redirect, get_object_or_404
from .models import Inductees,Question, Response, Posts
from . forms import BasicDetailsForm, QuestionsForm, PostsForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    return render(request,'home.html')

def signup_redirect(request):
    return render(request,'home.html')

def results(request):
    return render(request,'results.html')

def club_members(request):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        if is_club_member:
            students = Inductees.objects.filter(is_club_member=False).order_by('-round')
            return render(request, 'admin.html',{'students':students})
    return redirect('home')

def search(request,search_term="",category=""):
    user = request.user
    students = []
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        if is_club_member:
            if request.method == "GET":
                if category == "name":
                    if search_term == "":
                        students = Inductees.objects.filter(is_club_member=False)
                    else:
                        students = Inductees.objects.filter(is_club_member=False,full_name__icontains=search_term).order_by('-round')
                elif category == "roll":
                    if search_term == "":
                        students = Inductees.objects.filter(is_club_member=False)
                    else:
                        students = Inductees.objects.filter(is_club_member=False,rollnumber__icontains=search_term).order_by('-round')
                elif category == "branch":
                    if search_term == "":
                        students = Inductees.objects.filter(is_club_member=False)
                    else:
                        students = Inductees.objects.filter(is_club_member=False,department__icontains=search_term).order_by('-round')
            return render(request, 'admin.html',{'students':students})
    return redirect('home')

def student_profile(request,id):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        if is_club_member:
            student = Inductees.objects.get(id=id)
            comments = Posts.objects.filter(user=student)
            likes = student.total_likes()
            answers = Response.objects.filter(student=student)
            form = PostsForm(request.POST)
            allow = Inductees.objects.get(user = user).year
            liked = False
            if student.like.filter(id=user.id).exists():
                liked = True
            print(allow)
            if form.is_valid():
                post = Posts(
                    user = student,
                    comment = form.cleaned_data['comment'],
                    round = form.cleaned_data['round'],
                    by = Inductees.objects.get(user = user).full_name,
                    year = Inductees.objects.get(user = user).year,
                )
                post.save()
                return redirect('student_profile',id=id)
            return render(request,'student_profile.html',{'student':student,'comments2':comments.filter(year = 2).order_by('-round'),'comments3':comments.filter(year=3).order_by('-round'),'comments4':comments.filter(year=4).order_by('-round'), 'form':form, 'answers':answers, 'allow':allow,'likes':likes,'liked':liked})
    return redirect('home')

@login_required
def details(request):
    if request.method == 'POST':
        form = BasicDetailsForm(request.POST)
        if form.is_valid():
            if Inductees.objects.filter(user=request.user).exists() :
                student = get_object_or_404(Inductees, user = request.user)
                student.full_name = form.cleaned_data['name']
                student.gender = form.cleaned_data['gender']
                student.registration_no = form.cleaned_data['registration_no']
                student.rollnumber = form.cleaned_data['roll_no']
                student.department = form.cleaned_data['branch']
                student.place = form.cleaned_data['place']
                student.phone_number = form.cleaned_data['Mobile_Number']
                student.year = form.cleaned_data['year']
                student.save()
                return redirect('ques')
            else:
                return redirect('home')
    else:
        if Inductees.objects.filter(user=request.user).exists():
            student = get_object_or_404(Inductees, user = request.user)
            form = BasicDetailsForm(initial={
            'name': student.full_name,
            'gender': student.gender,
            'registration_no': student.registration_no,
            'roll_no': student.rollnumber,
            'branch': student.department,
            'place': student.place,
            'Mobile_Number': student.phone_number,
            'year': student.year,
            })
        else:
            form = BasicDetailsForm()
    return render(request, 'detailsform.html', {'form': form})

@login_required
def ques(request):
    if Inductees.objects.filter(user=request.user).exists():
        student = get_object_or_404(Inductees, user = request.user)
        questions = Question.objects.all()
        if request.method == 'POST':        
            form = QuestionsForm(request.POST)
            if form.is_valid():               
                if Response.objects.filter(student=student).exists():
                    for q in questions:
                        response = get_object_or_404(Response, student = student, question = q)
                        response.answer = form.cleaned_data[f'{q.id}']
                        response.save()
                else:
                    for q in questions:
                        response = Response(
                        student = student,
                        question = q,
                        answer = form.cleaned_data[f'{q.id}'] 
                        )
                        response.save()
                return redirect('/')
            else:
                return render(request, 'questions.html', {'form' : form})
       
        else:
            if Response.objects.filter(student=student).exists():
                responses = get_object_or_404(Inductees, user = request.user)
                formData = {}
                for q in questions:
                    formData[f'{q.id}'] = get_object_or_404(Response, student= student, question = q).answer
                form = QuestionsForm(initial= formData)
            else:
                form = QuestionsForm()
            return render(request, 'questions.html', {'form' : form})
    else:
        return redirect('details')
    

@login_required
def like(request,id):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        if is_club_member:
            student = Inductees.objects.get(id=id)
            liked = False
            if student.like.filter(id=user.id).exists():
                student.like.remove(user)
                liked = False
            else:
                liked = True
                student.like.add(user)
            return HttpResponseRedirect(reverse('student_profile', args=[str(id)]))
    return redirect('home')

@login_required
def filter(request,type):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        students = []
        if is_club_member:
            if request.method=='GET':
                students = Inductees.objects.filter(is_club_member=False,color = type).order_by('-round')
            return render(request, 'admin.html',{'students':students})
        else:
            return redirect('home')
    else:
        return redirect('home')

@login_required
def mark(request,id,type):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        if is_club_member:
            if request.method=='POST':
                student = get_object_or_404(Inductees, id = id)
                student.color = type
                student.save()
            return HttpResponseRedirect(reverse('student_profile', args=[str(id)]))
        else:
            return redirect('home')
    else:
        return redirect('home')