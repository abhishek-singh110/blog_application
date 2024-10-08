from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import send_mail
from .models import Blog, Tag, Comment, Like
from django.contrib.postgres.search import SearchVector

# this is for required to make the strong password
password_regex_validator = RegexValidator(
    regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[*@^%()!#$])[A-Za-z\d@$!%*#?&]{8,}$',
    message="Password must be at least 8 characters long, contain at least one uppercase letter, one special character, and one digit."
)

# this is for the signup the new user.
def signup(request):
    if request.method == 'POST':
        # Extracting user input from the form
        username = request.POST.get('username')
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validating password confirmation
        if password != confirm_password:
            messages.error(request, 'Password and Confirm Password do not match.')
            return render(request, 'signup.html')
        
        # Validating password against the regex
        try:
            password_regex_validator(password)  # Validate password
        except ValidationError as e:
            messages.error(request, str(e))  # Display validation error message
            return render(request, 'signup.html')

        # Checking if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'signup.html')  # Return to the signup page

        # Creating the user
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully!')
        return redirect('login')  # Redirect to login page after successful signup

    return render(request, 'signup.html')  # Render signup page for GET request

# this is for the login.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('home')  # Change 'home' to your desired view after login
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

# this is showing the blog list and details of the blogs.
@login_required
def home(request):
    tag_search = request.GET.get('tag_search', '')  # Get the search input from the URL
    search_query = request.GET.get('search')
    blog_id = request.GET.get('blog_id') 
    
    if search_query:
        # Perform full-text search on title and content fields
        blogs = Blog.objects.annotate(
            search=SearchVector('title', 'content')
        ).filter(search=search_query).distinct()
    elif tag_search:
        blogs = Blog.objects.filter(tags__name__icontains=tag_search).distinct()
    else:
        blogs = Blog.objects.all()  

    paginator = Paginator(blogs, 3)  # Paginate the blog list
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)

    # Retrieve the full list of blogs for the sidebar
    all_blogs = Blog.objects.all()  

    tags = Tag.objects.all()

    selected_blog = None
    if blog_id:
        selected_blog = get_object_or_404(Blog, id=blog_id)

    return render(request, 'blog.html', {
        'blogs': blogs,  # This is for the current page of blogs
        'all_blogs': all_blogs,  # This is for the sidebar list
        'tags': tags,
        'tag_search': tag_search,
        'selected_blog': selected_blog,
    })

# this is for adding the comments on the blogs.
@login_required
@require_POST
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    content = request.POST.get('content')
    if content:
        comment = Comment.objects.create(blog=blog, author=request.user, content=content)
        return JsonResponse({
            'id': comment.id,
            'content': comment.content,
            'author': comment.author.username,
            'created_at': comment.created_at.strftime('%B %d, %Y, %I:%M %p')
        })
    return JsonResponse({'error': 'Comment content is required'}, status=400)

# this is for add the like on the comments.
@login_required
@require_POST
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    Like.objects.get_or_create(comment=comment, user=request.user)
    return JsonResponse({'likes_count': comment.likes.count()})

# this is for share the blogs through the email.
@login_required
def share_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        recipient_email = request.POST.get('email')
        subject = f"Check out this blog: {blog.title}"
        message = f"Hi,I am {request.user}\n\nI thought you might be interested in this blog: {blog.title}\n\n{blog.content}."
        
        if recipient_email:
            try:
                send_mail(subject, message, 'abhis9169@gmail.com', [recipient_email])
                messages.success(request, 'Blog shared successfully!')
            except Exception as e:
                messages.error(request, f'Error sharing the blog: {e}')
        else:
            messages.error(request, 'Please enter a valid email address.')

    return render(request, 'share_blog.html', {'blog': blog})

# this is for the logout view
def user_logout(request):
    logout(request)  # Log the user out
    return redirect('signup')  