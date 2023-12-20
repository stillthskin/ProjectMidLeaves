from matplotlib.style import context
from .theblockchain import Blockchain
import json
from unicodedata import category
from wsgiref.util import request_uri
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile, constestant
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import createUserForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

blockchain = Blockchain()

def mine_block(request):
    prev_block = blockchain.get_last_block()
    prev_proof = prev_block['proof']
    thechain = blockchain.chain
    proof = blockchain.proof_of_work(prev_proof)
    previous_hash = blockchain.hassher(prev_block)
    thedata = blockchain.chain_data()
    block = blockchain.create_block(proof, previous_hash, thedata) 
    print(thechain)
    context = {'message' : 'Congrats block mined',
                'index':block['index'],
                'proof': block['proof'],
                'previous_hash':block['prev_hash'],
                'data':thedata,
                'block':block,
                'chain':thechain
                  }
    #return jsonify(response), 200
    return render(request, "blocks.html", context)


def home(request):
        president_category = constestant.objects.filter(positions="President", approved="True")
        sports_category = constestant.objects.filter(positions="Sports", approved="True")
        total = User.objects.count() 
        context = {
            "president_category":president_category,
            "sports_category":sports_category,
            "total": total
            }
        return render(request, 'index.html',context)
def view_login(request):
    if request.method == 'POST':
        usermame = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=usermame,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            print("user none")
        
        pass
    return render(request, 'login.html')
def view_logout(request):
    logout(request)
    return redirect('login')   
def register(request):
    #form = UserCreationForm()
    form = createUserForm()
    form2 = ProfileForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        form2 = ProfileForm(request.POST)
        if form.is_valid() and form2.is_valid:
            user = form.save()
            userprofile = form2.save(commit=False)
            userprofile.user = user
            userprofile.save()
            
            print("saved success")
        pass
    context = {'form':form,
               'form2':form2}
    return render(request, 'register.html',context)
@login_required(login_url='login')
def user_contest(request):
    theuser = request.user
    
    if request.method == 'POST':
        #user = request.user
        userinfo = User.objects.get(username=theuser)
        fname = userinfo.first_name
        print(fname)
        lname = userinfo.last_name
        email = userinfo.email
        regeid = theuser.profile.regid
        positions = request.POST.get('thecategory')
        thedocument = request.FILES['documents']
        #namethedocs = thedocuments['filename']
        potrait = request.FILES['potrait']
        contestantdetails = constestant(fname=fname,lname=lname,email=email,regeid=regeid,
        positions=positions,thedocument=thedocument,potrait=potrait)
        contestantdetails.save()
        #print(namethedocs)
        pass
    #elif request.method == "GET":
    else:
        userinfo = User.objects.get(username=theuser)
        contfname = userinfo.first_name
        contlname = userinfo.last_name
        contemail = userinfo.email
        contid = theuser.profile.regid
        #uids = User.Item_set()
        context = {"theuser":theuser,
                "userinfo":userinfo,
                "contfname":contfname,
                "contlname":contlname,
                "contemail":contemail,
                "contid":contid}
        return render(request, 'contest.html', context)

        #return contfname, contemail, contlname, contid
    
    return render(request, 'contest.html')
@login_required(login_url='login')
def user_vote(request):
    if request.method == 'POST':
        presidents = request.POST.getlist('presidentcheck')
        sports = request.POST.getlist('sportcheck')
        theuser = request.user
        voterupdated = Profile.objects.get(user=theuser)
        has_voted = voterupdated.voted
        print("Has he/she voted?")
        print(has_voted)
        print(presidents)
        print(sports)
        print(len(presidents))
        print(len(sports))
        if len(presidents) > 1 or len(sports) > 1 or has_voted==True:
            print('spoilt vote')
            validity = "Spoilt Vote"
            #theuser = request.user
            voterupdate = Profile.objects.filter(user=theuser).update(voted=True)
            voterupdated = Profile.objects.get(user=theuser)
            print(voterupdated)
            context = {
                "voterupdated":voterupdated,
                "validity":validity
            }
            return render(request, 'vote.html',context)
        else:
            print('valid vote')
            validity = "vote cast succesfuly"
            voterupdate = Profile.objects.filter(user=theuser).update(voted=True)
            presidentsreg,sportsreg = presidents[0],sports[0]
            currentpresidents = constestant.objects.get(regeid=presidentsreg).votes
            currentsports = constestant.objects.get(regeid=sportsreg).votes
            currentpresidents += 1
            currentsports += 1
            print("presidents votes updated to")
            print(currentpresidents)
            print(currentsports)
            updatepres = constestant.objects.filter(regeid=presidentsreg).update(votes = currentpresidents)
            updatesports = constestant.objects.filter(regeid=presidentsreg).update(votes = currentsports)
            prev_block = blockchain.get_last_block()
            prev_proof = prev_block['proof']
            thechain = blockchain.chain
            proof = blockchain.proof_of_work(prev_proof)
            previous_hash = blockchain.hassher(prev_block)
            thedata = blockchain.chain_data()
            block = blockchain.create_block(proof, previous_hash, thedata) 
    else:
         president_category = constestant.objects.filter(positions="President", approved=True)
         sports_category = constestant.objects.filter(positions="Sports", approved=True)
         context = {
            "president_category":president_category,
            "sports_category":sports_category
            }
         return render(request, 'vote.html',context)
        
            
  
    return render(request, 'vote.html')
def offline_block(request):
    thedata = blockchain.chain_data()
    thedata = json.dumps(thedata)
    hit = {"numb":10}
    hit = json.dumps(hit)
    return HttpResponse(thedata)