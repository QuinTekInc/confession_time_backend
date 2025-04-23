from django.db import models

#user the model
class User(models.Model):
    
    username = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    status = models.BooleanField(default=False)

    def __str__(self):

        status_str = 'offline'

        if self.status:
            status_str = 'online'
        

        return f'({self.username}, {self.email}, {status_str})'
    
    def __repr__(self):
        return self.__str__()

    pass



#verification for an email....when a user is either creating a new account or is recovering his account.
class EmailVerification(models.Model):
    
    email = models.EmailField(max_length=100)
    verification_code = models.CharField(max_length=10)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'({self.email}, {self.verification_code})'
    
    def __repr__(self):
        return self.__str__()
    


class SavedUser(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)

    def __str__(self):
        return f'({self.name}, {self.username})'
    
    def __repr__(self):
        return self.__str__()


#confession model
class Confession(models.Model):

    confessionID = models.AutoField(primary_key=True)
    dateTime = models.DateTimeField(auto_now_add= True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message: str = models.TextField(default='')
    bookmarked: bool = models.BooleanField(default=False)

    def __str__(self):
        return f'(ID:{self.confessionID}, {self.dateTime}\nRecv:{self.receiver}\nMessage: \n{self.message})'

    def __repr__(self):
        return self.__str__()

    class Meta:
        # according to the document I read, adding the hyphen '-' before the particular field name implies ordering in descending order.
        ordering = ['-dateTime']

    pass


#the purpose of this class is store a user's sent messages provided they have an account.
#also it is optional ..... As a user will have to activate this setting
class UserSentConfession(models.Model):
    #the one who sent the confession
    user: User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    #corresponds to a confession the current user sent to some receiver.
    confession: Confession = models.ForeignKey(Confession, on_delete=models.CASCADE, related_name='user_confession')

    def __str__(self):
        return f'({self.user.username} - {self.confession.confessionID})'

    def __repr__(self):
        return self.__str__()

    pass



# this handles a user report of a confession
# a reported confession will not show in a reporter's feed.
class ConfessionReport(models.Model):

    id = models.BigAutoField(primary_key=True)
    datetime = models.DateTimeField(auto_now=True)
    confession_id = models.ForeignKey(Confession, on_delete=models.CASCADE, related_name='confession')
    reporter_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter_id')
    report = models.TextField(default='')

    def __str__(self):
        return f'({self.id}, conf_id {self.confession_id}, {self.report})'

    
    def __repr__(self):
        return self.__str__()




# models to handle the reports
class Reports(models.Model):

    id = models.AutoField(primary_key = True)
    datetime = models.DateTimeField(auto_now = True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
    detail = models.TextField(default='')

    def __str__(self):
        return f'({self.id}, {self.datetime}, {self.reporter}, {self.detail})'

    def __repr__(self):
        return self.__str__()

    pass




#model to handle the review of the application
class Review(models.Model):
    
    id = models.AutoField(primary_key= True)
    datetime = models.DateTimeField(auto_now = True)
    reviewer = models.EmailField(max_length = 250)
    rating = models.IntegerField()
    detail = models.TextField(default='')

    def __str__(self):
        return f'({self.id}, {self.datetime}, {self.reviewer}, {self.rating}, {self.detail})'

    def __repr__(self):
        return self.__str__()

