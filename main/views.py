from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
import os
import requests
# Create your views here.

def home(request):
    return render(request, 'html/index.html')

def Aldult_English(request):
    return render(request, 'html/adultenglish/Adult_English.html')

def Aldult_English1(request):
    return render(request, 'html/adultenglish/Adult_English1.html')

def Aldult_English2(request):
    return render(request, 'html/adultenglish/Adult_English2.html')

def Children_English(request):
    return render(request, 'html/chidrenenglish/Children_English.html')

def Children_English1(request):
    return render(request, 'html/chidrenenglish/Children_English1.html')

def Children_English2(request):
    return render(request, 'html/chidrenenglish/Children_English2.html')

def ielts(request):
    return render(request, 'html/ietls/ielts.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'html/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username  = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password) 
        print(user)  # kiểm tra xem user có tồn tại không
        # kiểm tra xem user có tồn tại không
        if user is not None:
            login(request, user)
            print('Login successfully')
            return redirect('home')
        else: messages.info(request,'Username or password is incorrect')
    form = UserCreationForm()
    context = {'form':form}
    return render(request, 'html/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def unit1(request):
    return render(request, 'html/chidrenenglish/unit1.html')

def unit2(request):
    return render(request, 'html/chidrenenglish/unit2.html')

def unit3(request):
    return render(request, 'html/chidrenenglish/unit3.html')

def unit4(request):
    return render(request, 'html/chidrenenglish/unit4.html')

def unit5(request):
    return render(request, 'html/chidrenenglish/unit5.html')

def unit6(request):
    return render(request, 'html/chidrenenglish/unit6.html')

def unit7(request):
    return render(request, 'html/chidrenenglish/unit7.html')

def unit8(request):
    return render(request, 'html/chidrenenglish/unit8.html')

def unit9(request):
    return render(request, 'html/chidrenenglish/unit9.html')


def _compute_level_and_recommendation(score: float):
	# Simple threshold-based placement; adjust as needed
	if score >= 85:
		level = 'Upper-Intermediate (B2)'
		rec = (
			"Trình độ của bạn ở mức B2. Khuyến nghị học khóa IELTS Foundation/IELTS 5.5-6.5, "
			"tập trung kỹ năng đọc-nghe nâng cao, từ vựng học thuật và kỹ năng viết Task 2."
		)
		target_url = '/Aldult_English2'
		target_label = 'Vào khóa Adult English 2 (B2/IELTS)'
	elif score >= 70:
		level = 'Intermediate (B1)'
		rec = (
			"Bạn đang ở mức B1. Nên học General English Intermediate và bắt đầu "
			"chuẩn bị IELTS căn bản, luyện ngữ pháp trung cấp và kỹ năng nói theo chủ đề."
		)
		target_url = '/Aldult_English1'
		target_label = 'Vào khóa Adult English 1 (B1)'
	elif score >= 50:
		level = 'Pre-Intermediate (A2)'
		rec = (
			"Bạn ở mức A2. Khuyến nghị học Pre-Intermediate để củng cố ngữ pháp cơ bản, "
			"tăng vốn từ chủ đề hàng ngày và luyện nghe-hội thoại thực tế."
		)
		target_url = '/Children_English1'
		target_label = 'Vào Children English 1 (A2)'
	else:
		level = 'Beginner (A1)'
		rec = (
			"Bạn ở mức A1. Hãy bắt đầu với khóa Beginner/Children Basic, tập trung phát âm, "
			"từ vựng cơ bản và mẫu câu giao tiếp thông dụng."
		)
		target_url = '/Children_English'
		target_label = 'Vào Children English (A1)'
	return level, rec, target_url, target_label


@csrf_exempt
def api_test_result(request):
	if request.method != 'POST':
		return JsonResponse({'error': 'Method not allowed'}, status=405)

	# Ensure session key exists for anonymous tracking
	if not request.session.session_key:
		request.session.save()
	session_key = request.session.session_key

	try:
		payload = json.loads(request.body.decode('utf-8')) if request.body else {}
	except json.JSONDecodeError:
		return JsonResponse({'error': 'Invalid JSON'}, status=400)

	score = payload.get('score')
	details = payload.get('details', '')
	if score is None:
		return JsonResponse({'error': 'score is required'}, status=400)

	try:
		score_val = float(score)
	except (TypeError, ValueError):
		return JsonResponse({'error': 'score must be a number'}, status=400)

	level, recommendation, target_url, target_label = _compute_level_and_recommendation(score_val)

	result = TestResult.objects.create(
		user=request.user if request.user.is_authenticated else None,
		session_key=session_key,
		score=score_val,
		level=level,
		recommendation=recommendation,
		details=details or ''
	)

	return JsonResponse({
		'id': result.id,
		'score': result.score,
		'level': result.level,
		'recommendation': result.recommendation,
		'target_url': target_url,
		'target_label': target_label,
		'created_at': result.created_at.isoformat(),
	})


def api_recommendation(request):
	# Require either authenticated user or session key
	if not request.session.session_key:
		request.session.save()
	session_key = request.session.session_key

	qs = TestResult.objects.all()
	if request.user.is_authenticated:
		qs = qs.filter(user=request.user)
	else:
		qs = qs.filter(session_key=session_key)

	latest = qs.order_by('-created_at').first()
	if not latest:
		return JsonResponse({'message': 'No recommendation yet'}, status=404)

	return JsonResponse({
		'id': latest.id,
		'score': latest.score,
		'level': latest.level,
		'recommendation': latest.recommendation,
		# Recompute mapping for convenience in fetch API
		**(lambda m: {'target_url': m[2], 'target_label': m[3]})(_compute_level_and_recommendation(latest.score)),
		'created_at': latest.created_at.isoformat(),
	})


# Make sure to set the GENERATIVE_API_KEY environment variable for this to work.
def api_generate(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8')) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    message = payload.get('message')
    prompt = payload.get('prompt')

    if not message or not prompt:
        return JsonResponse({'error': 'message and prompt are required'}, status=400)

    api_key = os.environ.get('GENERATIVE_API_KEY')
    if not api_key:
        return JsonResponse({'error': 'The AI is not configured on the server. Please contact the administrator.'}, status=500)

    api_url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'

    body = {
        "system_instruction": {
            "parts": [
                { "text": prompt }
            ]
        },
        'contents': [
            {
                'parts': [
                    { 'text': message }
                ]
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json',
    }

    try:
        resp = requests.post(api_url, headers=headers, json=body, timeout=20)
        resp.raise_for_status() # Raise an exception for bad status codes
        data = resp.json()
        
        # Extract the text from the response
        # Note: The exact path might change based on the API version.
        reply_text = data['candidates'][0]['content']['parts'][0]['text']
        
        return JsonResponse({'reply': reply_text})

    except requests.RequestException as e:
        return JsonResponse({'error': f'Failed to contact the AI service: {str(e)}'}, status=502)
    except (KeyError, IndexError) as e:
        return JsonResponse({'error': f'Could not parse the AI response: {str(e)}'}, status=500)