from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .validators import validate_unique_field 
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta



class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_time = models.DateTimeField(default=timezone.now)
    is_reset_allowed = models.BooleanField(default=False)

    def allow_reset(self):
        self.is_reset_allowed = True
        self.save()

    def __str__(self):
        return f"Password reset request for {self.user.username} at {self.request_time}"
    
class AdminNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.user.username} - {self.created_at}"



# Validators
alpha_validator = RegexValidator(
    regex=r'^[a-zA-Z ]*$',
    message='Only alphabetic characters and spaces are allowed.'
)
integer_validator = RegexValidator(
    regex=r'^[0-9]+$',
    message='Enter only integers.'
)

# BatchMaster table
BATCH_CHOICES = [
    (" ", "Select_Batch"),
    ("2020-2022", "2020-2022"),
    ("2021-2023", "2021-2023"),
    ("2022-2024", "2022-2024"),
    ("2023-2025", "2023-2025"),
    ("2024-2025", "2024-2025"),
    ("2025-2027", "2025-2027"),
    ("2026-2028", "2026-2028"),
    ("2027-2029", "2027-2029"),
    ("2028-2030", "2028-2030"),
]

class BatchMaster(models.Model):
    batchNo = models.CharField(max_length=2, validators=[integer_validator], unique=True)
    batchId = models.CharField(max_length=10, choices=BATCH_CHOICES, default=" ", unique=True)

    def __str__(self):
        return f'{self.batchId}'

    def clean(self):
        if not self.batchNo.isdigit():
            raise ValidationError("Batch number should contain only digits.")


# SemesterMaster table
SEM_CHOICES = [
    (" ", "Select_Semester"),
    ("I", "I"),
    ("II", "II"),
    ("III", "III"),
    ("IV", "IV"),
]

class SemesterMaster(models.Model):
    semester = models.CharField(max_length=15, choices=SEM_CHOICES, default=" ", blank=True)
    semesterId = models.CharField(max_length=6, validators=[integer_validator])

    def __str__(self):
        return f'{self.semester}'

    def clean(self):
        if not self.semesterId.isdigit():
            raise ValidationError("Semester ID should contain only digits.")


# StudentMaster table

# CASTE_CHOICES = [
#     (" ", "Select_Caste"),
#     ("General", "General"),
#     ("OBC", "OBC"),
#     ("SC", "SC"),
#     ("ST", "ST"),
# ]

COURSE_CHOICES = [
    (" ", "Select_Course"),
    ("B.Sc. Computer Science", "B.Sc. Computer Science"),
    ("B.Com", "B.Com"),
    ("B.A. English", "B.A. English"),
    ("B.Tech Civil Engineering", "B.Tech Civil Engineering"),
    ("B.Tech Mechanical Engineering", "B.Tech Mechanical Engineering"),
    ("B.Sc. Physics", "B.Sc. Physics"),
    ("B.Sc. Chemistry", "B.Sc. Chemistry"),
    ("B.A. Economics", "B.A. Economics"),
    ("BBA", "BBA"),
    ("MBA", "MBA"),
    ("MCA", "MCA"),
]

class StudentMaster(models.Model):
    batchNo = models.ForeignKey('BatchMaster', on_delete=models.CASCADE, related_name='students')
    sem = models.ForeignKey('SemesterMaster', on_delete=models.CASCADE, related_name='students')
    studentRegNo = models.CharField(max_length=10, validators=[integer_validator])
    studentName = models.CharField(max_length=50, validators=[alpha_validator])
    studentMobile = models.CharField(max_length=10, validators=[integer_validator])
    studentEmail = models.EmailField(max_length=55, unique=True)
    # studentCaste = models.CharField(max_length=10, choices=CASTE_CHOICES, default=" ")
    course = models.CharField(max_length=50, choices=COURSE_CHOICES, default=" ")

    class Meta:
        unique_together = ('batchNo', 'sem', 'studentRegNo', 'studentName')

    def clean(self):
        if len(self.studentMobile) != 10:
            raise ValidationError("Mobile number must be exactly 10 digits.")

    def __str__(self):
        return f'{self.studentName} - {self.studentRegNo}'


# StaffMaster table
DEPARTMENT_CHOICES = [
    (" ", "Select Department"),
    ("Science", "Science"),
    ("Arts", "Arts"),
    ("Commerce", "Commerce"),
    ("Engineering", "Engineering"),
    ("Medical", "Medical"),
    ("Law", "Law"),
    ("MCA", "MCA"),
    ("MBA", "MBA"),
]

DESIGNATIONS_CHOICES = [
    (" ", "Select Designation"),
    ("Director", "Director"),
    ("Principal", "Principal"),
    ("HOD", "HOD"),
    ("Associate Professor", "Associate Professor"),
    ("Assistant Professor", "Assistant Professor"),
    ("Professor", "Professor"),
    ("Lecturer", "Lecturer"),
    ("Lab Admin", "Lab Admin"),
]

