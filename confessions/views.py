
# required imports

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *
from .models import User, Confession, EmailVerification, SavedUser
from .serializer import UserAuthSerializer, ConfessionSerializer, SavedUserSerializer, ReportSerializer, ReviewSerializer
from django.core.mail import send_mail
from django.conf import settings

from . import utils


# Create your views here.

@api_view(['GET'])
def getEnpoints(request):

    endpoints_dict_list: list =[

        {
            'endpoint': '/endpoints/',
            'method': 'GET',
            'decription': 'Show all enpoints in the api'
        },

        {
            'endpoint': '/verify-user/<str:username>/<str:email>',
            'method': 'GET',
            'description': 'Check whether a user account exists.'
        },

        {
            'endpoint': '/send-email/',
            'method': 'GET',
            'body': '{email}: email',
            'decription': 'Sends a six figure number to specified email for verification'
        },

        {
            'endpoint':'/verify-code-sent/<str:emailAddress>/c=<str:vcode>/',
            'method': 'GET',
            'description': 'Compares the sent verification code'
        },

        {
            'endpoint': '/verify-username/<str:username>',
            'method': 'GET',
            'description': 'Checks whether a username exists in the database'
        },

        {
            'endpoint': '/signup/',
            'method': 'POST',
            'body': 'map of user object',
            'decription': 'Show all enpoints in the api'
        },

        {
            'endpoint': '/login/<str:username>',
            'method': 'PUT',
            'decription': 'Change the status of user to true'
        },


        {
            'endpoint': '/logout/<str:username>',
            'method': 'PUT',
            'decription': 'Change the user status to false'
        },

        {
            'endpoint': '/update-user-cred/',
            'method': 'PUT',
            'decription': 'update the user credentials'
        },

        {
            'endpoint': '/delete-account/<str:username>',
            'method': 'DELETE',
            'description': 'Deletes a user account record from the database'
        },

        {
            'endpoint': '/send-msg/recv=<str:username>',
            'method': 'POST',
            'body': 'map of a confession object',
            'decription': 'Send a message to a recipient'
        },

        {
            'endpoint': '/get-msg/recv=<str:username>',
            'method': 'GET',
            'decription': 'Get user\'s received messages'
        },

        {
            'endpoint': '/get-msg/sender=<str:username>',
            'method': 'GET',
            'description': 'Get the user\'s sent messages',
        },

        {
            'endpoint': '/get-meg/recv=<str:username>/marked=<str:bookmarked>',
            'method': 'GET',
            'decription': 'Show the bookmarked messages'
        },

        {
            'endpoint': '/update-msg/<str:id>/marked=<int:marked>',
            'method': 'GET',
            'decription': 'update message bookmark status (1 for true and 0 for false)'
        },

        {
            'endpoint': '/delete-msg/<str:id/',
            'method': 'DELETE',
            'decription': 'Show all enpoints in the api'
        },

        {
            'endpoint': '/get-saved-users/usr=<str:username>',
            'method': 'PUT',
            'decription': 'Get a list of saved users belonging to a particular account'
        },

        {
            'endpoint': '/save-user-detail/',
            'method': 'PUT',
            'body': 'A map of SavedUser object',
            'decription': 'Save a user detail with thier username and a name you can use to rememeber them'
        },

        {
            'endpoint': '/update-user-detail/<str:id>',
            'method': 'PUT',
            'body': 'a map of SavedUser object',
            'decription': 'Update the saved user information'
        },

        {
            'endpoint': '/delete-saved-user/<str:id>',
            'method': 'PUT',
            'decription': 'delete the saved user information'
        },

        {
            'enpoint': '/add-report/',
            'method': 'post',
            'body': 'a map of Reports model object without the Id',
            'description': 'Adds a user report to the database'
        },

        {
            'enpoint': '/add-review/',
            'method': 'post',
            'body': 'a map of Review model object without the Id',
            'description': 'Adds a user\'s review of the app to the database'
        },
       
    ]


    return Response(endpoints_dict_list)


