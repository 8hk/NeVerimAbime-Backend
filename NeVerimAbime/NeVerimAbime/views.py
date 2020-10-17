# Created by keremocakoglu at 30-Apr-20
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from requests import auth

from NeVerimAbime.forms import LoginForm


def loginPage(request):
    return render(request,'home.html',{})

def home(request):
    return render(request,'my-profile-feed.html',{})

def render_to_response(param, csrfContext):
    pass

# form = LoginForm(request.POST)
#         user = authenticate(username=request.POST['username'], password=request.POST['password'])
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('travel:main')
#             form = self.form_class(None)
#             return render(request, self.template_name, {'form': form})
@csrf_protect
def view_login(request):
    # def post(self, request):
    #     form = self.form_class(request.POST)
        form = LoginForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request,user)
                #todo değiştir
                # return redirect('/')
                # return redirect('/')
                # return render(request,"my-profile-feed.html")
                return redirect(request.GET.get('next', 'home'))
            form = request.form_class(None)
            return render(request, request.template_name, {'form': form})

    # if request.method == "POST":
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         user = auth.authenticate(
    #             username=form.cleaned_data["id_username"],
    #             password=form.cleaned_data["id_password"])
    #         auth.login(request, user)
    #         return HttpResponseRedirect("/")
    # else:
    #     form = LoginForm()
    #
    # return render(request, 'home2.html', {'form': form})
     # return render_to_response('nutrients.html', csrfContext)