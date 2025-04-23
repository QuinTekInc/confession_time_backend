
# required imports
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import *
from .forms import CreateUserForm, LoginUserForm
from . import utils



#set the current user object as global variable.
currentUser = None

#login page.
def loginPage(request):

    form = LoginUserForm()

    context = {'loginForm': form}

    if request.method == 'POST':
        form = LoginUserForm(request.POST)

        if not form.is_valid():
            #display the error messages.
            messages.error(request, form.errors.as_text)
            pass

        username =  form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = User.objects.get(username=username, password=password)

        if user.DoesNotExist:
            messages.error(request, 'Incorrect username or password plese try again')
            pass

        #todo: redirect the user to the homepage when the login is successful
        currentuser = user
        pass

    return render(request, 'login.html', context)


#the sign up page.
def signupPage(request):

    form = CreateUserForm()


    context = {'signupForm': form}

    if request.method == 'POST':
        #get the data from the fields in the signup form.
        form = CreateUserForm(request.POST)

        if not form.is_valid():
            #todo: show an error message with indicating the particular error.
            messages.error(request, 'An error occurred. Please try again')
            return
        
        print(form.cleaned_data)

        #todo: redirect the user to the e-mail confirmation page.
        return redirect('sendmail')

    return render(request, 'signup.html', context)



#this function sends the verification code the user's email account
def sendEmail(request, emailAddress: str) -> bool:

    verification_code = utils.generateRandomNumber()

    subject = 'Confession Time, Account Verification'
    message = f"Your email's verification code is \n\n{verification_code}.\n\nDo not share with anyone"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [emailAddress]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=True
    )

    email_verification = EmailVerification.objects.create(
        email=emailAddress,
        verification_code=verification_code
    )

    email_verification.save()

    context = {
        'email': emailAddress,
        'verificationCode': verification_code
    }

    return redirect(request ,'vcode_entry.html', context)



def verifyEmail(request):

    context = {'email': 'quinsefalloyd@gmail.com'}

    return render(request, 'vcode_entry.html', context)



#for sending a confession to a receiver.
def sendMessage(request, recv_username: str):

    if request.method == 'POST':

        #retrieve the message the person entered in the text-area of the form in the template.
        message = request.POST.get('message-entry')

        #check if the message is empty.
        if not len(message):
            messages.error(request, 'Messages field not be left blank')
            return
        
        #encrypt the message.
        message = utils.encryptStr(message)

        #get the receiver object.
        receiver = User.objects.get(username = recv_username)

        #create a confession object with the receiver and encrypted message and save it.
        confession = Confession.objects.create(receiver=receiver, message=message)

        #save the confession to the database.
        confession.save()

        messages.success(request, 'Confession has been sent sucessfully.')

    #context dictionary to be passed to the template.
    context = {
        'receiver': recv_username,
    }

    #render the enter message template to the screen.
    return render(request, 'enter_message.html', context)


    # Honestly I don't know what to do now.

