import json
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from django.contrib import messages
from .forms import CustoUserForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.


def home(request):
    products=Product.objects.filter(trending=1)

    return render(request,'home.html',{'products':products})

def cart_page(request):
   if request.user.is_authenticated:
      cart=Cart.objects.filter(user=request.user)
      return render(request,'cart.html',{'cart':cart}) 
   else:
      return redirect('home')

def remove_cart(request,cid):
   cartid=Cart.objects.get(id=cid)
   cartid.delete() 
   return redirect("cart")


def addto_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
      if request.user.is_authenticated:
         data=json.load(request)
         product_qty=data['product_qty']
         product_id=data['product_id']
         #print(request.user.id)
         product_status=Product.objects.get(id=product_id)
         if product_status:
            if Cart.objects.filter(user=request.user,product_id=product_id):
                return JsonResponse({'status':'product already in cart'},status=200)
            else:
               if product_status.quantity>=product_qty:
                  Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                  return JsonResponse({'status':'Product added in cart'},status=200)
               else:
                  return JsonResponse({'status':'Product stock not available'},status=200)
         else:
            return JsonResponse({'status':'no product found'},status=200)
         return JsonResponse({'status':'product added'},status=200)
      else:
         return JsonResponse({"status":"please login"},status=200)

   else:
      return JsonResponse({'status':'Invalid access'},status=200) 
   
def fav_page(request):
   if request.user.is_authenticated:
      fav=favourite.objects.filter(user=request.user)
      return render(request,'fav.html',{'fav':fav})
   
def addto_fav(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
      if request.user.is_authenticated:
         data=json.load(request)
         fav_prd=data['fav_prd']
         product_status=Product.objects.get(id=fav_prd)
         if product_status:
             if favourite.objects.filter(user=request.user,product_id=fav_prd):
                
                return JsonResponse({'status':'product already in fav'},status=200)
             else:
                  favourite.objects.create(user=request.user,product_id=fav_prd)
                  return JsonResponse({'status':'Product added in fav'},status=200)
         else:
            return JsonResponse({'status':'product not available'},status=200)
      else:
          return JsonResponse({'status':'login please'},status=200)
      
   else:
      return JsonResponse({'status':'Invalid access'},status=200) 

def rmfav(request,fid):
   fav_prd=favourite.objects.get(id=fid)
   fav_prd.delete()
   return redirect('fav')

   

def logout_page(request):


   if request.user.is_authenticated:
      logout(request)
      messages.success(request,"logout successfully")
   return redirect("home")   
def login_page(request):
   if request.user.is_authenticated:
      return redirect('home')
   else:
     if request.method=='POST':
       name=request.POST.get('username')
       pwd=request.POST.get('password')
       user=authenticate(request,username=name,password=pwd)
       if user is not None:
         login(request,user)
         messages.success(request,"login successfully")
         return redirect('home')

       else:
         messages.error(request,"invalid username or password")   
         return redirect('login')


   return render(request,'login.html')
def register(request):
    forms=CustoUserForm()
    if request.method=='POST':
       forms=CustoUserForm(request.POST)
       if forms.is_valid():
          forms.save()
          messages.success(request,"Registeration Success")
          return redirect('login')
    return render(request,'register.html',{'forms':forms})
def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,'collections.html',{'catagory':catagory})
def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
      products=Product.objects.filter(category__name=name)
      return render(request,'products/index.html',{'products':products,"catagory_name":name})
    else:
      messages.warning(request,'No such a category')
      return redirect('collections')

def productview(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)): 
       if(Product.objects.filter(name=pname,status=0)):
          products=Product.objects.filter(name=pname,status=0).first()
          return render(request,'products/productview.html',{"products":products})
       else:
          messages.warning('No such a product found')
          return redirect('collections')
    else:        
       messages.warning('No such a catagory found')
       return redirect('collections')