class StaffMaster(models.Model):
    staffId = models.IntegerField(unique=True, validators=[integer_validator])
    staffName = models.CharField(max_length=25, validators=[alpha_validator])
    staffCollegeName = models.CharField(max_length=60, validators=[alpha_validator])
    department = models.CharField(max_length=30, choices=DEPARTMENT_CHOICES, default=" ")
    designation = models.CharField(max_length=30, choices=DESIGNATIONS_CHOICES, default=" ")

    def __str__(self):
        return f' {self.designation}'  # Keep both for other uses

    def designation_only(self):
        return self.designation 
    
    def clean(self):
        if not str(self.staffId).isdigit():
            raise ValidationError("Staff ID should contain only digits.")


# CommitteeDepartment table
# COMMITTEE_DESIGNATION_CHOICES = [
#     (" ", "Select_Designation"),
#     ("Chairman", "Chairman"),
#     ("Convener", "Convener"),
#     ("Member", "Member"),
#     ("Executive Member", "Executive Member"),
#     ("Student Member", "Student Member"),
# ]

# class CommitteeDepartment(models.Model):
#     departmentId = models.CharField(unique=True, max_length=3, validators=[integer_validator])
#     committeeDesignation = models.CharField(max_length=30, choices=COMMITTEE_DESIGNATION_CHOICES, default=" ")

#     def __str__(self):
#         return f'{self.committeeDesignation}'

#     def clean(self):
#         if not self.departmentId.isdigit():
#             raise ValidationError("Department ID should contain only digits.")


# CommitteeMaster table

# COMMITTEE_NAME_CHOICES = [
#     ("Admission Committee", "Admission Committee"),
#     ("Anti-Ragging Committee", "Anti-Ragging Committee"),
#     ("Cultural Committee", "Cultural Committee"),
#     ("Discipline Committee", "Discipline Committee"),
#     ("Internal Complaints Committee", "Internal Complaints Committee"),
#     ("Library Committee", "Library Committee"),
#     ("SC/ST Committee", "SC/ST Committee"),
#     ("Student and Staff Grievance Committee", "Student and Staff Grievance Committee"),
#     ("Student Council", "Student Council"),
#     ("Sports Committee", "Sports Committee"),
#     ("Women Empowerment Committee (WEC)", "Women Empowerment Committee (WEC)"),
# ]

# class CommitteeMaster(models.Model):
#     committeeId = models.CharField(unique=True, max_length=10, validators=[integer_validator])
#     committeeName = models.CharField(max_length=100, choices=COMMITTEE_NAME_CHOICES, default=" ")

#     def __str__(self):
#         return f'{self.committeeName}'

#     def clean(self):
#         if not self.committeeId.isdigit():
#             raise ValidationError("Committee ID should contain only digits.")

BATCHID_CHOICES = [
    (" ", "Select_Batch"),
    ("2020-2021", "2020-2021"),
    ("2021-2022", "2021-2022"),
    ("2022-2023", "2022-2023"),
    ("2023-2024", "2023-2024"),
    ("2024-2025", "2024-2025"),
    ("2025-2026", "2025-2026"),
    ("2026-2027", "2026-2027"),
    ("2027-2028", "2027-2028"),
    ("2028-2029", "2028-2029"),
    ("2029-2030", "2029-2030"),
]

# TransactionMaster table
# class TransactionMaster(models.Model):
#     batchID = models.CharField(max_length=10, choices=BATCHID_CHOICES, default=" ")
#     Name = models.CharField(max_length=50, validators=[alpha_validator])
#     designation = models.ForeignKey('StaffMaster', on_delete=models.CASCADE, related_name='total')
#     committeeDesignation = models.ForeignKey('CommitteeDepartment', on_delete=models.CASCADE, related_name='total')
#     committeeName = models.ForeignKey('CommitteeMaster', on_delete=models.CASCADE, related_name='total')

#     def __str__(self):
#         return f'{self.Name} - {self.committeeName}'

class Book(models.Model):
    bookId=models.IntegerField(unique=True)
    title=models.CharField(max_length=200)
    author=models.CharField(max_length=100)
    publisher=models.CharField(max_length=150)
    # status_id=models.BooleanField(default=True)
    edition=models.CharField(max_length=100)
    no_of_book=models.IntegerField()
    
    def __str__(x):
        return x.title

class BookIssued(models.Model):
    std_Name=models.ForeignKey(StudentMaster,on_delete=models.CASCADE)
    bname=models.ForeignKey(Book,on_delete=models.CASCADE)
    issue_date=models.DateField()
    
    def __str__(d):
        return str(d.issue_date)
    # def __str__(a):
    #     return a.std_Name.lastName

class BookReturned(models.Model):
    name=models.ForeignKey(StudentMaster,on_delete=models.CASCADE)
    b_name=models.ForeignKey(Book,on_delete=models.CASCADE)
    is_date=models.ForeignKey(BookIssued,on_delete=models.CASCADE) ####
    penalty_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)###
    
    returned_date=models.DateField()
   
    def __str__(self):
        return str(self.returned_date)
    

    def cal_penalty(self):
        if self.returned_date:
            # Assuming a penalty of $1 per day after a due date (7 days after borrowing)
            due_date = self.is_date.issue_date + timedelta(days=15)
            if self.returned_date > due_date:
                days_late = (self.returned_date - due_date).days
                self.penalty_amount = days_late * 1  # $1 per day
                self.save()

