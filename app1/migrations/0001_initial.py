# Generated by Django 5.0.6 on 2024-10-30 12:50

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batchNo', models.CharField(max_length=2, unique=True, validators=[django.core.validators.RegexValidator(message='Enter only integers.', regex='^[0-9]+$')])),
                ('batchId', models.CharField(choices=[(' ', 'Select_Batch'), ('2020-2022', '2020-2022'), ('2021-2023', '2021-2023'), ('2022-2024', '2022-2024'), ('2023-2025', '2023-2025'), ('2024-2025', '2024-2025'), ('2025-2027', '2025-2027'), ('2026-2028', '2026-2028'), ('2027-2029', '2027-2029'), ('2028-2030', '2028-2030')], default=' ', max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommitteeDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentId', models.CharField(max_length=3, unique=True, validators=[django.core.validators.RegexValidator(message='Enter only integers.', regex='^[0-9]+$')])),
                ('committeeDesignation', models.CharField(choices=[(' ', 'Select_Designation'), ('Chairman', 'Chairman'), ('Convener', 'Convener'), ('Member', 'Member'), ('Executive Member', 'Executive Member'), ('Student Member', 'Student Member')], default=' ', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='CommitteeMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('committeeId', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Enter only integers.', regex='^[0-9]+$')])),
                ('committeeName', models.CharField(choices=[('Admission Committee', 'Admission Committee'), ('Anti-Ragging Committee', 'Anti-Ragging Committee'), ('Cultural Committee', 'Cultural Committee'), ('Discipline Committee', 'Discipline Committee'), ('Internal Complaints Committee', 'Internal Complaints Committee'), ('Library Committee', 'Library Committee'), ('SC/ST Committee', 'SC/ST Committee'), ('Student and Staff Grievance Committee', 'Student and Staff Grievance Committee'), ('Student Council', 'Student Council'), ('Sports Committee', 'Sports Committee'), ('Women Empowerment Committee (WEC)', 'Women Empowerment Committee (WEC)')], default=' ', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SemesterMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(blank=True, choices=[(' ', 'Select_Semester'), ('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV')], default=' ', max_length=15)),
                ('semesterId', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(message='Enter only integers.', regex='^[0-9]+$')])),
            ],
        ),
        migrations.CreateModel(
            name='StaffMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staffId', models.IntegerField(unique=True, validators=[django.core.validators.RegexValidator(message='Enter only integers.', regex='^[0-9]+$')])),
                ('staffName', models.CharField(max_length=25, validators=[django.core.validators.RegexValidator(message='Only alphabetic characters and spaces are allowed.', regex='^[a-zA-Z ]*$')])),
                ('staffCollegeName', models.CharField(max_length=60, validators=[django.core.validators.RegexValidator(message='Only alphabetic characters and spaces are allowed.', regex='^[a-zA-Z ]*$')])),
                ('department', models.CharField(choices=[(' ', 'Select Department'), ('Science', 'Science'), ('Arts', 'Arts'), ('Commerce', 'Commerce'), ('Engineering', 'Engineering'), ('Medical', 'Medical'), ('Law', 'Law'), ('MCA', 'MCA'), ('MBA', 'MBA')], default=' ', max_length=30)),
                ('designation', models.CharField(choices=[(' ', 'Select Designation'), ('Director', 'Director'), ('Principal', 'Principal'), ('HOD', 'HOD'), ('Associate Professor', 'Associate Professor'), ('Assistant Professor', 'Assistant Professor'), ('Professor', 'Professor'), ('Lecturer', 'Lecturer'), ('Lab Admin', 'Lab Admin')], default=' ', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='AdminNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_reset_allowed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Only alphabetic characters and spaces are allowed.', regex='^[a-zA-Z ]*$')])),
                ('batchID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='total', to='app1.batchmaster')),
                ('committeeDesignation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='total', to='app1.committeedepartment')),
                ('committeeName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='total', to='app1.committeemaster')),
                ('designation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='total', to='app1.staffmaster')),
            ],
        ),
        migrations.CreateModel(
            name='StudentMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentRegNo', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Enter only integers.', regex='^[0-9]+$')])),
                ('studentName', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Only alphabetic characters and spaces are allowed.', regex='^[a-zA-Z ]*$')])),
                ('studentMobile', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Enter only integers.', regex='^[0-9]+$')])),
                ('studentEmail', models.EmailField(max_length=55, unique=True)),
                ('studentCaste', models.CharField(choices=[(' ', 'Select_Caste'), ('General', 'General'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST')], default=' ', max_length=10)),
                ('course', models.CharField(choices=[(' ', 'Select_Course'), ('B.Sc. Computer Science', 'B.Sc. Computer Science'), ('B.Com', 'B.Com'), ('B.A. English', 'B.A. English'), ('B.Tech Civil Engineering', 'B.Tech Civil Engineering'), ('B.Tech Mechanical Engineering', 'B.Tech Mechanical Engineering'), ('B.Sc. Physics', 'B.Sc. Physics'), ('B.Sc. Chemistry', 'B.Sc. Chemistry'), ('B.A. Economics', 'B.A. Economics'), ('BBA', 'BBA'), ('MBA', 'MBA'), ('MCA', 'MCA')], default=' ', max_length=50)),
                ('batchNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='app1.batchmaster')),
                ('sem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='app1.semestermaster')),
            ],
            options={
                'unique_together': {('batchNo', 'sem', 'studentRegNo', 'studentName')},
            },
        ),
    ]
