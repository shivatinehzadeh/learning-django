from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DeleteView,View,CreateView,DetailView
from .models import Book,Category,Suggestion,Reserve
from .forms import suggestionForm,RegisterForm,LoginForm,quantityForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import BookSerializers
import json
import requests


class ApiBook(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-id')
    serializer_class = BookSerializers

class GetApi(View):
    template_name='api.html'
    def get(self,request):
        response=requests.get('https://jsonplaceholder.typicode.com/posts').json
        return render(request,self.template_name,context={'response':response})





MERCHANT = ''
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# amount = 1000  # Toman / Required
description = "for sell"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/verify/' # Important: need to edit for realy server.

def send_request(request):
    queryset = Reserve.objects.filter(user=request.user.username)
    p = 0
    t = 0
    for q in queryset:
        if q.takhfif is None:
            p += q.price * q.quantity
        else:
            t += round(q.price - q.price * q.takhfif / 100) * q.quantity
    amount = sum((p, t))

    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request):
    queryset = Reserve.objects.filter(user=request.user.username)
    p = 0
    t = 0
    for q in queryset:
        if q.takhfif is None:
            p += q.price * q.quantity
        else:
            t += round(q.price - q.price * q.takhfif / 100) * q.quantity
    amount = sum((p, t))

    Reserve.objects.filter(user=request.user.username).update(sell=True)
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            return redirect('myApp:template')
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')

def numberOfSell(request):
    reserveOfmySelf=Reserve.objects.filter(user=request.user.username,sell=False).count()
    return (reserveOfmySelf)

# Create your views here.
#
# def base(request):
#     query= Book.objects.all()
#     context={
#         'book':query
#     }
#     return render(request,'base.html',context)


class BookList(ListView):

    def get(self, request, name):
     queryset = Book.objects.filter(catogery=name)
     number = numberOfSell(request)
     variable=0
     CheckQuery = Book.objects.filter(catogery=name).values_list('brand',flat=True).distinct()
     return render(request,self.template_name,context={'query':queryset,'num':number,'i':variable,'check':CheckQuery})

class Base(View):

    template_name = 'base.html'
    def get(self,request):
     queryset = Category.objects.all()

     newest=Book.objects.all().order_by('-id')[:6]
     takhfif=Book.objects.filter(takhfif__isnull=False)
     number=numberOfSell(request)



     context={
         'queryset':queryset,
         'new':newest,
         'takhfif':takhfif,
         'num':number,


     }
     return render(request,self.template_name,context)

#
# def detail_list(request,id):
#     query= Book.objects.filter(id=id)
#     context={
#         'book':query
#     }
#     return render(request,'detail.html',context)


class DetailList(DetailView):
    form_class=quantityForm
    template_name = 'detail.html'
    def get(self, request,name,brand):
     queryset = Book.objects.filter(name=name,brand=brand)
     number = numberOfSell(request)
     form=quantityForm(initial={'quantity':1})
     return render(request,self.template_name,context={
         'query':queryset,'num':number,'form':form
     })



def suggest(request):
    if request.is_ajax():
        form = suggestionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'msg':'success'})
        else:
            return JsonResponse({'msg': 'error'})
    else:
     number = numberOfSell(request)
     form = suggestionForm()
     return render(request, 'suggestion.html', context={'num': number, 'form': form})


# class Suggest(View):
#     template_name='suggestion.html'
#     form_class=suggestionForm
#
#     def get(self,request):
#         number = numberOfSell(request)
#         form=self.form_class()
#         return render(request,self.template_name,context={'num':number,'form':form})
# #
#     def post(self,request):
#      form = suggestionForm(request.POST)
#      if form.is_valid():
#             form.save()
#
#             return  redirect('myApp:suggestion')


#
# class Suggest(CreateView):
#     template_name = 'suggestion.html'
#     form_class=suggestionForm
#     success_url = '/suggest'
#
#     def form_valid(self, form):
#         print(form.cleaned_data)
#         return super().form_valid(form)
#
#     def get(self,request):
#         number=numberOfSell(request)
#         return render(request,self.template_name,context={'num':number,'form':self.form_class})




class Register(CreateView):
    template_name = 'signUp.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user=form.save()
        user.refresh_from_db()
        user.profile.phone=form.cleaned_data.get('phone')
        user.profile.email=form.cleaned_data.get('email')
        user.save()
        password_us=form.cleaned_data.get('password1')
        user=authenticate(username=user.username,password=password_us)
        login(self.request,user)
        messages.success(self.request,'ثبت نام با موفقیت  انجام شد')
        return redirect('myApp:reg')

    def get(self,request):
        number=numberOfSell(request)
        return render(request,self.template_name,context={'num':number,'form':self.form_class})




class Login (View):
    template_name = 'login.html'
    form_class = LoginForm
    def post(self,request):
     username=request.POST['username']
     password=request.POST['password']
     user = authenticate(username=username, password=password)
     if user.is_active:
         login(request,user)
         return redirect('myApp:template')
     return redirect('myApp:log')

    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,context={'form':form})


class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('myApp:template')


class ReserveView(View):

    def post(self, request, name,brand):
        quantityNumber=request.POST['quantity']
        if request.user.is_authenticated:
            inform = Book.objects.filter(name=name)
            temp_price = inform.values_list('price')
            temp_takhfif = inform.values_list('takhfif')
            queryset=Reserve.objects.filter(user=request.user.username,name=name,brand=brand,sell=False)
            tedad=queryset.count()
            if tedad != 0:
               for q in queryset:
                number=sum((q.quantity,int(quantityNumber)))
                Reserve.objects.filter(user=request.user.username,name=name,brand=brand,sell=False).update(quantity=number)
            else:
             reserve = Reserve(name=name, user=request.user.username, price=temp_price, takhfif=temp_takhfif,
                                  quantity=quantityNumber,brand=brand)
             reserve.save()

            return redirect('myApp:detail', name=name,brand=brand)
        else:
            return redirect('myApp:log')





class ShowReserve(ListView):
    template_name = 'show.html'
    def get(self, request):
     if request.user.is_authenticated:
        queryset = Reserve.objects.filter(user=request.user.username,sell=False)
        p=0
        t=0
        for q in queryset:
            if q.takhfif is None:
             p += q.price*q.quantity
            else:
             t += round(q.price-q.price*q.takhfif/100)*q.quantity
        Sum=sum((p,t))
        number = numberOfSell(request)

        return render(request, self.template_name, context={'query': queryset, 'num': number,'total':Sum})
     else:
        return redirect('myApp:log')


class Search(View):
   template_name = 'search_list.html'
   def get(self,request):
       searchquery=request.GET.get('q')
       if searchquery is not None:
           lookups=Q(name__icontains=searchquery)|Q(brand__icontains=searchquery)
           queryset=Book.objects.filter(lookups)
           num=numberOfSell(request)
           return render(request,self.template_name,context={'query':queryset,'num':num})



class CheckSearch(View):
    template_name = 'search_list.html'
    def post(self,request):
        getCheck=request.POST.getlist('brands')
        print(getCheck)
        if getCheck is not None:
         lookups=Q()
         for q in getCheck:
            lookups |= Q(brand__icontains=q)
         queryset = Book.objects.filter(lookups)
         num = numberOfSell(request)
         return render(request, self.template_name, context={'query': queryset, 'num': num})
        else:
             return redirect('myApp:template')
