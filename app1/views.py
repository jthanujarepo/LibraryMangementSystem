from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import loader
from .models import *
from .forms import *
from django.db.models import Q  # Import Q for complex queries
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re


def admin_login(request):
    if request.method == 'POST':
        # Handle admin login logic here
        pass
    return render(request, 'admin_login.html')

def user_login(request):
    if request.method == 'POST':
        # Handle user login logic here
        pass
    return render(request, 'user_login.html')


@login_required  # Ensure the user is logged in
def admin_notifications(request):
    notifications = AdminNotification.objects.all().order_by('-created_at')  # Fetch all notifications
    return render(request, 'admin_notifications.html', {'notifications': notifications})

@login_required
def manage_password_reset_requests(request):
    # View all password reset requests
    requests = PasswordResetRequest.objects.all()
    return render(request, 'manage_password_reset_requests.html', {'requests': requests})

@login_required
def create_password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password reset request created successfully.")
            return redirect('manage_password_reset_requests')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'create_password_reset_request.html', {'form': form})

@login_required
def edit_password_reset_request(request, pk):
    reset_request = get_object_or_404(PasswordResetRequest, pk=pk)
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST, instance=reset_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Password reset request updated successfully.")
            return redirect('manage_password_reset_requests')
    else:
        form = PasswordResetRequestForm(instance=reset_request)
    return render(request, 'edit_password_reset_request.html', {'form': form})

@login_required
def delete_password_reset_request(request, pk):
    reset_request = get_object_or_404(PasswordResetRequest, pk=pk)
    reset_request.delete()
    messages.success(request, "Password reset request deleted successfully.")
    return redirect('manage_password_reset_requests')

@login_required
def manage_admin_notifications(request):
    # View all admin notifications
    notifications = AdminNotification.objects.all()
    return render(request, 'manage_admin_notifications.html', {'notifications': notifications})

@login_required
def create_admin_notification(request):
    if request.method == 'POST':
        form = AdminNotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Admin notification created successfully.")
            return redirect('manage_admin_notifications')
    else:
        form = AdminNotificationForm()
    return render(request, 'create_admin_notification.html', {'form': form})

@login_required
def edit_admin_notification(request, pk):
    notification = get_object_or_404(AdminNotification, pk=pk)
    if request.method == 'POST':
        form = AdminNotificationForm(request.POST, instance=notification)
        if form.is_valid():
            form.save()
            messages.success(request, "Admin notification updated successfully.")
            return redirect('manage_admin_notifications')
    else:
        form = AdminNotificationForm(instance=notification)
    return render(request, 'edit_admin_notification.html', {'form': form})

@login_required
def delete_admin_notification(request, pk):
    notification = get_object_or_404(AdminNotification, pk=pk)
    notification.delete()
    messages.success(request, "Admin notification deleted successfully.")
    return redirect('manage_admin_notifications')

# Login view


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            # Allow admin users to log in regardless of reset approval
            if user.is_staff:
                login(request, user)
                messages.success(request, "You have logged in successfully as admin.")
                return redirect('home')  # Redirect to home or another page
            # Fetch all PasswordResetRequests for the user
            reset_requests = PasswordResetRequest.objects.filter(user=user)
            # Check the latest reset request
            reset_allowed = any(req.is_reset_allowed for req in reset_requests)
            if not reset_allowed:
                messages.error(request, "You must reset your password before logging in.")
                return render(request, 'login.html', {'form': form})
            login(request, user)
            messages.success(request, "You have logged in successfully.")
            return redirect('home')  # Redirect to home or another page
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

from .forms import LoginForm, PasswordResetForm
def reset_password_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']
            # Set the new password for the user
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                # Update the PasswordResetRequest to allow logging in
                reset_request = PasswordResetRequest.objects.filter(user=user).order_by('-request_time').first()
                if reset_request:
                    reset_request.allow_reset()
                messages.success(request, "Your password has been reset successfully. You can now log in.")
                return redirect('login')
            except User.DoesNotExist:
                form.add_error(None, "User does not exist.")
    else:
        form = PasswordResetForm()

    return render(request, 'reset_password.html', {'form': form})
