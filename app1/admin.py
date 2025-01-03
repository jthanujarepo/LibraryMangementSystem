from django.contrib import admin
from .models import PasswordResetRequest, AdminNotification

class PasswordResetRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'request_time', 'is_reset_allowed']

class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'created_at']

admin.site.register(PasswordResetRequest, PasswordResetRequestAdmin)
admin.site.register(AdminNotification, AdminNotificationAdmin)

from django.contrib import admin
from .models import *

class BatchMasterAdmin(admin.ModelAdmin):
    list_display = ('batchNo', 'batchId')
    search_fields = ('batchNo',)

class SemesterMasterAdmin(admin.ModelAdmin):
    list_display = ('semester', 'semesterId')
    search_fields = ('semester',)

class StudentMasterAdmin(admin.ModelAdmin):
    list_display = ('studentName', 'studentRegNo', 'studentEmail', 'studentMobile')
    search_fields = ('studentName', 'studentRegNo', 'studentEmail')

class StaffMasterAdmin(admin.ModelAdmin):
    list_display = ('staffId', 'staffName', 'staffCollegeName', 'department', 'designation')
    search_fields = ('staffName', 'staffCollegeName')

class CommitteeDepartmentAdmin(admin.ModelAdmin):
    list_display = ('departmentId', 'committeeDesignation')
    search_fields = ('departmentId',)

class CommitteeMasterAdmin(admin.ModelAdmin):
    list_display = ('committeeId', 'committeeName')
    search_fields = ('committeeId', 'committeeName')

class TransactionMasterAdmin(admin.ModelAdmin):
    list_display = ['batchID', 'Name', 'designation', 'committeeDesignation', 'committeeName']
    search_fields = ('batchId', 'committeeName__committeeName')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "designation":
            kwargs["queryset"] = StaffMaster.objects.all()  # Adjust the queryset if needed
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def designation(self, obj):
        return obj.designation.designation_only()  # Use the new method to display only designation
    designation.short_description = 'Designation'  # Change the column header

class BookAdmin(admin.ModelAdmin):
    # list_display = ('studentName', 'studentRegNo', 'studentEmail', 'studentMobile')
    list_display=('title','bookId','author')
    search_fields = ('title',)

# Registering the models with their respective admin classes
admin.site.register(BatchMaster, BatchMasterAdmin)
admin.site.register(SemesterMaster, SemesterMasterAdmin)
admin.site.register(StudentMaster, StudentMasterAdmin)
admin.site.register(StaffMaster, StaffMasterAdmin)
admin.site.register(Book, BookAdmin)

# admin.site.register(CommitteeDepartment, CommitteeDepartmentAdmin)
# admin.site.register(CommitteeMaster, CommitteeMasterAdmin)
# admin.site.register(TransactionMaster, TransactionMasterAdmin)

