from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import reset_password_in_login

urlpatterns = [

    path('', views.home, name='home'),  
    # path('', views.login_view, name='home'),  

    path('admin-login/', views.admin_login, name='admin_login'),
    path('user-login/', views.user_login, name='user_login'),
   
    path('password-reset-requests/', views.manage_password_reset_requests, name='manage_password_reset_requests'),
    path('password-reset-requests/create/',views. create_password_reset_request, name='create_password_reset_request'),
    path('password-reset-requests/edit/<int:pk>/',views. edit_password_reset_request, name='edit_password_reset_request'),
    path('password-reset-requests/delete/<int:pk>/', views.delete_password_reset_request, name='delete_password_reset_request'),
    
    path('admin-notifications/',views. admin_notifications, name='admin_notifications'),
    path('admin-notifications/',views. manage_admin_notifications, name='manage_admin_notifications'),
    path('admin-notifications/create/',views. create_admin_notification, name='create_admin_notification'),
    path('admin-notifications/edit/<int:pk>/', views.edit_admin_notification, name='edit_admin_notification'),
    path('admin-notifications/delete/<int:pk>/', views.delete_admin_notification, name='delete_admin_notification'),
    # Authentication routes
    path('login/', views.login_view, name='login'),
    path('reset_password/', views.reset_password_view, name='reset_password'), 
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    path('reset-password-in-login/<int:user_id>/', reset_password_in_login, name='reset_password_in_login'),
    # Password reset routes
    path('forgot-password/', views.forgot_password_request, name='forgot_password'),
    path('reset-password/', views.user_reset_password, name='reset_password'),

    # Home after login
    path('home/', views.homeDisplay, name='home'),
    path('home2/', views.homeDisplay, name='home2'),

    # Admin-specific routes (for admin to manage password resets)
    path('admin-remove-password/<int:user_id>/', views.admin_remove_password, name='admin_remove_password'),

    path('batches/', views.batchmaster_list, name='batchmaster_list'),
    path('batches/create/', views.batchmaster_create, name='batchmaster_create'),
    path('batches/update/<int:pk>/', views.batchmaster_update, name='batchmaster_update'),
    path('batches/delete/<int:pk>/', views.batchmaster_delete, name='batchmaster_delete'),
    path('batches/search/', views.batchmaster_search, name='batchmaster_search'),
    path('batches/report/',views. batchmaster_report, name='batchmaster_report'), 

    path('semesters/', views.semester_list, name='semester_list'),
    path('semesters/create/', views.semester_create, name='semester_create'),
    path('semesters/update/<int:pk>/',views. semester_update, name='semester_update'),
    path('semesters/delete/<int:pk>/',views. semester_delete, name='semester_delete'),
    path('semesters/search/', views.semester_search, name='semester_search'),
    
    path('semester/report/', views.semester_report, name='semester_report'),  # For all semesters
    path('semester/report/<int:pk>/',views. semester_report, name='semester_report_specific'),  # For specific semester

    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/search/', views.student_search, name='student_search'),

    path('students/report/', views.student_report, name='student_report_all'),
    path('students/report/<int:pk>/', views.student_report, name='student_report'),

    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('books/search/', views.book_search, name='book_search'),
    path('books/report/', views.book_report, name='book_report'),

    # path('books/report/', views.book_report, name='book_report_all'),
    # path('books/report/<int:pk>/', views.book_report, name='book_report'),


    path('booksissue/', views.bookissue_list, name='bookissue_list'),
    path('booksissue/create/', views.bookissue_create, name='bookissue_create'),
    path('booksissue/<int:pk>/edit/', views.bookissue_update, name='bookissue_update'),
    path('booksissue/<int:pk>/delete/', views.bookissue_delete, name='bookissue_delete'),
    path('booksissue/search/', views.bookissue_search, name='bookissue_search'),
    path('booksissue/report/', views.bookissue_report, name='bookissue_report'),


    path('booksreturn/', views.bookreturn_list, name='bookreturn_list'),
    path('booksreturn/create/', views.bookreturn_create, name='bookreturn_create'),
    path('booksreturn/<int:pk>/edit/', views.bookreturn_update, name='bookreturn_update'),
    path('booksreturn/<int:pk>/delete/', views.bookreturn_delete, name='bookreturn_delete'),
    path('booksreturn/search/', views.bookreturn_search, name='bookreturn_search'),
    path('booksreturn/report/', views.bookreturn_report, name='bookreturn_report'),

    path('penalty/', views.penalty, name='penalty'),
    path('bookpenalty_search/', views.bookpenalty_search, name='bookpenalty_search'),
    path('penaltyreport/', views.penaltyreport, name='penaltyreport'),



    path('staff/', views.staffmaster_list, name='staffmaster_list'),
    path('staff/create/', views.staffmaster_create, name='staffmaster_create'),
    path('staff/update/<int:pk>/', views.staffmaster_update, name='staffmaster_update'),
    path('staff/delete/<int:pk>/', views.staffmaster_delete, name='staffmaster_delete'),
    path('staff/search/', views.staffmaster_search, name='staffmaster_search'),
    path('staff/report/', views.staffmaster_report, name='staffmaster_report'),

    # path('committee-department/', views.committee_department_list, name='committee_department_list'),  # List view
    # path('committee-department/create/', views.committee_department_create, name='committee_department_create'),  # Create view
    # path('committee-department/update/<int:pk>/', views.committee_department_update, name='committee_department_update'),  # Update view
    # path('committee-department/delete/<int:pk>/', views.committee_department_delete, name='committee_department_delete'),  # Delete confirmation view
    # path('committee-department/report/', views.committee_department_report, name='committee_department_report'),

    # path('committee-master/', views.committee_master_list, name='committee_master_list'),
    # path('committee-master/create/', views.committee_master_create, name='committee_master_create'),
    # path('committee-master/update/<int:pk>/',views. committee_master_update, name='committee_master_update'),
    # path('committee-master/delete/<int:pk>/', views.committee_master_delete, name='committee_master_delete'),
    # path('committee-master/report/', views.committee_master_report, name='committee_master_report'),


    # path('transactions/', views.transaction_list, name='transaction_list'),
    # path('transactions/create/', views.transaction_create, name='transaction_create'),
    # path('transactions/update/<int:pk>/', views.transaction_update, name='transaction_update'),
    # path('transactions/delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),
    # path('transactions/search/', views.transaction_search, name='transaction_search'),
    # path('transactions/report/', views.transaction_report, name='transaction_report'),
    # path('transactions/report/<int:pk>/',views.transaction_report, name='transaction_report_pk'),
   
    # path('transactions/grouped/', views.grouped_transaction_view, name='grouped_transaction_view'),
    

    # path('admission-committee/', views.admission_committee, name='admission_committee'),
    # path('anti-ragging-committee/', views.anti_ragging_committee, name='anti_ragging_committee'),
    # path('cultural-committee/', views.cultural_committee, name='cultural_committee'),
    # path('discipline-committee/', views.discipline_committee, name='discipline_committee'),
    # path('internal-complaints-committee/', views.internal_complaints_committee, name='internal_complaints_committee'),
    # path('library-committee/', views.library_committee, name='library_committee'),
    # path('sc-st-committee/', views.sc_st_committee, name='sc_st_committee'),
    # path('student-staff-grievance-committee/', views.student_staff_grievance_committee, name='student_staff_grievance_committee'),
    # path('student-council/', views.student_council, name='student_council'),
    # path('sports-committee/', views.sports_committee, name='sports_committee'),
    # path('women-empowerment-committee/', views.women_empowerment_committee, name='women_empowerment_committee'),

    # path('committee/<str:committee_name>/', views.committee_view, {'template_name': 'committee_template.html'}, name='committee_view'),
]

