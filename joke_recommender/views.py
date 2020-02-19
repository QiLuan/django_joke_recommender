

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms

from .models import Joke, Rating
# Create your views here.
from .recommender import recommender 
from .customUserCreationForm import CustomUserCreationForm




def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})	

def index(request):
	jokes = Joke.objects.all()
	d = {}
	if request.user.is_authenticated:
		ratings = Rating.objects.filter(user = request.user)
		for rating in ratings:
			d[int(rating.joke.id)] = int(rating.rating)
	try:
		recommendation = [Joke.objects.get(pk = joke_id) for joke_id in recommender(d)]
	except:
		recommendation = []
	template = loader.get_template('joke_recommender/index.html')
	context = {
		'jokes': jokes,
		'noRating': len(d) == 0,
		'ratedAll': len(d) == 100,
		'hasRecommendation': len(recommendation) != 0,
		'recommendation': recommendation,
		'numRec': len(recommendation),
	}
	return HttpResponse(template.render(context, request))

def detail(request, joke_id):
	try:
		joke = Joke.objects.get(pk = joke_id)
	except Joke.DoesNotExist:
		raise Http404("Joke doe not exist")

	if request.user.is_authenticated:
		try:
			rating = Rating.objects.get(user = request.user, joke = joke)
			isRated = True
			rate = int(rating.rating)
		except Rating.DoesNotExist:
			isRated = False
			rate = None
	else:
		isRated = False
		rate = None
	return render(request, 'joke_recommender/detail.html', {'joke': joke, 'isRated': isRated, 'rate': rate, 'nums': [ (4-i) for i in range(4)], 'numsRev': [-(i+1) for i in range(4)]})


@login_required
def ratings_view(request):
	model = Rating
	template = 'joke_recommender/rating.html'
	ratings = model.objects.filter(user = request.user).order_by('joke')
	return render(request, template, {'ratings': ratings})

@login_required
def rate(request, joke_id):
	try:
		joke = Joke.objects.get(pk = joke_id)
	except Joke.DoesNotExist:
		raise Http404("Joke does not exist")
	rating = request.POST['rating']
	try:
		r = Rating.objects.get(joke = joke, user = request.user)
		r.rating = max(-5, min(5,int(rating)))
	except Rating.DoesNotExist:
		r = Rating(user = request.user, joke = joke, rating = max(-5, min(5,int(rating))))
	r.save()
	return HttpResponseRedirect('/jr/my_ratings/')