# Logout view
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

# Home view (for logged-in users)
@login_required
def homeDisplay(request):
    return render(request, "home.html")

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Signup successful. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Signup failed. Please correct the errors.")
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def forgot_password_request(request):
    if request.method == "POST":
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('forgot_password')
        
        # Create password reset request
        PasswordResetRequest.objects.create(user=user)
        
        # Notify admin
        AdminNotification.objects.create(
            user=user,
            message=f"{user.username} requested a password reset."
        )
        
        messages.success(request, "Password reset request submitted. Admin will respond.")
        return redirect('login')
    return render(request, 'forgot_password.html')

def admin_remove_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Set the user's password to None, requiring them to reset it
    user.set_password(None)
    user.save()
    
    # Update reset request and notify the user
    reset_request = get_object_or_404(PasswordResetRequest, user=user)
    reset_request.allow_reset()

    messages.success(request, f"Password for {user.username} removed. User can reset their password.")
    return redirect('admin_dashboard')

def user_reset_password(request):
    if request.method == "POST":
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('reset_password')
        
        # Check if the user is allowed to reset the password
        reset_request = get_object_or_404(PasswordResetRequest, user=user)
        
        if not reset_request.is_reset_allowed:
            messages.error(request, "You cannot reset the password yet.")
            return redirect('reset_password')
        
        # Validate new passwords
        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()

            # Mark the reset request as completed
            reset_request.delete()  # Optionally, you can mark it as completed instead of deleting it

            update_session_auth_hash(request, user)
            messages.success(request, "Password reset successfully.")
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, 'reset_password.html')


def reset_password_in_login(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the passwords match
        if new_password == confirm_password:
            # Validate the password (length, capital letter, number, special char)
            if not validate_password(new_password):
                messages.error(request, "Password does not meet criteria.")
                return redirect('reset_password_in_login', user_id=user.id)

            # Update the user's password
            user.set_password(new_password)
            user.save()

            # Mark the password reset request as completed
            reset_request = PasswordResetRequest.objects.get(user=user)
            reset_request.delete()  # Remove the request since it is now completed

            messages.success(request, "Password reset successful. Please log in.")
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, 'reset_password_in_login.html', {'user': user})



def home(request):
    return render(request, 'home.html')
def home2(request):
    return render(request, 'home2.html')



def batchmaster_list(request):
    batches = BatchMaster.objects.all()
    return render(request, 'batchmaster_list.html', {'batches': batches})

def batchmaster_create(request):
    if request.method == 'POST':
        form = BatchMasterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Batch created successfully!")
            return redirect('batchmaster_list')
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        form = BatchMasterForm()
    return render(request, 'batchmaster_form.html', {'form': form})

def batchmaster_update(request, pk):
    batch = get_object_or_404(BatchMaster, pk=pk)
    if request.method == 'POST':
        form = BatchMasterForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, "Batch updated successfully!")
            return redirect('batchmaster_list')
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        form = BatchMasterForm(instance=batch)
    return render(request, 'batchmaster_form.html', {'form': form})

def batchmaster_delete(request, pk):
    batch = get_object_or_404(BatchMaster, pk=pk)
    if request.method == 'POST':
        batch.delete()
        messages.success(request, "Batch deleted successfully!")
        return redirect('batchmaster_list')
    return render(request, 'batchmaster_confirm_delete.html', {'batch': batch})

def batchmaster_search(request):
    query = request.GET.get('q')
    batches = BatchMaster.objects.filter(batchId__icontains=query) if query else BatchMaster.objects.all()
    return render(request, 'batchmaster_list.html', {'batches': batches})


def batchmaster_report(request):
    batches = BatchMaster.objects.all()  # Default to all batches
    error_message = None

    if request.method == 'POST':
        search_value = request.POST.get('search_value', '').strip()

        if search_value:  # Check if search value is provided
            batches = BatchMaster.objects.filter(batchNo__icontains=search_value)

            if not batches.exists():  # Check if any batches were found
                error_message = "No batches found with that Batch No."

    return render(request, 'batchmaster_report.html', {'batches': batches, 'error_message': error_message})



