# Add this to your blog/views.py file:

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def simple_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', 'gregdyche')
        password = request.POST.get('password', 'temp123')
        
        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect('/admin/')
        else:
            return HttpResponse("Login failed")
    
    return HttpResponse(f"""
    <h2>Simple Login Test</h2>
    <form method="post">
        <p>Username: <input type="text" name="username" value="gregdyche"></p>
        <p>Password: <input type="password" name="password" value="temp123"></p>
        <p><input type="submit" value="Login"></p>
    </form>
    <p><a href="/admin/">Go to Admin</a></p>
    """)