@api_view(['GET'])
def verifyUser(request, username, email):

    user = User.objects.filter(username = username, email = email)

    user_list = list(user)

    return Response({'exists': bool(user_list)})



@api_view(['GET'])
def verifyUsername(request, newUsername):

    users = User.objects.filter(username=newUsername)

    #convert the filters objects into list
    users_list = list(users)

    exists = bool(users_list) #returns False when the list is empty and returns True when the list is not empty

    return Response({'exists': exists})



#send an email to the emailAddress the user specifies.
@api_view(['GET', 'POST'])
def sendEmail(request, emailAddress):

    #get the random number
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
       email = emailAddress,
       verification_code = verification_code
    )

    email_verification.save()


    return Response(utils.detailFormat('Your message has been sent'))


#verify the last code sent to a user email
@api_view(['GET'])
def verifyCodeSent(request, emailAddress, vcode):

    email_verification = EmailVerification.objects.filter(email = emailAddress).last()
    verification_code = email_verification.verification_code

    if vcode != verification_code:
        return Response(utils.detailFormat('Incorrect verification code'), status = HTTP_404_NOT_FOUND)

    return Response(utils.detailFormat('Correct verification code'))


#for the signup of the user

@api_view(['GET','POST'])
def signup(request):

    data = request.data

    serialized = UserAuthSerializer(data = data)

    if not serialized.is_valid():
        return Response()
    
    serialized.save()

    return Response(serialized.data)
    

@api_view(['PUT'])  
def login(request):

    data: dict = request.data

    username: str = data['username']
    password: str = data['password']

    #decrypt the password
    password = utils.decryptStr(password)

    try:

        user = User.objects.get(username = username, password = password)
        user.status = True
        user.save()

        user.email = utils.encryptStr(user.email)
        user.password = utils.encryptStr(user.password)

        serializer = UserAuthSerializer(user)

        return Response(serializer.data)

    except User.DoesNotExist:
        return Response(utils.detailFormat('Incorrect username or password'), status = HTTP_404_NOT_FOUND)

    pass


