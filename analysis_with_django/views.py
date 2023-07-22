from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    error_message = None
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)

                # CHECKING if there is any NEXT param in request.
                # For eg: if i tried to access the reports page
                # next = reports , after login go to reports page.
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('sales:home')
        else:
            error_message = 'Something went wrong'
        
    
    context ={
        'form': form,
        'error_message': error_message
    }
    
    return render(request,'auth/login.html',context)