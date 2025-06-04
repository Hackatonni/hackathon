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
from django.contrib.auth.decorators import login_required
from . forms import *
from . views import *
from django.http import JsonResponse
import datetime



DATA_PATH = os.path.join('data', 'users.json')
ARTICLE_PATH = os.path.join('data', 'articles.json')
RECOMMENDATION_PATH = os.path.join('data', '_recommendations.json')


ONBOARDING_RESPONSES_PATH = os.path.join('data', 'onboarding_responses.json')

INTERACTION_FILE = os.path.join('data', 'user_interractions.json')


#This is the homepage functionality 
# @login_required(login_url='login/')
# def home_view(request):
#     try:
#         with open(ARTICLE_PATH, 'r') as f:
#             article = json.load(f)
#     except Exception:
#         article = []
    
#     if 'user' not in request.session:
#         request.session['user'] = 'DemoUser'
        
#     article_to_view = article[:3]    
    
#     context = {
#         'articles' : article_to_view
#     }
#     return render(request, 'home.html', context)



def home_view(request):
    username = request.session.get('user', 'DemoUser')
    rec_file = os.path.join('data', f'{username}_custom_recommendations.json')

    try:
        with open(rec_file, 'r') as f:
            articles = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        articles = []

    context = {
        'articles': articles,
        'username': username
    }
    return render(request, 'home.html', context)



def has_completed_onboarding(username):
    if not os.path.exists(ONBOARDING_RESPONSES_PATH):
        return False

    try:
        with open(ONBOARDING_RESPONSES_PATH, 'r') as f:
            responses = json.load(f)
        user_responses = responses.get(username, [])
    except:
        return False

    rec_file = os.path.join('data', f"{username}_recommendations.json")
    if not os.path.exists(rec_file):
        return False

    with open(rec_file, 'r') as f:
        articles = json.load(f)

    return len(user_responses) >= len(articles)


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

            # Ensure the file exists before reading
            if not os.path.exists(DATA_PATH):
                with open(DATA_PATH, 'w') as f:
                    json.dump([], f)

            # Load users safely
            with open(DATA_PATH, 'r') as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []

            # Check for username uniqueness
            if any(u['username'] == new_user['username'] for u in users):
                messages.error(request, "Username already exists!")
                return render(request, 'registration/signup.html', {'form': form})

            # Hash password
            new_user['password'] = make_password(new_user['password'])

            # Save new user
            users.append(new_user)
            with open(DATA_PATH, 'w') as f:
                json.dump(users, f, indent=4)
                
            # Path to user activity file
                USER_ACTIVITY_PATH = os.path.join('data', 'user_activity.json')

                # Ensure file exists
                if not os.path.exists(USER_ACTIVITY_PATH):
                    with open(USER_ACTIVITY_PATH, 'w') as f:
                        json.dump({}, f)

                # Load existing data
                with open(USER_ACTIVITY_PATH, 'r') as f:
                    try:
                        activity_data = json.load(f)
                    except json.JSONDecodeError:
                        activity_data = {}

                # Add blank activity record for the new user
                activity_data[new_user['username']] = {}

                with open(USER_ACTIVITY_PATH, 'w') as f:
                    json.dump(activity_data, f, indent=4)
                    
                                
            # After saving user
            ai_output_file = os.path.join('data', f"{new_user['username']}_recommendations.json")

            # Simulate AI team sending 20 articles
            try:
                with open(RECOMMENDATION_PATH, 'r') as f:
                    all_articles = json.load(f)
                selected_articles = all_articles[:10]  # Simulate AI's pick
                with open(ai_output_file, 'w') as f:
                    json.dump(selected_articles, f, indent=4)
            except Exception as e:
                print(f"Error during AI simulation: {e}")

            request.session['user'] = new_user['username']
            return redirect('onboarding', username=new_user['username'])
            # messages.success(request, "Account created Successfully")
            # return redirect('login')

    else:
        form = SingupForm()

    return render(request, 'registration/signup.html', {'form': form})

