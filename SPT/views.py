from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from . forms import MembersForm,SpendingsForm,SharesForm,User_registerForm
from .models import Members,Spendings,Shares
from django.forms import inlineformset_factory
from . filters import SharesFilter
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .decorators import authenticate_user,un_auth_users
from django.contrib.auth.models import User
from django import forms
# Create your views here.
@authenticate_user
def home(request):       
    # forms
    form1=MembersForm()
    form2=SpendingsForm(initial={'user':request.user})
    # To save all models user field with request.user
    obj=User.objects.get(pk=request.user.id)    
    # inlinform(form3)
    members=Members.objects.filter(user=obj)
    members_count=members.count()
    #To show only filtered member's name in 'name' field
    class SharesFormSet1(forms.ModelForm):
       def __init__(self,*args,**kwargs):
                super(SharesFormSet1,self).__init__(*args,**kwargs)
                self.fields['name'].queryset=self.fields['name'].queryset.filter(user=obj)

    SharesFormSet=inlineformset_factory(Spendings,Shares,form=SharesFormSet1,fields=('name','amount'),extra=members_count,can_delete=False)
    form3=SharesFormSet()
    
    # filter login user's spending details from Spendings model
    spendings=Spendings.objects.filter(user=obj)
    total_spent_count=spendings.count()
    # to get last 5 updates from spendings
    spendings1=spendings[::-1]
    spendings1=spendings1[:5]
    #end last 5     
    # variable assignment
    overall_amount_spent=0
    members_shares=[]    
    # create a list by members name
    members_name=[]
    for member in members:              
        members_name.append(member.name)

    # To findout overall amount spent
    for sp in spendings:
        overall_amount_spent+=sp.total

    # from remove_spending view & spending_confirm_delete.html ,when user click cancel it will redirect 
    #to the page where they give request to delete.    
    # and in spending_confirm_delete.html <a class="btn btn-warning" href="{% url 'home' %}?next=({{request.GET.next}})">Cancel</a>
    next=request.GET.get('next')    
    if next:
        for i in next:                               
            if i =='1':
                return redirect('consolidate')                      
            
                         
   # post method handling
   #                     # 
    if request.method=='POST':
        if request.POST.get('form_1')=='1':
            form1=MembersForm(request.POST)
            if form1.is_valid():
                member_instance=form1.save()
                member_instance.user=obj
                member_instance.save()
                messages.info(request," Member added successfully...!")                
                return redirect("home")
        elif request.POST.get('form_2')=='2':
            form2=SpendingsForm(request.POST)
            if form2.is_valid():
                spending_instance=form2.save()
                spending_instance.user=obj
                spending_instance.save()
                form3=SharesFormSet(request.POST,instance=spending_instance)
                if form3.is_valid():
                    form3.save()                                        
                    messages.info(request,"details added....! ")                   
                    return redirect("home")
                    
            messages.warning(request,"Enter a required field")   
            return redirect("home")                                                                
               
    else:                   
        
        context={'form1':form1,'form2':form2,'form3':form3,'members':members,'spendings':spendings1,'overall_amount_spent':overall_amount_spent,'total_spent_count':total_spent_count}
        return render(request,"SPT/home.html",context)
@authenticate_user
def consolidate(request):
    # create a dictionary with the key of available members's name,
    # and a empty list as Values.
    members_shares={}
    members_shares2={}
    members_shares3={}
    obj=User.objects.get(pk=request.user.id)
    members=Members.objects.filter(user=obj)
    members_count=members.count()
    for member in members:
        members_shares[member.name]=[]
    # filter form for Spendings model
    total=0
    spendings=Spendings.objects.filter(user=obj)       
    myfilter=SharesFilter(request.GET,queryset=spendings)
    spendings=myfilter.qs
    # to find every member's share depend on the filtersearch 
    shares=[]
    for spend in spendings:
        total+=(spend.total)
    # to find equal share amount for every member depend on the filtersearch   
    equal=total/members_count
    equal=round(equal,2)
    equal2=-equal
    
    
    
    
    for sp in spendings:      
        # to findout individual shares 
        individual_shares=Shares.objects.filter(spends=sp)
        shares+=Shares.objects.filter(spends=sp)
        # To store the each members each spent amount in list as values and member's names as key in members_shares dictionary
        #we created list with members name as key before:
        if individual_shares:
            for i in individual_shares:                
                members_shares[i.name.name].append(i.amount)               
    
    # to find out the each members total spent amount from
    #list of spent  in members_shares dict.
    for key,values in members_shares.items():
        members_shares2[key]=sum(values)
        # in consolidate page to show consolidate value(we used key,value in con.result view) with string
        x=sum(values)
        y=members_shares2[key]-equal
        y=round(y,2)        
        if y<0:
            messages.warning(request,"")
            members_shares3[key]="need to be share  {}".format(-y)
        elif y>0:
            messages.info(request,"")
            members_shares3[key]="additionally shared  {}".format(y)

    context={'members':members,'myfilter':myfilter,'spendings':spendings,'members_shares2':members_shares2,'members_shares3':members_shares3,'total':total,'equal':equal,'equal2':equal2,'shares':shares}
    return render(request,"SPT/consolidation_page.html",context)

