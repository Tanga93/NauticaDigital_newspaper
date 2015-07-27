import requests
from django.shortcuts import render
from newspaper.forms import UsuarioForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from newspaper.models import Favoritos_Usuario
from django.http import HttpResponseRedirect


# Create your views here.
def search(request):
    articles = []

    context = RequestContext(request)

    if request.method == "POST":
        keywords = request.POST['keywords']
        keywords_format=keywords.replace(' ', '%20')

        url="http://www.ebi.ac.uk/europepmc/webservices/rest/search/query="+keywords_format+"&resulttype=core&format=json"
        response = requests.get(url)
        data=response.json()
        list_articles = data['resultList']['result']

        for articulo in list_articles:

            try:
                article_id = articulo['id']
                if Favoritos_Usuario.objects.filter(usuario_id=request.user.id, id_articulo=article_id):
                    is_favorite= True
                else:
                    is_favorite= False
            except Exception as e:
                article_id = 'Not available'
                is_favorite = False
            try:
                article_title = articulo['title']
            except Exception as e:
                article_title = 'Not available'

            try:
                article_author = articulo['authorString']
            except Exception as e:
                article_author = 'Not available'

            new_article = [article_id, article_title, article_author, is_favorite]
            articles.append(new_article)

        return render(request, 'newspaper/search.html', {'articles':articles, 'keywords': keywords})
    else:
        return render(request, 'newspaper/search.html', {'articles':articles})


def favorites(request):
    context = RequestContext(request)

    if request.method == "POST":

        try:
            id_add = request.POST['add_id']

            if id_add:
                new_entry = Favoritos_Usuario(id_articulo=id_add, usuario_id=request.user.id)
                new_entry.save()
        except Exception as e:
            print(e)

        try:
            id_delete = request.POST['delete_id']

            if id_delete:
                Favoritos_Usuario.objects.filter(id_articulo=id_delete, usuario_id=request.user.id).delete()
        except Exception as e:
            print(e)

    fav_articles=[]

    for entry in Favoritos_Usuario.objects.filter(usuario_id=request.user.id):
        url="http://www.ebi.ac.uk/europepmc/webservices/rest/search/query=ext_id:"+str(entry.id_articulo)+"&resulttype=core&format=json"
        response = requests.get(url)
        data=response.json()
        article = data['resultList']['result'][0]

        try:
            article_title = article['title']
        except Exception as e:
            article_title = 'Not available'

        try:
            article_author = article['authorString']
        except Exception as e:
            article_author = 'Not available'

        new_article = [entry.id_articulo, article_title, article_author]
        fav_articles.append(new_article)

    return render(request, 'newspaper/favorites.html', {'fav_articles': fav_articles})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/newspaper/')


def detail(request):
    if request.method=="POST":
        id_article=request.POST['id_article']
        previous_page=request.POST['previous_page']

        url="http://www.ebi.ac.uk/europepmc/webservices/rest/search/query=ext_id:"+str(id_article)+"&resulttype=core&format=json"
        response = requests.get(url)
        data=response.json()
        article = data['resultList']['result'][0]

        if Favoritos_Usuario.objects.filter(usuario_id=request.user.id, id_articulo=id_article):
            is_favorite= True
        else:
            is_favorite= False

        try:
            article_title = article['title']
        except Exception as e:
            article_title = 'Not available'

        try:
            article_author = article['authorString']
        except Exception as e:
            article_author = 'Not available'

        try:
            article_abstract = article['abstractText']
        except Exception as e:
            article_abstract = 'Not available'

        return render(request, 'newspaper/detail.html', {'id_article': id_article, 'article_title': article_title,'article_author': article_author,
                                                         'article_abstract': article_abstract, 'previous_page': previous_page, 'is_favorite': is_favorite})


def index(request):
    return render(request, 'newspaper/index.html', {})


def user_login(request):
    context = RequestContext(request)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        usuario = authenticate(username=username, password=password)

        if usuario:
            if usuario.is_active:
                login(request, usuario)
                return render(request, 'newspaper/index.html', {})
            else:
                messages.add_message(request, messages.WARNING, 'Your account is disabled.')
                return render(request, 'newspaper/login.html', {})
        else:
            messages.add_message(request, messages.ERROR, 'The password or the login are wrong')
            return render(request, 'newspaper/login.html', {})
    else:
        return render(request, 'newspaper/login.html', {})


def registro(request):
    context = RequestContext(request)

    success = False

    if request.method == 'POST':
        usuario_form = UsuarioForm(data=request.POST)

        if usuario_form.is_valid():
            usuario = usuario_form.save()

            usuario.set_password(usuario.password)
            usuario.save()

            success = True
        else:
            print(usuario_form.errors)
    else:
        usuario_form = UsuarioForm()

    return render(request, 'newspaper/registro.html', {'usuario_form': usuario_form, 'success': success})