# @login_required(login_url='login/')
# def onboarding_view(request, username):
#     user = request.session.get('user')
#     if user != username:
#         return JsonResponse({'error': 'Unauthorized'}, status=403)

#     rec_file = os.path.join('data', f"{username}_recommendations.json")
#     if not os.path.exists(rec_file):
#         return JsonResponse({'error': 'Recommendations not found'}, status=404)

#     with open(rec_file, 'r') as f:
#         articles = json.load(f)

#     # Load current progress
#     try:
#         with open(ONBOARDING_RESPONSES_PATH, 'r') as f:
#             responses = json.load(f)
#     except:
#         responses = {}

#     user_responses = responses.get(username, [])
#     current_index = len(user_responses)

#     if current_index >= len(articles):
#         return redirect('home')

#     article = articles[current_index]
#     return render(request, 'onboarding.html', {'article': article, 'progress': current_index, 'total': len(articles)})

def onboarding_view(request, username):
    user = request.session.get('user')
    if user != username:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    rec_file = os.path.join('data', f"{username}_recommendations.json")
    if not os.path.exists(rec_file):
        return JsonResponse({'error': 'Recommendations not found'}, status=404)

    try:
        #     return JsonResponse({'error': 'No valid recommendations found.'}, status=500)
        with open(rec_file, 'r') as f:
            articles = json.load(f)
            if isinstance(articles, dict):
                articles = list(articles.values())  # fix malformed structure
            if not isinstance(articles, list) or not articles:
                return JsonResponse({'error': 'No valid recommendations found.'}, status=500)

    except Exception as e:
        return JsonResponse({'error': f'Failed to load recommendations: {str(e)}'}, status=500)

    # Load current progress
    try:
        with open(ONBOARDING_RESPONSES_PATH, 'r') as f:
            responses = json.load(f)
    except:
        responses = {}

    user_responses = responses.get(username, [])
    current_index = len(user_responses)

    if current_index >= len(articles):
        return redirect('home')

    try:
        article = articles[current_index]
    except IndexError:
        return JsonResponse({'error': 'Index out of range while accessing recommendations.'}, status=500)

    return render(request, 'onboarding.html', {
        'article': article,
        'progress': current_index,
        'total': len(articles)
    })

