from urllib import request
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from questions.forms import RegistrationForm,LoginForm,QuestionForm,AnswerForm
from django.views.generic import CreateView,FormView,ListView,DetailView
from questions.models import Answers, MyUser,Questions
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib import messages



# Create your views here
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"you must login")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper            


@method_decorator(signin_required,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="home.html"
    form_class=QuestionForm
    model=Questions
    success_url=reverse_lazy("index")
    context_object_name="questions"
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user)    




class SignupView(CreateView):
    model=MyUser
    form_class=RegistrationForm
    template_name='register.html'
    success_url=reverse_lazy("register")

class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login success")
                return redirect("index")
            else:
                messages.error(request,"login failed")
                return render(request,self.template_name,{"form":form})

def signout_view(request,*args,**kwargs):
    logout(request)
    messages.success(request,"you logout successfully")
    return redirect("signin")

@method_decorator(signin_required,name="dispatch")
class QuestionListView(ListView):
    model=Questions
    template_name="question-list.html"
    context_object_name="question"

@method_decorator(signin_required,name="dispatch")
class QuestionDetailView(DetailView,FormView):
    model=Questions
    template_name="question-detail.html"
    pk_url_kwarg="id"
    context_object_name="question"
    form_class=AnswerForm


@signin_required
def add_answer(request,*args,**kwargs):
    if request.method=="POST":
        form=AnswerForm(request.POST)
        if form.is_valid():
            answer=form.cleaned_data.get("answer")
            qid=kwargs.get("id")
            ques=Questions.objects.get(id=qid)
            Answers.objects.create(Questions=ques,user=request.user,answer=answer)
            messages.success(request,"answer created")
            return redirect("index")
        else:
            messages.error(request,"please try again")
            return redirect("index")
#localhost:8000/answers/{id}/upvote/
@signin_required
def upvote_view(request,*args,**kwargs):
    ans_id=kwargs.get("id")
    ans=Answers.objects.get(id=ans_id)
    ans.upvote.add(request.user)
    ans.save()
    return redirect("index")

@signin_required    
def remove_answer(request,*args,**kwargs):
    ans_id=kwargs.get("id")
    Answers.objects.get(id=ans_id).delete()
    messages.success(request,"answer deleted")
    return redirect("index")
        