@authenticate_user
def spendings_update(request,pk):
    spending=Spendings.objects.get(id=pk)
    form=SpendingsForm(instance=spending)
    # used html elements for form field so,set default value in
    #date type in html we need below format
    date=spending.date
    date1=date.strftime('%Y-%m-%d')
    if request.method=="POST":
        form=SpendingsForm(request.POST,instance=spending)
        if form.is_valid():
            form.save()
            messages.info(request,"Spending details updated...")
            next=request.POST.get('next')            
            if next:                
                return redirect('consolidate')
            else:
                return redirect('home')           
    return render(request,"SPT/spendings_update.html",{'form':form,'spending':spending,'date':date1})
@authenticate_user
def member_share_update(request,pk):
    members_count=Members.objects.filter(user=request.user).count()        
    spend=Spendings.objects.get(id=pk)
    # con.page members update form with instance, shows field only if it is already saved
    # to show empty form if member's field not saved before 
    shares=Shares.objects.filter(spends=spend) 
    x=[]
    for share in shares:
        x.append(share.name)
    if len(x)>0:
        ct=0
    else:
        ct=members_count
        
    #To show only filtered member's name in 'name' field
    obj=User.objects.get(pk=request.user.id)
    class SharesFormSet1(forms.ModelForm):
       def __init__(self,*args,**kwargs):
                super(SharesFormSet1,self).__init__(*args,**kwargs)
                self.fields['name'].queryset=self.fields['name'].queryset.filter(user=obj)

    SharesFormSet=inlineformset_factory(Spendings,Shares,form=SharesFormSet1,fields=('name','amount'),extra=ct,can_delete=False)
    form3=SharesFormSet()    
    # using instance to get form with filled field that we want to update
    form3=SharesFormSet(instance=spend)
    if request.method=="POST":
        form3=SharesFormSet(request.POST,instance=spend)               
        if form3.is_valid():
            form3.save()
            messages.info(request,"Member's Shares updated...")
            #update request can came from home page & consolidate page. after update completed
            #we have to redirect the user to respected page,when user give update request from page we have to
            #pass the value.based on the value we can redirect to the respective page
            # we only pass value for next from con.page.html <td><a class="btn btn-sm btn-info" href="{% url 'share_update' spend.id %}?next=(1)">Update</a></td>
            # in member_share_update.html <input type="hidden"  name="next"  value="{{request.GET.next}}">
            next=request.POST.get('next')            
            if next:                
                return redirect('consolidate')
            else:
                return redirect('home')
          
                        
            
    return render(request,"SPT/member_share_update.html",{'form':form3})

@un_auth_users
def register(request):
    form=User_registerForm()
    if request.method=="POST":
        form=User_registerForm(request.POST)
        if form.is_valid():
            # to check user given email id is already exist in register page
            Email=form.cleaned_data['email']
            if User.objects.filter(email=Email).exists():
                messages.warning(request,"email id already exist")
                return redirect("register")
            else:
                form.save()
                return redirect("login")
    return render(request,'SPT/register.html',{'form':form})
@un_auth_users
def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.warning(request,"username or password incorrect")
    return render(request,"SPT/login.html")
@authenticate_user
def user_logout(request):
    logout(request)
    return redirect("login")

@authenticate_user
def remove_member (request,pk):
    member=Members.objects.get(id=pk)
    if request.method=="POST":
        member=Members.objects.get(id=pk)
        member.delete()
        messages.warning(request,"Member has been removed...")
        return redirect("home")
    return render(request,"SPT/member_confirm_delete.html")
@authenticate_user
def remove_spending (request,pk):
    if request.method=="POST":
        spendings=Spendings.objects.get(id=pk)
        spendings.delete()
        messages.warning(request,"spending detail has been removed...")
        next=request.POST.get('next')
        # in con.page.html <td><a class="btn btn-sm btn-danger" href="{% url 'remove_spending' spend.id %}?next=1">Delete</a></td>
        # in spending_confirm_delete.html <input type="hidden" name="next" value="{{request.GET.next}}">
        if next:            
            return redirect('consolidate')
        else:
            return redirect("home")
    return render(request,"SPT/spending_confirm_delete.html")  

 


