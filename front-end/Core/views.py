import json
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SingupForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



DATA_PATH = os.path.join('data', 'users.json')
ARTICLE_PATH = os.path.join('data', 'articles.json')

INTERACTION_FILE = os.path.join('data', 'user_interractions.json')


#This is the homepage functionality 

def home_view(request):
    try:
        with open(ARTICLE_PATH, 'r') as f:
            article = json.load(f)
    except Exception:
        article = []
    
    if 'user' not in request.session:
        request.session['user'] = 'DemoUser'
        
    article_to_view = article[:3]    
    
    context = {
        'articles' : article_to_view
    }
    return render(request, 'home.html', context)


#the function to view articles in details
def article_detail_view(request, article_id):
    try:
        with open(ARTICLE_PATH, 'r') as f:
            articles = json.load(f)
    except Exception:
        articles = []

    # Find article by ID
    article = next((a for a in articles if a.get('id') == int(article_id)), None)
    
    if not article:
        return render(request, '404.html', status=404)
    
    context = {
        'article': article
    }
    return render(request, 'article_detail.html', context)


def recommended_view(request):
    # For now, just show all articles or filtered by user interests
    try:
        with open(DATA_PATH, 'r') as f:
            articles = json.load(f)
    except Exception:
        articles = []
    
    user_interests = request.session.get('user_interests', [])
    
    # Filter articles by user interests (tags)
    recommended_articles = [
        a for a in articles
        if any(interest.lower() in (tag.lower() for tag in a.get('tags', [])) for interest in user_interests)
    ]
    
    context = {
        'articles': recommended_articles
    }
    
    return render(request, 'recommended.html', context)


#the search functionality
def search_view(request):
    query = request.GET.get('q', '').strip().lower()
    
    try:
        with open(DATA_PATH, 'r') as f:
            articles = json.load(f)
    except Exception:
        articles = []
        
    articles = [a for a in articles if isinstance(a, dict) and 'title' in a and 'abstract' in a]
    
    if query:
        filtered = [
            a for a in articles
            if query in a.get('title').lower() or
               query in a.get('abstract').lower() or
               any(query in tag.lower() for tag in a.get('tags', []))
        ]
        
    else:
        filtered = []
    
    return render(request, 'search_results.html', {'articles': filtered, 'query': query})


#the signup_form functioanlity 
def signup_view(request):
    if request.method == 'POST':
        form = SingupForm(request.POST)
        if form.is_valid():
            new_user = form.cleaned_data
            
            ### load exixting users
            with open(DATA_PATH, 'r') as f:
                users = json.load(f)
                
            ### check for nicename uniqueness 
            if any(u['username'] == new_user['username'] for u in users):
                messages.error(request, "Username is already exists!")
                return render(request, 'registration/signup.html', {'form':form})
            
            #hashed the password
            
            new_user['password'] = make_password(new_user['password'])
            ## Save user
            users.append(new_user)
            with open(DATA_PATH, 'w') as f:
                json.dump(users, f, indent=4)
                
            messages.success(request, "Account created Successfully")
            return redirect('login')
        
    else:
        form = SingupForm()
            
    return render(request, 'registration/signup.html', {'form': form })

#the user interaction form 
@csrf_exempt
def user_interaction_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        action = data.get('action')  # e.g., 'click', 'like', 'search'
        value = data.get('value')

        # Make sure the file exists
        if not os.path.exists(INTERACTION_FILE):
            with open(INTERACTION_FILE, 'w') as f:
                json.dump({}, f)

        with open(INTERACTION_FILE, 'r') as f:
            interactions = json.load(f)

        if username not in interactions:
            interactions[username] = {
                "clicks": [],
                "likes": [],
                "favorites": [],
                "time_spent": [],
                "searches": [],
                "last_active": timezone.now().isoformat()
            }

        user_data = interactions[username]
        
        # Append based on action
        if action == 'clicks':
            user_data['clicks'].append(value)
        elif action == 'likes':
            if value not in user_data['likes']:
                user_data['likes'].append(value)
        elif action == 'unlike':
            if value in user_data['likes']:
                user_data['likes'].remove(value)
        elif action == 'favorites':
            if value not in user_data['favorites']:
                user_data['favorites'].append(value)
        elif action == 'unfavorite':
            if value in user_data['favorites']:
                user_data['favorites'].remove(value)
        elif action == 'time_spent':
            # value = { "article_id": "123", "seconds": 30 }
            user_data['time_spent'].append(value)
        elif action == 'search':
            user_data['searches'].append(value)

        user_data['last_active'] = timezone.now().isoformat()
        interactions[username] = user_data

        # Save updated file
        with open(INTERACTION_FILE, 'w') as f:
            json.dump(interactions, f, indent=4)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'error': 'Invalid method'}, status=405)

def initialize_user_interaction(username):
    if not os.path.exists(INTERACTION_FILE):
        with open(INTERACTION_FILE, 'w') as f:
            json.dump({}, f)

    with open(INTERACTION_FILE, 'r') as f:
        data = json.load(f)

    if username not in data:
        data[username] = {
            "clicks": [],
            "likes": [],
            "searches": [],
            "last_active": timezone.now().isoformat()
        }

        with open(INTERACTION_FILE, 'w') as f:
            json.dump(data, f, indent=4)


#the function for the login
def login_view(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            ## Load users from Json
            
            try:
                with open(DATA_PATH, 'r') as f:
                    users = json.load(f)
            except FileNotFoundError:
                users = []
                
            print('Hey, i am here')
                
            # let try to find a user
            for user in users:
                if user['username'] == username and check_password(password, user['password']):
                    print('i am here')
                    request.session['user'] = user['username']
                    messages.success(request, 'Login Successful !')
                    print(f"{username} logged in")
                    
                    return redirect('home')
            messages.error(request, 'Invalid username or password')
    except Exception as e:
        print(f"this is an issue with {e}")
        messages.error(request, 'login failed with ')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
