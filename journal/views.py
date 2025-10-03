from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Article, Category, Comment
from .forms import ArticleForm, CommentForm
from .decorators import author_required

def home(request):
    """Главная страница - список опубликованных статей"""
    articles = Article.objects.filter(status=Article.PUBLISHED)
    return render(request, 'journal/home.html', {'articles': articles})

def custom_login(request):
    """Кастомная страница входа"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    
    return render(request, 'journal/login.html')

def custom_logout(request):
    """Кастомная функция выхода из системы"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')

@login_required
def dashboard(request):
    """Личный кабинет пользователя"""
    articles = Article.objects.for_user(request.user)
    return render(request, 'journal/dashboard.html', {'articles': articles})

@login_required
@author_required
def create_article(request):
    """Создание новой статьи (только для авторов и выше)"""
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Статья успешно создана!')
            return redirect('dashboard')
    else:
        form = ArticleForm()
    
    return render(request, 'journal/create_article.html', {'form': form})

@login_required
def article_detail(request, article_id):
    """Просмотр деталей статьи"""
    article = get_object_or_404(Article, id=article_id)
    
    # Проверяем права доступа к статье
    user_articles = Article.objects.for_user(request.user)
    if article not in user_articles:
        messages.error(request, 'У вас нет доступа к этой статье.')
        return redirect('dashboard')
    
    return render(request, 'journal/article_detail.html', {'article': article})

@login_required
def edit_article(request, article_id):
    """Редактирование статьи"""
    article = get_object_or_404(Article, id=article_id)
    
    # Проверяем, что пользователь имеет право редактировать статью
    if not (request.user.is_editor() or article.author == request.user):
        messages.error(request, 'У вас нет прав для редактирования этой статьи.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статья успешно обновлена!')
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'journal/edit_article.html', {'form': form, 'article': article})

@login_required
def change_article_status(request, article_id, new_status):
    """Изменение статуса статьи"""
    article = get_object_or_404(Article, id=article_id)
    
    # Проверяем, что пользователь имеет право менять статус
    if not request.user.is_editor():
        messages.error(request, 'У вас нет прав для изменения статуса статей.')
        return redirect('dashboard')
    
    # Проверяем, что новый статус допустим
    if new_status not in dict(Article.STATUS_CHOICES):
        messages.error(request, 'Неверный статус.')
        return redirect('article_detail', article_id=article.id)
    
    article.status = new_status
    article.save()
    
    status_display = article.get_status_display()
    messages.success(request, f'Статус статьи изменен на "{status_display}".')
    
    return redirect('article_detail', article_id=article.id)

@login_required
def add_comment(request, article_id):
    """Добавление комментария к статье"""
    article = get_object_or_404(Article, id=article_id)
    
    # Проверяем, что пользователь имеет доступ к статье
    user_articles = Article.objects.for_user(request.user)
    if article not in user_articles:
        messages.error(request, 'У вас нет доступа к этой статье.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен.')
            return redirect('article_detail', article_id=article.id)
    else:
        form = CommentForm()
    
    return render(request, 'journal/add_comment.html', {'form': form, 'article': article})