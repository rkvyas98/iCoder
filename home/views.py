from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from blog.models import Post

# HTML pages here.

def home(request):
    top_post = Post.objects.all().order_by('views').reverse()[0:4]
    print(top_post)
    return render(request, 'home/home.html',{ 'top_post' : top_post})
    
def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email,phone,content)
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<5:
            messages.error(request, "Please fill all the fields of form!")

        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been sent successfully!")

    return render(request, 'home/contact.html')

def about(request):
    messages.error(request, 'This is about')
    return render(request, 'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query) > 80:
        allposts = Post.objects.none()
    else:
        allpostsTitle = Post.objects.filter(title__icontains=query)
        allpostsContent = Post.objects.filter(content__icontains=query)
        allposts = allpostsTitle.union(allpostsContent)

    if allposts.count() == 0:
        messages.error(request, 'No search reults found. Please refine your query!')

    params ={
        'allposts' : allposts,
        'query' : query
    }
    return render(request, 'home/search.html', params)

# Authentication APIs

def handleSignup(request):
    if request.method == 'POST':
        # Getting post params
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for inputs
        if len(username) > 10:
            messages.error(request, "Username should contain less than 10 characters.")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers.")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords donot match. ")
            return redirect('home')

        # creating users
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully created!")

        return redirect('home')

    else:
        return HttpResponse("404 - Not Found")

def handleLogin(request):
    if request.method == 'POST':
        # Getting post params
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username = loginusername, password = loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In!")
            return redirect('home')
        
        else:
            messages.error(request, "Invalid Credentials, Please Try Again!")
            return redirect('home')

    return HttpResponse('404 - Not Found')
    
def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out!")
    return redirect('home')