# @csrf_exempt
# @require_http_methods(["POST"])
def onboarding_response_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        article_id = data.get('article_id')
        response = data.get('response')  # "interested" or "not_interested"

        if not username or not article_id or not response:
            return JsonResponse({'error': 'Incomplete data'}, status=400)

        # Ensure the data folder exists
        response_file_path = os.path.join('data', f'onboarding_{username}_responses.json')
        os.makedirs(os.path.dirname(response_file_path), exist_ok=True)

        # If file doesn't exist or is empty, initialize it
        if not os.path.exists(response_file_path) or os.path.getsize(response_file_path) == 0:
            with open(response_file_path, 'w') as f:
                json.dump({}, f)

        # Load existing responses safely
        with open(response_file_path, 'r') as f:
            try:
                responses = json.load(f)
            except json.JSONDecodeError:
                responses = {}

        # Update the user's response
        if username not in responses:
            responses[username] = []

        responses[username].append({
            'article_id': article_id,
            'response': response
        })

        # Save back
        with open(response_file_path, 'w') as f:
            json.dump(responses, f, indent=4)

        return JsonResponse({'status': 'recorded'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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
                    
                    if not has_completed_onboarding(username):
                        return redirect('onboarding', username=username)
                    return redirect('home')
            messages.error(request, 'Invalid username or password')
    except Exception as e:
        print(f"this is an issue with {e}")
        messages.error(request, 'login failed with ')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login/')
def upload_article_view(request):
    if request.method == 'POST':
        form = ArticleUploadForm(request.POST)
        if form.is_valid():
            # Load existing articles
            if not os.path.exists(ARTICLE_PATH):
                with open(ARTICLE_PATH, 'w') as f:
                    json.dump([], f)

            with open(ARTICLE_PATH, 'r') as f:
                try:
                    articles = json.load(f)
                except json.JSONDecodeError:
                    articles = []

            # Create new article entry
            new_id = max([a['id'] for a in articles], default=0) + 1
            username = request.session.get('user', 'anonymous')
            tags = [tag.strip() for tag in form.cleaned_data['tags'].split(',')]

            new_article = {
                'id': new_id,
                'title': form.cleaned_data['title'],
                'abstract': form.cleaned_data['abstract'],
                'content': form.cleaned_data['content'],
                'tags': tags,
                'author': username,
                'timestamp': timezone.now().isoformat()
            }

            # Save article
            articles.append(new_article)
            with open(ARTICLE_PATH, 'w') as f:
                json.dump(articles, f, indent=4)

            messages.success(request, "Article uploaded successfully!")
            return redirect('home')
    else:
        form = ArticleUploadForm()

    return render(request, 'upload_article.html', {'form': form})


@csrf_exempt
# def record_user_action(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             username = data['username']
#             article_id = str(data['article_id'])  # ensure it's a string
#             action = data['action']  # e.g., "click", "like", "favourite"

#             USER_ACTIVITY_PATH = os.path.join('data', 'user_activity.json')
#             with open(USER_ACTIVITY_PATH, 'r') as f:
#                 activity_data = json.load(f)

#             # Ensure user exists
#             if username not in activity_data:
#                 return JsonResponse({'status': 'error', 'message': 'User not found'}, status=400)

#             # Get user's activity
#             user_data = activity_data.get(username, {})
#             article_data = user_data.get(article_id, {
#                 "clicks": [],
#                 "likes": [],
#                 "favorites": [],
#                 "time_spent": [],
#                 "searches": [],
#                 "last_active": str(datetime.datetime.now())
#             })

#             # Update action
#             if action == "click":
#                 article_data["clicks"].append("1")
#             elif action == "like":
#                 article_data["likes"].append("1")
#             elif action == "dislike":
#                 article_data["likes"].append("0")
#             elif action == "favourite":
#                 article_data["favorites"].append("1")

#             article_data["last_active"] = str(datetime.datetime.now())
#             user_data[article_id] = article_data
#             activity_data[username] = user_data

#             # Save
#             with open(USER_ACTIVITY_PATH, 'w') as f:
#                 json.dump(activity_data, f, indent=4)

#             return JsonResponse({'status': 'success'})

#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
# def record_user_interaction(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username = data.get('username')
#         article_id = data.get('article_id')
#         action = data.get('action')

#         user_data_path = os.path.join('data', f"{username}_interactions.json")

#         if not os.path.exists(user_data_path):
#             with open(user_data_path, 'w') as f:
#                 json.dump([], f)

#         with open(user_data_path, 'r') as f:
#             try:
#                 interactions = json.load(f)
#             except json.JSONDecodeError:
#                 interactions = []

#         interactions.append({
#             "article_id": article_id,
#             "action": action,
#             "timestamp": datetime.now().isoformat()
#         })

#         with open(user_data_path, 'w') as f:
#             json.dump(interactions, f, indent=4)

#         return JsonResponse({"status": "ok", "msg": f"{action} recorded."})
#     return JsonResponse({"status": "error", "msg": "Invalid request"}, status=400)


def record_user_interaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        article_id = data.get('article_id')
        action = data.get('action')

        try:
            user = User.objects.get(username=username)
            profile = user.userprofile
            profile.update_activity(article_id, action)
            return JsonResponse({"status": "ok", "msg": f"{action} recorded for article {article_id}."})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "msg": "User not found."}, status=404)

    return JsonResponse({"status": "error", "msg": "Invalid request"}, status=400)
