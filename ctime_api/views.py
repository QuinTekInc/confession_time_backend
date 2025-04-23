from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *  #to give a status to a json response.
from .serializer import *
from confessions.models import *
from confessions import utils
from confession_time import settings



#import some of the code files in the application.
@api_view(['GET'])
def getEnpoints(request):

    endpoints_dict_list: list = [

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
            'endpoint': '/verify-code-sent/<str:emailAddress>/c=<str:vcode>/',
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
            'decription': 'Logs a user into his account. [Change the status of user to true]'
        },

        {
            'endpoint': '/logout/<str:username>',
            'method': 'PUT',
            'decription': 'Logs a user out of his account. [Change the user status to false]'
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
            'endpoint': '/add-msg/recv=<str:username>',
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
            'endpoint': '/get-msg/recv=<str:username>/marked=<str:bookmarked>',
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
            'endpoint': '/add-report/',
            'method': 'post',
            'body': 'a map of Reports model object without the Id',
            'description': 'Adds a user report to the database'
        },

        {
            'endpoint': '/add-review/',
            'method': 'post',
            'body': 'a map of Review model object without the Id',
            'description': 'Adds a user\'s review of the app to the database'
        },

        {
            'endpoint': '/report-confession/',
            'method': 'post',
            'body': 'a map of ConfessionReport object with the confession_id field.',
            'description': 'Adds a confession_report to the database.'
        }

    ]

    return Response(endpoints_dict_list)


@api_view(['GET'])
def verifyUser(request, username, email):
    
    user = User.objects.filter(username=username, email=email)
    user_list = list(user)

    return Response({'exists': bool(user_list)})


@api_view(['GET'])
def verifyUsername(request, newUsername):
    users = User.objects.filter(username=newUsername)

    #convert the filters objects into list
    users_list = list(users)

    exists = bool(users_list)  #returns False when the list is empty and returns True when the list is not empty

    return Response({'exists': exists})


#send an email to the emailAddress the user specifies.
@api_view(['GET', 'POST'])
def sendEmail(request, emailAddress):

    #generates a six-digit otp code for the user's account creation
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

    return Response(utils.detailFormat('Your message has been sent'))


#verify the last code sent to a user's email
@api_view(['GET'])
def verifyCodeSent(request, emailAddress, vcode):

    #decrypt the verificiation code
    vcode = utils.decryptStr(vcode)

    email_verification = EmailVerification.objects.filter(email=emailAddress).last()
    verification_code = email_verification.verification_code

    if vcode != verification_code:
        return Response(utils.detailFormat('Incorrect verification code'), status=HTTP_404_NOT_FOUND)

    return Response(utils.detailFormat('Correct verification code'))


#for the signup of the user

@api_view(['GET', 'POST'])
def signup(request):

    data = request.data

    serialized = UserAuthSerializer(data=data)

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

    print(f'Data: {data},\nDecrypted Password: {password}')

    try:

        user = User.objects.get(username=username, password=password)
        user.status = True
        user.save()

        user.email = utils.encryptStr(user.email)
        user.password = utils.encryptStr(user.password)

        serializer = UserAuthSerializer(user)

        return Response(serializer.data)

    except User.DoesNotExist:
        return Response(utils.detailFormat('Incorrect username or password'), status=HTTP_404_NOT_FOUND)

    pass


