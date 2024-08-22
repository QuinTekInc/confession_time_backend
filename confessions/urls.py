
from django.urls import path 
from . import views

# api urls
urlpatterns = [
    path('', views.getEnpoints),
    path('verify-user/<str:username>/<str:email>',  views.verifyUser),
    path('verify-code-sent/<str:emailAddress>/c=<str:vcode>/', views.verifyCodeSent),
    path('verify-username/<str:newUsername>/', views.verifyUsername),
    path('signup/', views.signup),
    path('login/', views.login),
    path('logout/<str:username>', views.logout),
    path('update-user-cred/<str:username>', views.updateUserCredentials),
    path('update-username/<str:username>/<str:newUsername>', views.updateUsername),
    path('delete-account/<str:username>', views.deleteAccount),
    path('send-email/<str:emailAddress>', views.sendEmail),
    path('get-msg/recv=<str:recv_username>', views.getConfessions),
    path('get-msg/sender=<str:sender_username>', views.getSentConfessions),
    path('add-msg/', views.addConfession),
    path('update-msg/<str:confessionID>/marked=<str:bookmarked>', views.updateConfession),
    path('delete-msg/<str:confessionID>', views.deleteConfession),
    path('get-saved-users/usr=<str:username>', views.getSavedUsers),
    path('save-user-detail/', views.addSavedUser),
    path('update-user-detail/<str:savedUserID>', views.updateSavedUser),
    path('delete-saved-user/<str:savedUserID>', views.deleteSavedUser),
    path('add-report/', views.addReport),
    path('add-review/', views.addReview)
]