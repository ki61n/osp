from django.urls import path
from . import views

urlpatterns = [

    # pages


    path('',views.home,name='home'),
    path('worker',views.worker,name='worker'),
    path('customer',views.customer,name='customer'),
    path('admin',views.admin,name='admin'),
   


# reg pages

    path('regworker',views.regworker,name='regworker'),
    path('regcustomer',views.regcustomer,name='regcustomer'),
    path('regdepartment',views.regdepartment,name='regdepartment'),
    path('regservice',views.regservice,name='regservice'),
    path('regtaskpage<int:id>',views.regtaskpage,name='regtaskpage'),
    path('profile_content',views.profile_content,name='profile_content'),

# edit pages
    path('edituser',views.edituser,name='edituser'),
    path('edit_worker',views.edit_worker,name='edit_worker'),
    path('edit_worker',views.edit_worker,name='edit_worker'),
    path('edit_dep/<int:id>',views.edit_dep,name='edit_dep'),
    path('edit_ser/<int:id>',views.edit_ser,name='edit_ser'),

    path('changepassword',views.changepassword,name='changepassword'),
    path('changeworkerpass',views.changeworkerpass,name='changeworkerpass'),
    path('changecustonerpass',views.changecustonerpass,name='changecustonerpass'),
    path('edit_profile_content/<int:id>',views.edit_profile_content,name='edit_profile_content'),
    # view pages
    path('view_deptartment',views.viewdept,name='viewdept'),
    path('view_service',views.viewserv,name='viewserv'),
    path('view_worker',views.viewworker,name='viewworker'),
    path('view_customer',views.viewcustomer,name='viewcustomer'),
    path('view_service_provider',views.viewsp,name='viewsp'),
    path('viewcustask',views.viewcustask,name='viewcustask'),
    path('viewcurtask',views.viewcurtask,name='viewcurtask'),
    path('viewspdetails/<int:id>',views.viewspdetails,name='viewspdetails'),
    path('viewtaskrequest',views.viewtaskrequest,name='viewtaskrequest'),
    path('history/<int:id>',views.history,name='history'),
    path('profile',views.profile,name='profile'),
    path('profilecus',views.profilecus,name='profilecus'),
    path('profileworker',views.profileworker,name='profileworker'),
    path('viewserindep/<int:id>',views.viewserindep,name='viewserindep'),
    path('viewapproveldata/<int:id>',views.viewapproveldata,name='viewapproveldata'),
    path('view_content',views.view_content,name='view_content'),
    path('view_rating',views.view_rating,name='view_rating'),
    path('depapprovels',views.depapprovels,name='depapprovels'), 
     
    # auth pages
    path('signin',views.signin,name='signin'),
    path('viewapprovels',views.viewapprovels,name='viewapprovels'),
    path('approveworker/<int:id>',views.approveworker,name='approveworker'),
    path('rejectworker/<int:id>',views.rejectworker,name='rejectworker'),
    path('approveserv/<int:id>',views.approveserv,name='approveserv'),
    path('approvedep/<int:id>',views.approvedep,name='approvedep'),
    path('apdept/<int:id>',views.apdept,name='apdept'),
    path('aprovdept/<int:id>',views.aprovdept,name='aprovdept'),
    path('apserv/<int:id>',views.apserv,name='apserv'),
    path('rejserv/<int:id>',views.rejserv,name='rejserv'),
    path('rejdept/<int:id>',views.rejdept,name='rejdept'),
    path('rerejectdepartjdept/<int:id>',views.rejectdepart,name='rejectdepart'),
    path('accepttask/<int:id>',views.accepttask,name='accepttask'),
    path('rejecttask/<int:id>',views.rejecttask,name='rejecttask'),



    # registration
    path('register_deptartment',views.r_dept,name='r_dept'), 
    path('register_service',views.r_serv,name='r_serv'),
    path('register_worker',views.r_worker,name='r_worker'),
    path('register_customer',views.r_customer,name='r_customer'),
    path('regtask/<int:id>',views.regTask,name='regTask'),
    path('add_review/<int:id>',views.add_review,name='add_review'),
    path('reg_profile',views.reg_profile,name='reg_profile'),

    # edit
  
    path('editprofile',views.editprofile,name='editprofile'),
    path('chpassword',views.chpassword,name='chpassword'),
    path('e_serv/<int:id>',views.e_serv,name='e_serv'),
    path('e_dep/<int:id>',views.e_dep,name='e_dep'),
    path('e_profilecon/<int:id>',views.e_profilecon,name='e_profilecon'),


    # delete
  
    
    path('d_user/<int:id>',views.d_user,name='d_user'),
    path('d_serv/<int:id>',views.d_serv,name='d_serv'),
    path('d_dep/<int:id>',views.d_dep,name='d_dep'),
    path('d_pro_con/<int:id>',views.d_pro_con,name='d_pro_con'),
    # status
    path('complete/<int:id>',views.complete,name='complete'),
    path('pending/<int:id>',views.pending,name='pending'),

  

    # authentication
    path('login',views.log,name='log'),



    path('out',views.out,name='out'),

     path('search',views.search,name='search'),


    # ajax 

    path('getserv',views.getserv,name='getserv'),

    
    # validations
    path('checkuname',views.checkuname,name='checkuname'),
    path('chackmail',views.chackmail,name='chackmail'),
    path('chackphone',views.chackphone,name='chackphone'),

    path('echeckuname',views.echeckuname,name='echeckuname'),
    path('echackmail',views.echackmail,name='echackmail'),
    path('echackphone',views.echackphone,name='echackphone'), 

    path('notification',views.notification,name='notification'),


    
] 