# views.py


def semester_list(request):
    semesters = SemesterMaster.objects.all()
    return render(request, 'semester_list.html', {'semesters': semesters})

def semester_create(request):
    if request.method == "POST":
        form = SemesterMasterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Semester created successfully!")
            return redirect('semester_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SemesterMasterForm()
    return render(request, 'semester_form.html', {'form': form})

def semester_update(request, pk):
    semester = get_object_or_404(SemesterMaster, pk=pk)
    if request.method == "POST":
        form = SemesterMasterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            messages.success(request, "Semester updated successfully!")
            return redirect('semester_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SemesterMasterForm(instance=semester)
    return render(request, 'semester_form.html', {'form': form})

def semester_delete(request, pk):
    semester = get_object_or_404(SemesterMaster, pk=pk)
    if request.method == "POST":
        semester.delete()
        messages.success(request, "Semester deleted successfully!")
        return redirect('semester_list')
    return render(request, 'semester_confirm_delete.html', {'semester': semester})

def semester_search(request):
    query = request.GET.get('q')
    if query:
        semesters = SemesterMaster.objects.filter(semesterId__icontains=query)
    else:
        semesters = SemesterMaster.objects.all()
    return render(request, 'semester_list.html', {'semesters': semesters})



def semester_report(request, pk=None):
    current_time = timezone.now()
    if pk:
        # Fetch specific semester record
        semester = get_object_or_404(SemesterMaster, pk=pk)
        semesters = [semester]  # Create a list with a single item for display
        report_title = f"Report for Semester {semester.semester}"
    else:
        # Fetch all semester records
        semesters = SemesterMaster.objects.all()
        report_title = "Report for All Semesters"

    return render(request, 'semester_report.html', {
        'semesters': semesters,
        'report_title': report_title,
        'current_time': current_time,
    })



# View to list all students in sorted order
def student_list(request):
    students = StudentMaster.objects.all().order_by('studentRegNo')  # Adjust sorting as needed
    return render(request, 'student_list.html', {'students': students})

def student_create(request):
    if request.method == "POST":
        form = StudentMasterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student created successfully!")
            return redirect('student_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentMasterForm()
    return render(request, 'student_form.html', {'form': form})

def student_update(request, pk):
    student = get_object_or_404(StudentMaster, pk=pk)
    if request.method == "POST":
        form = StudentMasterForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('student_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentMasterForm(instance=student)
    return render(request, 'student_form.html', {'form': form})

def student_delete(request, pk):
    student = get_object_or_404(StudentMaster, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})

def student_search(request):
    query = request.GET.get('q')
    if query:
        students = StudentMaster.objects.filter(studentName__icontains=query).order_by('studentName')  # Sort results
    else:
        students = StudentMaster.objects.all().order_by('studentName')  # Sort all records
    return render(request, 'student_list.html', {'students': students})

# Report view, if needed for generating reports


def student_report(request, pk=None):
    current_time = timezone.now()

    query = request.GET.get('q')  # Get the search query from the request (studentRegNo)

    if query:
        # Filter students by studentRegNo
        students = StudentMaster.objects.filter(studentRegNo__icontains=query).order_by('studentRegNo')
        if not students:
            error_message = f"No students found with Registration Number: {query}"
        else:
            error_message = None
        report_title = f"Search Results for {query}"
    else:
        if pk:
            # Fetch specific student record by pk
            student = get_object_or_404(StudentMaster, pk=pk)
            students = [student]  # Create a list with a single item for display
            report_title = f"Report for Student {student.studentName}"
        else:
            # Fetch all student records if no pk or search query is provided
            students = StudentMaster.objects.all().order_by('studentRegNo')
            report_title = "Report for All Students"
        error_message = None

    return render(request, 'student_report.html', {
        'students': students,
        'report_title': report_title,
        'current_time': current_time,
        'error_message': error_message,
    })


# View to list all staff members
def staffmaster_list(request):
    staff_members = StaffMaster.objects.all()
    return render(request, 'staffmaster_list.html', {'staff_members': staff_members})

# View to create a new staff member
def staffmaster_create(request):
    if request.method == 'POST':
        form = StaffMasterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Staff member created successfully!")
                return redirect('staffmaster_list')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        form = StaffMasterForm()
    return render(request, 'staffmaster_form.html', {'form': form})

# View to update an existing staff member
def staffmaster_update(request, pk):
    staff_member = get_object_or_404(StaffMaster, pk=pk)
    if request.method == 'POST':
        form = StaffMasterForm(request.POST, instance=staff_member)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Staff member updated successfully!")
                return redirect('staffmaster_list')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        form = StaffMasterForm(instance=staff_member)
    return render(request, 'staffmaster_form.html', {'form': form})
# View to delete a staff member
def staffmaster_delete(request, pk):
    staff_member = get_object_or_404(StaffMaster, pk=pk)
    if request.method == 'POST':
        staff_member.delete()
        messages.success(request, "Staff member deleted successfully!")
        return redirect('staffmaster_list')
    return render(request, 'staffmaster_confirm_delete.html', {'staff_member': staff_member})

# View to search for staff members by staff name or department
def staffmaster_search(request):
    query = request.GET.get('q')
    staff_members = StaffMaster.objects.filter(staffName__icontains=query) if query else StaffMaster.objects.all()
    return render(request, 'staffmaster_list.html', {'staff_members': staff_members})

# View to generate a report based on staff search

def staffmaster_report(request):
    staff_members = StaffMaster.objects.all()  # Default to all staff
    error_message = None

    if request.method == 'POST':
        search_value = request.POST.get('search_value', '').strip()

        if search_value:  # Check if search value is provided
            staff_members = StaffMaster.objects.filter(staffId__icontains=search_value)

            if not staff_members.exists():  # Check if any staff members were found
                error_message = "No staff found with that Staff ID."

    return render(request, 'staffmaster_report.html', {'staff_members': staff_members, 'error_message': error_message})

#book

def book_list(request):
    # books = Book.objects.all().order_by('studentRegNo')  # Adjust sorting as needed
    books = Book.objects.all()  # Adjust sorting as needed
    return render(request, 'book_list.html', {'books': books})

def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book created successfully!")
            return redirect('book_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect('book_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted successfully!")
        return redirect('book_list')
    return render(request, 'book_confirm_delete.html', {'book': book})

def book_search(request):
    query = request.GET.get('q')
    books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_report(request):
    books = Book.objects.all()  # Default to all staff
    error_message = None

    if request.method == 'POST':
        search_value = request.POST.get('search_value', '').strip()

        if search_value:  # Check if search value is provided
            books = Book.objects.filter(title__icontains=search_value)

            if not books.exists():  # Check if any staff members were found
                error_message = "No book found with that title."

    return render(request, 'book_report.html', {'books': books, 'error_message': error_message})





# Bookissued
def bookissue_list(request):
    books = BookIssued.objects.all() 
    return render(request, 'bookissue_list.html', {'books': books})

def bookissue_create(request):
    if request.method == "POST":
        form = BookIssueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "BookIssued created successfully!")
            return redirect('bookissue_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookIssueForm()
    return render(request, 'bookissue_form.html', {'form': form})
  
def bookissue_update(request, pk):
    book = get_object_or_404(BookIssued, pk=pk)
    if request.method == "POST":
        form = BookIssueForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "BookIssued updated successfully!")
            return redirect('bookissue_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookIssueForm(instance=book)
    return render(request, 'bookissue_form.html', {'form': form})
  
def bookissue_delete(request, pk):
    book = get_object_or_404(BookIssued, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "BookIssued deleted successfully!")
        return redirect('bookissue_list')
    return render(request, 'bookissue_confirm_delete.html', {'book': book})

def bookissue_search(request):
    query = request.GET.get('q')
    books = BookIssued.objects.filter(bname__title__icontains=query) if query else BookIssued.objects.all()
    return render(request, 'bookissue_list.html', {'books': books})

def bookissue_report(request):
    books = BookIssued.objects.all()  # Default to all staff
    error_message = None

    if request.method == 'POST':
        search_value = request.POST.get('search_value', '').strip()

        if search_value:  # Check if search value is provided
            books = BookIssued.objects.filter(bname__title__icontains=search_value)

            if not books.exists():  # Check if any staff members were found
                error_message = "No book found with that title."

    return render(request, 'bookissue_report.html', {'books': books, 'error_message': error_message})

# Bookreturned
def bookreturn_list(request):
    books = BookReturned.objects.all() 
    return render(request, 'bookreturn_list.html', {'books': books})

def bookreturn_create(request):
    if request.method == "POST":
        form = BookReturnForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "BookReturned created successfully!")
            return redirect('bookreturn_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookReturnForm()
    return render(request, 'bookreturn_form.html', {'form': form})
  
def bookreturn_update(request, pk):
    book = get_object_or_404(BookReturned, pk=pk)
    if request.method == "POST":
        form = BookReturnForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "BookReturned updated successfully!")
            return redirect('bookreturn_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookReturnForm(instance=book)
    return render(request, 'bookreturn_form.html', {'form': form})

def bookreturn_delete(request, pk):
    book = get_object_or_404(BookReturned, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "BookReturned deleted successfully!")
        return redirect('bookreturn_list')
    return render(request, 'bookreturn_confirm_delete.html', {'book': book})

def bookreturn_search(request):
    query = request.GET.get('q')
    books = BookReturned.objects.filter(b_name__title__icontains=query) if query else BookReturned.objects.all()
    return render(request, 'bookreturn_list.html', {'books': books})

def bookreturn_report(request):
    books = BookReturned.objects.all()  # Default to all staff
    error_message = None

    if request.method == 'POST':
        search_value = request.POST.get('search_value', '').strip()

        if search_value:  # Check if search value is provided
            books = BookReturned.objects.filter(b_name__title__icontains=search_value)

            if not books.exists():  # Check if any staff members were found
                error_message = "No book found with that title."

    return render(request, 'bookreturn_report.html', {'books': books, 'error_message': error_message})


def penalty(request):
    loans = BookReturned.objects.all()
    for loan in loans:
           penalty=loan.cal_penalty()
    
    date=datetime.now()
    if request.method == "GET" and 'query' in request.GET:
        form = SearchForm(request.GET)
       
        if form.is_valid():
            search_query = form.cleaned_data['query']
            loans = loans.filter(name_id=search_query)  # Case-insensitive search
            loans.save()
            # loans=BookReturned.objects.filter(name_firstName=search_query)
    else:
        form = SearchForm()

    return render(request, 'penaltynew.html', {'loans': loans,'date':date})

def bookpenalty_search(request):
    query = request.GET.get('q')
    loans = BookReturned.objects.filter(b_name__title__icontains=query) if query else BookReturned.objects.all()
    return render(request, 'penaltynew.html', {'loans': loans})

def penalty_report11(request):
    books = BookReturned.objects.all()  # Default to all staff
    error_message = None

    if request.method == 'POST':
        search_value = request.POST.get('search_value', '').strip()

        if search_value:  # Check if search value is provided
            books = BookReturned.objects.filter(b_name__title__icontains=search_value)

            if not books.exists():  # Check if any staff members were found
                error_message = "No book found with that title."

    return render(request, 'penalty_report.html', {'books': books, 'error_message': error_message})

def penaltyreport(request):
    loans = BookReturned.objects.all()
    error_message = None
    print("1")
    for loan in loans:
           penalty=loan.cal_penalty()
    print(2)
    if request.method == 'POST':
        search_value = request.POST.get('search_value', '').strip()
        print(3)
        if search_value:  # Check if search value is provided
            loans = BookReturned.objects.filter(b_name__title__icontains=search_value)

            if not loans.exists():  # Check if any staff members were found
                error_message = "No book found with that title."
        return render(request, 'penalty_report.html', {'loans': loans,'error_message': error_message})
    return render(request, 'penalty_report.html', {'loans': loans,'error_message': error_message})
    


    # date=datetime.now()
    # print(4)
    # if request.method == "GET" and 'query' in request.GET:
    #     form = SearchForm(request.GET)
    #     print(5)
    #     if search_value:  # Check if search value is provided
    #     #     books = BookReturned.objects.filter(b_name__title__icontains=search_value)
    #         loans = loans.filter(name_id__icontains=search_value)  # Case-insensitive search
              
        #     if not books.exists():  # Check if any staff members were found
        #         error_message = "No book found with that title."

        # if form.is_valid():
        #     search_query = form.cleaned_data['query']
        #     loans = loans.filter(name_id=search_query)  # Case-insensitive search
        #     loans.save()
            # loans=BookReturned.objects.filter(name_firstName=search_query)
    # else:
    #     form = SearchForm()






# def committee_department_list(request):
#     search_query = request.GET.get('search', '').strip()  # Get the search query and strip whitespace

#     if search_query:
#         # Filter by departmentId using icontains to allow partial matches
#         departments = CommitteeDepartment.objects.filter(departmentId__icontains=search_query)
#     else:
#         # If no search query, retrieve all departments
#         departments = CommitteeDepartment.objects.all()

    # return render(request, 'committee_department_list.html', {'departments': departments})
# def committee_department_create(request):
#     if request.method == 'POST':
#         form = CommitteeDepartmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Committee Department created successfully!")
#             return redirect('committee_department_list')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = CommitteeDepartmentForm()
#     return render(request, 'committee_department_form.html', {'form': form})

# def committee_department_update(request, pk):
#     department = get_object_or_404(CommitteeDepartment, pk=pk)
#     if request.method == 'POST':
#         form = CommitteeDepartmentForm(request.POST, instance=department)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Committee Department updated successfully!")
#             return redirect('committee_department_list')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = CommitteeDepartmentForm(instance=department)
#     return render(request, 'committee_department_form.html', {'form': form})

# def committee_department_delete(request, pk):
#     department = get_object_or_404(CommitteeDepartment, pk=pk)
#     if request.method == 'POST':
#         department.delete()
#         messages.success(request, "Committee Department deleted successfully!")
#         return redirect('committee_department_list')
#     return render(request, 'committee_department_confirm_delete.html', {'department': department})



# def committee_department_report(request):
#     departments = CommitteeDepartment.objects.all()  # Default to all departments
#     error_message = None

#     if request.method == 'POST':
#         search_value = request.POST.get('search_value', '').strip()

#         if search_value:  # Check if search value is provided
#             departments = CommitteeDepartment.objects.filter(departmentId__icontains=search_value)

#             if not departments.exists():  # Check if any departments were found
#                 error_message = "No departments found with that Department ID."

#     return render(request, 'committee_department_report.html', {'departments': departments, 'error_message': error_message})

# views.py

# def committee_master_list(request):
#     search_query = request.GET.get('search', '').strip()  # Get the search query and strip whitespace

#     if search_query:
#         # Filter by committeeId using icontains to allow partial matches
#         committees = CommitteeMaster.objects.filter(Q(committeeId__icontains=search_query) | Q(committeeName__icontains=search_query))
#     else:
#         # If no search query, retrieve all committees
#         committees = CommitteeMaster.objects.all()

#     return render(request, 'committee_master_list.html', {'committees': committees})

# def committee_master_create(request):
#     if request.method == 'POST':
#         form = CommitteeMasterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Committee Master created successfully!")
#             return redirect('committee_master_list')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = CommitteeMasterForm()
#     return render(request, 'committee_master_form.html', {'form': form})

# def committee_master_update(request, pk):
#     committee = get_object_or_404(CommitteeMaster, pk=pk)
#     if request.method == 'POST':
#         form = CommitteeMasterForm(request.POST, instance=committee)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Committee Master updated successfully!")
#             return redirect('committee_master_list')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = CommitteeMasterForm(instance=committee)
#     return render(request, 'committee_master_form.html', {'form': form})

# def committee_master_delete(request, pk):
#     committee = get_object_or_404(CommitteeMaster, pk=pk)
#     if request.method == 'POST':
#         committee.delete()
#         messages.success(request, "Committee Master deleted successfully!")
#         return redirect('committee_master_list')
#     return render(request, 'committee_master_confirm_delete.html', {'committee': committee})

# def committee_master_report(request):
#     # Retrieve all committee master records
#     committee_masters = CommitteeMaster.objects.all()  # Default to all committee masters
#     error_message = None

#     if request.method == 'POST':
#         search_value = request.POST.get('search_value', '').strip()

#         if search_value:  # Check if search value is provided
#             committee_masters = CommitteeMaster.objects.filter(committeeId__icontains=search_value)

#             if not committee_masters.exists():  # Check if any records were found
#                 error_message = "No committee masters found with that Committee ID."

#     return render(request, 'committee_master_report.html', {'committee_masters': committee_masters, 'error_message': error_message})



# View to list all transactions in sorted order
# def transaction_list(request):
#     transactions = TransactionMaster.objects.all().order_by('Name')  # Adjust sorting as needed
#     return render(request, 'transaction_list.html', {'transactions': transactions})


# def transaction_create(request):
#     if request.method == "POST":
#         form = TransactionMasterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Transaction created successfully!")
#             return redirect('transaction_list')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = TransactionMasterForm()
#     return render(request, 'transaction_form.html', {'form': form})


# def transaction_update(request, pk):
#     transaction = get_object_or_404(TransactionMaster, pk=pk)
#     if request.method == "POST":
#         form = TransactionMasterForm(request.POST, instance=transaction)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Transaction updated successfully!")
#             return redirect('transaction_list')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = TransactionMasterForm(instance=transaction)
#     return render(request, 'transaction_form.html', {'form': form})

# def transaction_delete(request, pk):
#     transaction = get_object_or_404(TransactionMaster, pk=pk)
#     if request.method == "POST":
#         transaction.delete()
#         messages.success(request, "Transaction deleted successfully!")
#         return redirect('transaction_list')
#     return render(request, 'transaction_confirm_delete.html', {'transaction': transaction})

# def transaction_search(request):
#     query = request.GET.get('q')
#     transactions = TransactionMaster.objects.all()
#     if query:
#         transactions = transactions.filter(Name__icontains=query).order_by('Name')
#     return render(request, 'transaction_list.html', {'transactions': transactions})

# def transaction_report(request):
#     # Fetch all unique batch IDs and committee names for default dropdown options
#     all_batches = TransactionMaster.objects.values_list('batchID', flat=True).distinct()
#     all_committees = CommitteeMaster.objects.values_list('committeeName', flat=True).distinct()

#     # Get the selected batch ID and committee name from the request
#     batch_id = request.GET.get('batchID', '')  # Default to an empty string if not provided
#     committee_name = request.GET.get('committeeName', '')  # Default to an empty string if not provided

#     # Filter transactions based on the selected criteria
#     transactions = TransactionMaster.objects.all()
#     if batch_id:
#         transactions = transactions.filter(batchID=batch_id)
#     if committee_name:
#         transactions = transactions.filter(committeeName__committeeName=committee_name)

#     # Group transactions by committee name
#     grouped_transactions = {}
#     for transaction in transactions:
#         if transaction.committeeName not in grouped_transactions:
#             grouped_transactions[transaction.committeeName] = []
#         grouped_transactions[transaction.committeeName].append(transaction)

#     return render(request, 'transaction_report.html', {
#         'grouped_transactions': grouped_transactions,
#         'batch_id': batch_id,
#         'committee_name': committee_name,
#         'all_batches': all_batches,
#         'all_committees': all_committees,
#     })

# def grouped_transaction_view(request):
#     # Get all transactions and organize them by committee name and batch ID
#     transactions = TransactionMaster.objects.select_related(
#         'committeeName'  # Include only relational fields in select_related
#     ).order_by('batchID', 'committeeName')

#     grouped_data = {}
#     for transaction in transactions:
#         batch_id = transaction.batchID
#         committee_name = transaction.committeeName

#         # Ensure the committee_name key exists in the grouped_data
#         if committee_name not in grouped_data:
#             grouped_data[committee_name] = {}

#         # Ensure the batch_id key exists under the committee_name
#         if batch_id not in grouped_data[committee_name]:
#             grouped_data[committee_name][batch_id] = []

#         # Add the transaction to the grouped_data
#         grouped_data[committee_name][batch_id].append(transaction)

#     return render(request, 'grouped_transaction_view.html', {
#         'grouped_data': grouped_data
#     })

# from django.utils import timezone

# def committee_view(request, committee_name, template_name, extra_context=None):
#     # Fetching all the transactions based on committee_name
#     batch_id = request.GET.get('batchID', None)
#     transactions = TransactionMaster.objects.filter(
#         committeeName__committeeName=committee_name
#     )

#     # Filter transactions by batch ID if a batch is selected
#     if batch_id:
#         transactions = transactions.filter(batchID=batch_id)
    
#     # Paginate the transactions (assuming pagination logic exists)
#     from django.core.paginator import Paginator
#     paginator = Paginator(transactions, 10)
#     page_number = request.GET.get('page')
#     transactions = paginator.get_page(page_number)

#     # Fetch unique batch IDs for the filter dropdown
#     all_batches = TransactionMaster.objects.values_list('batchID', flat=True).distinct()

#     # Extra context for additional values
#     extra_context = extra_context or {}
#     context = {
#         "committee_name": committee_name,
#         "transactions": transactions,
#         "batch_id": batch_id,
#         "all_batches": all_batches,
#     }
#     context.update(extra_context)

#     return render(request, template_name, context)


# def admission_committee(request):
#     current_time = timezone.now()  # Get the current date and time
#     return committee_view(
#         request, 
#         "Admission Committee", 
#         "admission_committee.html", 
#         extra_context={"current_time": current_time}
#     )

# def anti_ragging_committee(request):
#     current_time = timezone.now()
#     return committee_view(
#         request,
#         "Anti-Ragging Committee", 
#         "anti_ragging_committee.html",
#         extra_context={"current_time": current_time})

# def cultural_committee(request):
#     current_time = timezone.now()
#     return committee_view(request, "Cultural Committee", "cultural_committee.html",
#         extra_context={"current_time": current_time})

# def discipline_committee(request):
#     current_time = timezone.now()
#     return committee_view(request, "Discipline Committee", "discipline_committee.html",extra_context={"current_time": current_time})

# def internal_complaints_committee(request):
#     current_time = timezone.now()
#     return committee_view(request, "Internal Complaints Committee", "internal_complaints_committee.html",extra_context={"current_time": current_time})

# def library_committee(request):
#     current_time = timezone.now()
#     return committee_view(request, "Library Committee", "library_committee.html",extra_context={"current_time": current_time})

# def sc_st_committee(request):
#     current_time = timezone.now()
#     return committee_view(request, "SC/ST Committee", "sc_st_committee.html",extra_context={"current_time": current_time})

# def student_staff_grievance_committee(request):
#     current_time = timezone.now()
#     return committee_view(request, "Student and Staff Grievance Committee", "student_and_staff_grievance_committee.html",extra_context={"current_time": current_time})

# def student_council(request):
#     current_time = timezone.now()
#     return committee_view(request, "Student Council", "student_council.html",extra_context={"current_time": current_time})

# def sports_committee(request):
#     current_time = timezone.now()
#     return committee_view(request, "Sports Committee", "sports_committee.html",extra_context={"current_time": current_time})

# def women_empowerment_committee(request):
#     current_time = timezone.now()
#     return committee_view(request, "Women Empowerment Committee", "women_empowerment_committee.html",extra_context={"current_time": current_time})
