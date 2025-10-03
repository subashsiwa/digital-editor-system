from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE_OWNER = 'owner'
    ROLE_EDITOR = 'editor'
    ROLE_DESIGNER = 'designer'
    ROLE_AUTHOR = 'author'
    
    ROLE_CHOICES = [
        (ROLE_OWNER, 'Владелец'),
        (ROLE_EDITOR, 'Редактор'),
        (ROLE_DESIGNER, 'Дизайнер'),
        (ROLE_AUTHOR, 'Автор'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_AUTHOR,
        verbose_name='Роль'
    )
    
    bio = models.TextField(blank=True, verbose_name='Биография')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="journal_user_set",
        related_query_name="journal_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="journal_user_set",
        related_query_name="journal_user",
    )
    
    def is_owner(self):
        return self.role == self.ROLE_OWNER or self.is_superuser
    
    def is_editor(self):
        return self.role == self.ROLE_EDITOR or self.is_owner()
    
    def is_designer(self):
        return self.role == self.ROLE_DESIGNER or self.is_editor()
    
    def is_author(self):
        return self.role == self.ROLE_AUTHOR or self.is_designer()
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-адрес')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'

class ArticleManager(models.Manager):
    def for_user(self, user):
        if user.is_owner() or user.is_editor():
            return self.all()
        elif user.is_designer():
            return self.filter(status__in=[Article.APPROVED, Article.PUBLISHED])
        elif user.is_author():
            return self.filter(author=user)
        else:
            return self.none()

class Article(models.Model):
    DRAFT = 'draft'
    UNDER_REVIEW = 'under_review'
    APPROVED = 'approved'
    PUBLISHED = 'published'
    
    STATUS_CHOICES = [
        (DRAFT, 'Черновик'),
        (UNDER_REVIEW, 'На проверке'),
        (APPROVED, 'Одобрено'),
        (PUBLISHED, 'Опубликовано'),
    ]
    
    # Основные поля
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Рубрика'
    )
    
    # Статус и даты
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=DRAFT,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    # Менеджер объектов
    objects = ArticleManager()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    target_text = models.TextField(blank=True, verbose_name='Комментируемый текст')
    
    def __str__(self):
        return f'Комментарий к "{self.article.title}" от {self.author.username}'
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'