@api_view(['GET'])
def logout(response, username):
    try:

        user = User.objects.get(username=username)
        user.status = False

        user.save()

        return Response(utils.detailFormat('User logged out succesfully'))

    except User.DoesNotExist:
        return Response(utils.detailFormat('User does not exist'), status=HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def updateUserCredentials(request, username):

    data: dict = request.data

    user = User.objects.get(username=username)

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

        user = User.objects.get(username=username)
        user.username = newUsername
        user.save()


        serialized = UserAuthSerializer(user)

        return Response(serialized)

    except User.DoesNotExist:
        return Response(utils.detailFormat('Could not change the username'), status=HTTP_400_BAD_REQUEST)


#delete the user's information
@api_view(['DELETE'])
def deleteAccount(request, username):
    try:
        user = User.objects.get(username=username)
        #finally delete the user
        user.delete() #will automatically delete every records related to the user.

        return Response(utils.detailFormat('Account successfully deleted'))

    except User.DoesNotExist:
        return Response(utils.detailFormat('User does not exist or has already been deleted'),
                        status=HTTP_404_NOT_FOUND)

    pass


@api_view(['GET'])
def getConfessions(request, recv_username):
    #get the receiver username
    receiver = User.objects.get(username=recv_username)

    confessions = Confession.objects.filter(receiver=receiver)

    #filter out the confessions with reports.
    confessions = list(confessions)

    for confession in confessions:

        try:
            confession_report = ConfessionReport.objects.get(confession_id=confession)

            if confession_report:
                confessions.remove(confession)
                pass

        except ConfessionReport.DoesNotExist:
            continue
            
        pass

    serialized = ConfessionSerializer(confessions, many=True)

    return Response(serialized.data)


@api_view(['GET'])
def getSentConfessions(request, sender_username):
    sender = User.objects.get(username=sender_username)

    #get the sent confession ids from the model.
    sent_confession_ids = UserSentConfession.objects.filter(user=sender)

    sent_confessions = []

    #convert the confession ids to a list of confession objects.
    for confession_id  in sent_confession_ids:
        sent_confessions.append(confession_id.confession)

    serialized = ConfessionSerializer(sent_confessions, many=True)

    return Response(serialized.data)


@api_view(['POST'])
def addConfession(request, recv_username):

    #check if the receiver exists.
    receiver: User = None

    try:
        receiver = User.objects.get(username=recv_username)
    except User.DoesNotExist:
        return Response(f"Receiver: '{recv_username}' does not exist", status=HTTP_404_NOT_FOUND)

    
    #create new confession object with the provided information
    confession = Confession(receiver=receiver, message=request.data['message'])
    confession.save()

    #try to create a sender_confession object.

    try:
        sender_username = request.data['sender']

        if sender_username:
            sender = User.objects.get(username=sender_username)
            userSentConfession = UserSentConfession(user=sender, confession = confession)
            userSentConfession.save()
        
    except KeyError:
        #do nothing when the key error occurs.
        pass

    return Response('Message Sent', status=HTTP_200_OK)


@api_view(['GET'])
def updateConfession(request, confessionID, bookmarked):

    confessionID = int(confessionID)
    bookmarked = True if bookmarked == "true" else False

    confession = Confession.objects.get(confessionID=confessionID)
    confession.bookmarked = bool(bookmarked)

    confession.save()

    serializer = ConfessionSerializer(confession)

    return Response(serializer.data)


@api_view(['DELETE'])
def deleteConfession(request, confessionID):

    confession = Confession.objects.get(confessionID=confessionID)
    confession.delete()

    return Response(f'Confesssion: {confessionID} deleted!')


@api_view(['GET'])
def getSavedUsers(request, username):

    user = User.objects.get(username=username)

    savedUsers = SavedUser.objects.filter(user=user)

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

    savedUser = SavedUser.objects.get(id=savedUserID)

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
        savedUser = SavedUser(id=savedUserID)
        savedUser.delete()
        return Response(utils.detailFormat(f'User deleted succesfully'))
    except SavedUser.DoesNotExist:
        return Response(utils.detailFormat('Information not found'), status=HTTP_404_NOT_FOUND)

    pass


#for reporting a messages.
@api_view(['POST'])
def addReport(request):

    data = request.data

    serialized = ReportSerializer(data=data)

    if not serialized.is_valid():
        return Response(utils.detailFormat('Invalid request.'), status=HTTP_400_BAD_REQUEST)

    serialized.save()

    return Response(serialized.data)


#for  reviewing the rating the application.....and potentially reporting bugs.
@api_view(['POST'])
def addReview(request):

    data = request.data

    serialized = ReviewSerializer(data=data)

    if not serialized.is_valid():
        return Response(utils.detailFormat('Could not add review'), status=HTTP_400_BAD_REQUEST)

    serialized.save()

    return Response(utils.detailFormat('Review has been added'))



@api_view(['POST'])
def reportConfession(request):

    report_data = request.data

    serializer = ConfessionReportSerializer(data=report_data)

    if not serializer.is_valid():
        return Response(utils.detailFormat('Could not report confession. Please try again'))
    

    serializer.save()

    return Response(utils.detailFormat('Confession report has been added.'))