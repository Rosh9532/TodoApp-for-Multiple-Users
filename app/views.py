from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate, login as loginuser,logout
from app.forms import TODOForm
from app.models import TODO
from django.forms import TextInput, Textarea
from django import forms
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user=request.user
        form=TODOForm()
        todos=TODO.objects.filter(user=user).order_by('priority')
        return render(request,'index.html',context={'form':form,'todos':todos})

    
    # return render(request,'index.html')

# def home(request):
#     form=TODOForm()
#     return render(request,'index.html',context={'form':form})



def signup(request):
   if request.method =='GET':
        form=UserCreationForm()
        context={
            "form" :form
       }
        return render(request,'signup.html',context=context)
   else:
        print(request.POST)
        form=UserCreationForm(request.POST)
        context={
            "form" :form
       }
        if form.is_valid():
            print("Valid")
            user=form.save()
            
            print(user)
            if user is not None:   
                return redirect('login')  
        else:
            print(form.errors)
            return render(request,'signup.html',context=context)



def login(request):
    if request.method =='GET':
        form1=AuthenticationForm()
        context={
            "form":form1
        }
        return render(request,'login.html',context=context)
    else:
        print("rosho")
        form=AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            print("roshni")
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            print("autthenticated",user)
            if user is not None:
                loginuser(request,user)
                return redirect('home') 
        else:  
            context={
            "form":form
            }  
            return render(request,'login.html',context=context)    

@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user=request.user
        print(user)
        form=TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo=form.save(commit=False)
            todo.user=user
            form.save()
            return redirect('home')
        else:
            return render(request,'index.html',context={'form':form})
    # form=TODOForm(request.POST)
    # if form.is_valid():
    #     print(form.cleaned_data)
    #     return redirect('home')
    # else:
    #      return render(request,'index.html',context={'form':form})
def change_todo(request,id,status):
    
    todo=TODO.objects.get(pk=id)
    todo.status=status
    todo.save()
    return redirect('home')


def delete_todo(request,id):
    print(id)
    TODO.objects.get(pk=id).delete()
    return redirect('home')



def signout(request):
    logout(request)
    return redirect('login')

def about(request):
    return render(request,'about.html')

