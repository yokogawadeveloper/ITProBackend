from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MasterProcurement
from django.contrib.auth import get_user_model
from master.models import OrgDepartmentHead



User = get_user_model()

@receiver(post_save, sender=MasterProcurement)
def create_approval_transaction(sender, instance, created, **kwargs):
    if created:
        from approval.models import ApprovalTransaction ,ApproverMatrix
        appmat = ApproverMatrix.objects.filter(request_type=instance.RequestType).order_by('sequence')
        for app in appmat:
            if app.sequence == 1:
                userOrgDept = User.objects.get(id=instance.Created_by.id).OrgDepartmentId
                userOrgDeptHead = OrgDepartmentHead.objects.filter(OrgDepartment_id=userOrgDept).first()
                userOrgDeptHeadEmail = User.objects.get(username=userOrgDeptHead.Head).email
                approverEmail = userOrgDeptHeadEmail
                userId = User.objects.get(username=userOrgDeptHead.Head)
                #create approval transaction
                ApprovalTransaction.objects.create(procurementId=instance,approverEmail=approverEmail,approvalUserName=userId.username,sequence=app.sequence,approverType='BuHead',status='Pending')

            elif app.sequence == 2:
                    email = 'Jiya.K@yokogawa.com'
                    user = User.objects.get(email = email)
                    approvalName = user.username
                    #create approval transaction
                    ApprovalTransaction.objects.create(procurementId=instance,approverEmail=email,approvalUserName=approvalName,sequence=app.sequence,approverType='DSINHead',status='Pending')

                    
            elif app.sequence == 3:
                    email = 'ganeshchandra.p@yokogawa.com'
                    user = User.objects.get(email = email)
                    approvalName = user.username
                    #create approval transaction
                    ApprovalTransaction.objects.create(procurementId=instance,approverEmail=email,approvalUserName=approvalName,sequence=app.sequence,approverType='FinanceHead',status='Pending')

            elif app.sequence == 4:
                    email = 'sajiv.nath@yokogawa.com'
                    user = User.objects.get(email = email)
                    approvalName = user.username
                    #create approval transaction
                    ApprovalTransaction.objects.create(procurementId=instance,approverEmail=email,approvalUserName=approvalName,sequence=app.sequence,approverType='MD',status='Pending')


            elif app.sequence == 5:
                    email = 'Naveen.R@yokogawa.com' 
                    user = User.objects.get(email = email)
                    approvalName = user.username
                    #create approval transaction
                    ApprovalTransaction.objects.create(procurementId=instance,approverEmail=email,approvalUserName=approvalName,sequence=app.sequence,approverType='DSINMPR',status='Pending')

            else:
                pass
            
        if not appmat:
            pass


@receiver(post_save, sender=MasterProcurement)
def update_approval_transaction(sender, instance, created, **kwargs):
        if not created:
                print('update_approval_transaction')
                from approval.models import ApprovalTransaction
                apptrans = ApprovalTransaction.objects.filter(procurementId=instance).order_by('sequence')
                for app in apptrans:
                        if app.sequence == 1:
                                userOrgDept = User.objects.get(id=instance.Created_by.id).OrgDepartmentId
                                userOrgDeptHead = OrgDepartmentHead.objects.filter(OrgDepartment_id=userOrgDept).first()
                                userOrgDeptHeadEmail = User.objects.get(username=userOrgDeptHead.Head).email
                                approverEmail = userOrgDeptHeadEmail
                                userId = User.objects.get(username=userOrgDeptHead.Head)
                                #update approval transaction
                                ApprovalTransaction.objects.filter(procurementId=instance,approverType='BuHead').update(approverEmail=approverEmail,approvalUserName=userId.username,status='Pending')
                
                        elif app.sequence == 2:
                                email = 'Jiya.K@yokogawa.com'
                                user = User.objects.get(email = email)
                                approvalName = user.username
                                #update approval transaction
                                ApprovalTransaction.objects.filter(procurementId=instance,approverType='DSINHead').update(approverEmail=email,approvalUserName=approvalName)

                        elif app.sequence == 3:
                                email = 'ganeshchandra.p@yokogawa.com'
                                user = User.objects.get(email = email)
                                approvalName = user.username
                                #update approval transaction
                                ApprovalTransaction.objects.filter(procurementId=instance,approverType='FinanceHead').update(approverEmail=email,approvalUserName=approvalName)

                        elif app.sequence == 4:
                                email = 'sajiv.nath@yokogawa.com'
                                user = User.objects.get(email = email)
                                approvalName = user.username
                                #update approval transaction
                                ApprovalTransaction.objects.filter(procurementId=instance,approverType='MD').update(approverEmail=email,approvalUserName=approvalName)


                        elif app.sequence == 5:
                                email = 'Naveen.R@yokogawa.com' 
                                user = User.objects.get(email = email)
                                approvalName = user.username
                                #update approval transaction
                                ApprovalTransaction.objects.filter(procurementId=instance,approverType='DSINMPR').update(approverEmail=email,approvalUserName=approvalName)

                        else:
                                pass

                if not apptrans:
                        pass




                        

        

                    