@api_view(['GET'])
def logout(response, username):

    try:

        user = User.objects.get(username = username)
        user.status = False

        user.save()

        return Response(utils.detailFormat('User logged out succesfully'))

    except User.DoesNotExist:
        return Response(utils.detailFormat('User does not exist'), status=HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def updateUserCredentials(request, username):

    data: dict = request.data

    user = User.objects.get(username = username)

    if 'email' in data:
        user.email = utils.decryptStr(data['email'])

    if 'password' in data:
        user.password = utils.decryptStr(data['password'])

    #decrypt the username
    user.save()

    #scramble the data and return it to the user
    user.email = utils.encryptStr(user.email)
    user.password = utils.encryptStr(user.password)

    userSerializer = UserAuthSerializer(user)

    return Response(userSerializer.data)


@api_view(['GET'])
def updateUsername(request, username, newUsername):
    try:
        user = User.objects.get(username = username)
        user.username = newUsername

        user.save()

        return Response(utils.detailFormat('Username has been changed'))

    except User.DoesNotExist:
        return Response(utils.detailFormat('Could not change the username'), status=HTTP_400_BAD_REQUEST)



#delete the user's information
@api_view(['DELETE'])
def deleteAccount(request, username):

    try:
        user = User.objects.get(username = username)

        #all the user's sent and received confessions
        sentConfessions = Confession.objects.filter(sender = user)
        receivedConfessions = Confession.objects.filter(receiver = user)

        #delete the confessions associated with the user.
        sentConfessions.delete()
        receivedConfessions.delete()

        # all the user's saved users
        savedUsers = SavedUser.objects.filter(user=user)
        savedUsers.delete()

        #finally delete the user
        user.delete()
        return Response(utils.detailFormat('Account successfully deleted'))

    except User.DoesNotExist:
        return Response(utils.detailFormat('User does not exist or has already been deleted'), status= HTTP_404_NOT_FOUND)

    pass

@api_view(['GET'])
def getConfessions(request, recv_username):

    #get the receiver username
    receiver = User.objects.get(username = recv_username)

    confessions = Confession.objects.filter(receiver = receiver)

    #encrypt the sender's username
    for confession in confessions:
        sender = confession.sender
        sender.username = utils.encryptStr(sender.username)
        confession.sender = sender 
        pass


    serialized = ConfessionSerializer(confessions, many=True)

    return Response(serialized.data)


@api_view(['GET'])
def getSentConfessions(request, sender_username):

    sender = User.objects.get(username = sender_username)

    confessions = Confession.objects.filter(sender = sender)

    serialized = ConfessionSerializer(confessions, many= True)

    return Response(serialized.data)


@api_view(['POST'])
def addConfession(request):

    data = request.data

    sender: User = None

    try:
        sender = User.objects.get(username = data['sender'])
    except User.DoesNotExist:
        return Response(f'Sender {data["sender"]} does not exist', status = HTTP_404_NOT_FOUND)
    
    
    receiver: User = None

    try:
        receiver = User.objects.get(username = data['receiver'])
    except User.DoesNotExist:
        return Response(f'Receiver {data["receiver"]} does not exist', status = HTTP_404_NOT_FOUND)
    

    if sender == receiver:
        return Response('You cannot send message to yourself', status=HTTP_403_FORBIDDEN)
    
    serialized = ConfessionSerializer(data=data)

    if not serialized.is_valid():
        return Response('Invalid Request')
    
    serialized.save()
    return Response(serialized.data)


@api_view(['GET'])
def updateConfession(request, confessionID, bookmarked):

    confessionID = int(confessionID)
    bookmarked = True if bookmarked == "true" else False

    confession = Confession.objects.get(confessionID = confessionID)
    confession.bookmarked = bool(bookmarked)

    confession.save()

    serializer = ConfessionSerializer(confession)

    return Response(serializer.data)


@api_view(['DELETE'])
def deleteConfession(request, confessionID):

    confession = Confession.objects.get(confessionID = confessionID)
    confession.delete()

    return Response(f'Confesssion: {confessionID} deleted!')


@api_view(['GET'])
def getSavedUsers(request, username):

    user = User.objects.get(username = username)

    savedUsers = SavedUser.objects.filter(user = user)

    savedUserSerializer = SavedUserSerializer(savedUsers, many=True)

    return Response(savedUserSerializer.data)


@api_view(['POST'])
def addSavedUser(request):

    data = request.data

    serialized = SavedUserSerializer(data=data)

    if not serialized.is_valid():
        return Response(utils.detailFormat('An error occurred'))

    serialized.save()
    return Response(serialized.data)


@api_view(['PUT'])
def updateSavedUser(request, savedUserID):

    data = request.data

    savedUser = SavedUser.objects.get(id = savedUserID)

    if data['name']:
        savedUser.name = data['name']

    if data['username']:
        savedUser.username = data['username']
    
    savedUser.save()

    serialized = SavedUserSerializer(savedUser)

    return Response(serialized.data)

@api_view(['DELETE'])
def deleteSavedUser(request, savedUserID):

    try:
        savedUser = SavedUser(id = savedUserID)
        savedUser.delete()
        return Response(utils.detailFormat(f'User deleted succesfully'))
    except SavedUser.DoesNotExist:
        return Response(utils.detailFormat('Information not found'), status= HTTP_404_NOT_FOUND)
    
    pass
    


@api_view(['POST'])
def addReport(request):

    data = request.data

    serialized = ReportSerializer(data = data)

    if not serialized.is_valid():
        return Response(utils.detailFormat('Invalid request.'), status = HTTP_400_BAD_REQUEST)

    serialized.save()

    return Response(serialized.data)



@api_view(['POST'])
def addReview(request):
    data = request.data

    serialized = ReviewSerializer(data = data)

    if not serialized.is_valid():
        return Response(utils.detailFormat('Could not add review'), status=HTTP_400_BAD_REQUEST)

    serialized.save()

    return Response(utils.detailFormat('Review has been added'))