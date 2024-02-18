import json
import os
import re
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from .models import Post

# Create your views here.
from django.http import HttpResponse

def zerowaste(request):
    return render(request, '0_waste.html', {})

def chatbot(request):
    if check(request) == 'login': 
        with open('polls/static/json/secret.json', encoding='utf-8') as json_file:
            data = json.load(json_file)
        apikey = data['api__key']
        apidict = []
        for openai in apikey:
            content = {
                "apikey": str(openai['api_key']),    
            }
            apidict.append(content)

        openaiJson = json.dumps(apidict)
        return render(request, 'chatbot.html', {'openaiJson': openaiJson})
    else:
        messages.error(request, "챗봇을 이용하시려면 로그인이 필요해요.")
        return redirect('/polls/login')
    
def home_login(request):
    return render(request, 'home_login.html', {})

def home(request):
    if check(request) == 'login':
        return render(request, 'home_login.html')
    else:
        return render(request, 'home.html')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        login_id = request.POST.get('login_id')
        login_password = request.POST.get('login_password')

        if not (login_id and login_password):
            messages.error(request, "아이디와 비밀번호를 모두 입력해 주세요.")
        else:
            try:
                user = User.objects.get(username=login_id)
            except User.DoesNotExist:
                messages.error(request, "존재하지 않는 아이디입니다. 다시 입력해 주세요.")
                return render(request, 'login.html')

            user = User.objects.get(username=login_id)
            
            if check_password(login_password, user.password):
                request.session['user_session'] = user.id
                
                return redirect('/polls/home_login')
            else:
                messages.error(request, "비밀번호가 일치하지 않습니다. 다시 입력해 주세요.")

        return render(request, 'login.html')
    
def member(request):
    if request.method == "GET":
        return render(request, 'member.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        user_id = request.POST.get('user_id')
        user_password = request.POST.get('user_password')
        user_password_c = request.POST.get('user_password_c')

        if not (username and user_id and user_password and user_password_c):
            messages.error(request, "모든 값을 입력해 주세요.")
        elif user_password != user_password_c:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
        elif(isValidFormPassword(user_password)):
            messages.error(request, "비밀번호 기준에 맞지 않습니다. 최소 1개 이상의 특수문자와 8자리 이상으로 구성해 주세요.")

        else:
            user_info = User(
                username=user_id,
                first_name=username,
                password=make_password(user_password),
            )
            user_info.save()
            messages.success(request, "회원가입에 성공했습니다! 로그인 창에서 로그인해 주세요!")
            return redirect('/polls/login')

       
        return render(request, 'member.html')
    
def mini_game(request):
    if check(request) == 'login':
        return render(request, 'mini_game.html')
    else:
        messages.error(request, "미니게임을 이용하시려면 로그인이 필요해요.")
        return redirect('/polls/login')

def nephron(request):
    with open('polls/static/json/nephron_data.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        nephrons = data['props']['pageProps']['initialLocations']  # Access the 'records' list

        nephrondict = []
        for nephron in nephrons:
            input_wastes_str = ', '.join(nephron['input_wastes'])  # Combine list items into a single string
            content = {
                "title": str(nephron['name']),
                "mapx": str(nephron["latitude"]),
                "mapy": str(nephron["longitude"]),
                "info": input_wastes_str,
                "addr": str(nephron.get("address", "")),  
                "image_url": str(nephron.get("image_url", "")),  
            }
        
            nephrondict.append(content)

        nephronJson = json.dumps(nephrondict, ensure_ascii=False)
        return render(request, 'nephron.html', {'nephronJson': nephronJson})

def recycling_center(request):
    with open('polls/static/json/center.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        centers = data['records']  # Access the 'records' list

    centerdict = []
    for center in centers:
        content = {
            "title": str(center['재활용센터명']),
            "mapx": str(center["위도"]),
            "mapy": str(center["경도"]),
            "info": str(center["주요취급품목정보"]),
            "addr1": str(center.get("소재지도로명주소", "")),
            "addr2": str(center.get("소재지지번주소", "")),
            "tel": str(center.get("운영기관전화번호", ""))
        }
        
        centerdict.append(content)

    centerJson = json.dumps(centerdict, ensure_ascii=False)
    return render(request, 'recycling_center.html', {'centerJson': centerJson})

def check(request):
    user_session = request.session.get('user_session', '')
    if user_session == '':
        return 'logout'
    else:
        return 'login'

def recycling_market(request):
    return render(request, 'recycling_market2.html')
    
    
def logout(request):
    request.session.flush()
    return redirect('/polls/home')

def isValidFormPassword(pwd):
    if (len(pwd) <= 8 or not re.findall('[0-9]+', pwd) or not re.findall('[A-z]', pwd)): #숫자, 영문 대소문자 구성
        return True
    elif not re.findall ('[`~!@#$%^&*(),<.>/?]+', pwd): #최소 1개 이상의 특수문자
        return True
    return False

# blog.html 페이지를 부르는 blog 함수
def community(request):
    postlist = Post.objects.all()
    return render(request, 'community.html', {'postlist':postlist})

# def posting(request, pk):
#     # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
#     post = Post.objects.get(pk=pk)
#     # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
#     return render(request, 'posting.html', {'post':post})

def new_post(request):
    if request.method == 'POST':
        contents = request.POST.get('contents', '').strip()
        if contents:
            new_article = Post.objects.create(contents=contents)
        return redirect('/polls/community/')
    return render(request, 'new_post.html')

    
