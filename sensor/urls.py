from django.urls import path, include, re_path, register_converter
from django.views.generic import TemplateView
from sensor import views, api,auth, user, converts
from rest_framework.authtoken.views import obtain_auth_token

register_converter(converts.FloatUrlParameterConverter, 'float')

import sensor

urlpatterns = [
    # path('',views.index),
    # path('dashboard', TemplateView.as_view(template_name='sensor/track.html')),
    path('home', views.home, name='menu'),
    path('dryer', views.dryer, name='dryer'),
    path('dryer/<id>', views.dryerbyid, name='dryer'),
    path('sensor/<id>', views.sensorbyid),
    path('current/<id>', views.currentbyid),
    path('sensor', views.sensors),
    path('current', views.current),
    # path('menu', views.menu, name='menu'),
    path('', views.login, name='login'),
    path('submit_login', views.submit_login),
    path('individual_sensor/<id>', views.ind),
    path('individual3/<id>', views.sensor3),
    path('history', views.history),
    path('time/<id>', views.time),

    path('adduser',user.addUser),   
    path('submitNewUser',user.submitNewUser, name='submitNewUser'),
    # path('loguser',user.loguser, name='loguser'),
    path('updateUser/<id>',user.updateUser),
    path('deleteUser',user.submitNewUser),
    path('updatingUser',user.updatingUser, name='updatingUser'),
    path('profileUser/<id>',user.profileUser, name='profileUser'),
    # path('resetpassword/<id>',user.resetPassword),
    path('usermgt', user.usermgt, name='usermgt'),
    # path('logUserJson',user.logUserJson, name='logUserJson'),

    path('viewcctv',views.cctvview),
    path('viewcctv/<id>',views.cctvview),

    path('currentlimit',user.currentlimit),
    path('weight',user.weight),
    path('submitweight',user.submitweight),
    path('Buttonpage',user.Buttonpage),

    path('sampling', views.sampling),
    path('submitsampling',user.submitsampling, name='submitsampling'),

    path('api/dryer/<id>', api.dryer),
    path('api/elevator/<id>', api.elevator),
    path('api/controldryer',api.controldryer),
    path('api/controlelevator',api.controlelevator),
    path('api/dryer_status',api.dryer_status),
    path('api/elevator_status',api.elevator_status),
    path('api/gethistory/<id>',api.dryerhistory),
    #Combined API
    path('api/item/current_value_limit', api.api_get_value),
    path('api/item/status_dryer', api.api_get_status_dryer),
    path('api/item/sampling/<int:dryer_id>', api.api_get_sampling),
    path('api/item/<int:dryer_id>/<int:sensor_id>', api.api_get_weightset),
    path('api/item/<int:dryer_id>/batch', api.api_get_timer),
    path('api/item/<int:dryer_id>/batch/<int:batch_id>', api.api_get_historical),
    path('api/item/<int:dryer_id>/batch/<int:batch_id>/timer', api.api_get_timer_per_batch),
    path('api/item/<int:dryer_id>/batch/start_time', api.api_post_start_time),
    path('api/item/<int:dryer_id>/batch/end_time', api.api_post_end_time),
    path('api/item/sampling/<int:dryer_id>/<str:sampledata>', api.api_post_sampling),
    path('api/item/current_value_limit/<int:elevator_id>/<float:limitset>', api.api_edit_current_value),
    #Combined API
    path('api/auth/login/',obtain_auth_token,name='auth_user_login'),
    path('api/login',auth.login1),


    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),



]
