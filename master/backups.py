from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import *
import pandas as pd
import pyodbc

User = get_user_model()
# Create your views here.
class ExportEmployeeAPIView(APIView):
    def get(request,*args):
        server = '10.29.15.169'
        database = 'YokogawaDB_1505'
        username = 'sa'
        password = 'Yokogawa@12345'
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = connection.cursor()

        if cursor:
            query = 'SELECT  * FROM Employee'
            cursor.execute(query)
            results = cursor.fetchall()
            # for each row and column, dump into excel file
            df = pd.DataFrame.from_records(results, columns=[desc[0] for desc in cursor.description])
            df.to_excel('Employee.xlsx', index=False)
            return Response("Exported to excel file")
        else:
            return Response("No data found")

class ExportOrgDepartmentAPIView(APIView):
    def get(request,*args):
        server = '10.29.15.169'
        database = 'YokogawaDB_1505'
        username = 'sa'
        password = 'Yokogawa@12345'
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password) 
        cursor = connection.cursor()
        if cursor:
            query = 'SELECT  * FROM OrgDepartments'
            cursor.execute(query)
            results = cursor.fetchall()
            # for each row and column, dump into excel file
            df = pd.DataFrame.from_records(results, columns=[desc[0] for desc in cursor.description])
            df.to_excel('OrgDepartment.xlsx', index=False)
            return Response("Exported to excel file")
        else:
            return Response("No data found")

class ExportOrgDepartmentHeadAPIView(APIView):
    def get(request,*args):
        server = '10.29.15.169'
        database = 'YokogawaDB_1505'
        username = 'sa'
        password = 'Yokogawa@12345'
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = connection.cursor()
        if cursor:
            query = 'SELECT  * FROM OrgDepartmentsHead'
            cursor.execute(query)
            results = cursor.fetchall()
            # for each row and column, dump into excel file
            df = pd.DataFrame.from_records(results, columns=[desc[0] for desc in cursor.description])
            df.to_excel('OrgDepartmentHead.xlsx', index=False)
            return Response("Exported to excel file")
        else:
            return Response("No data found")
        
class ExportMasterDepartmentAPIView(APIView):
    def get(request,*args):
        server = '10.29.15.169'
        database = 'YokogawaDB_1505'
        username = 'sa'
        password = 'Yokogawa@12345'
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = connection.cursor()

        if cursor:
            query = 'SELECT  * FROM Departments'
            cursor.execute(query)
            results = cursor.fetchall()
            # for each row and column, dump into excel file
            df = pd.DataFrame.from_records(results, columns=[desc[0] for desc in cursor.description])
            df.to_excel('Department.xlsx', index=False)
            return Response("Exported to excel file")
        else:
            return Response("No data found")
        
class ExportMasterCostCenterAPIView(APIView):
    def get(request,*args):
        server = '10.29.15.169'
        database = 'YokogawaDB_1505'
        username = 'sa'
        password = 'Yokogawa@12345'
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = connection.cursor()

        if cursor:
            query = 'SELECT  * FROM CostCenters'
            cursor.execute(query)
            results = cursor.fetchall()
            # for each row and column, dump into excel file
            df = pd.DataFrame.from_records(results, columns=[desc[0] for desc in cursor.description])
            df.to_excel('masterCostCenter.xlsx', index=False)
            return Response("Exported to excel file")
        else:
            return Response("No data found")
          
class ExportMasterCategoryAPIView(APIView):
    def get(request,*args):
        server = '10.29.15.169'
        database = 'YokogawaDB_1505'
        username = 'sa'
        password = 'Yokogawa@12345'
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = connection.cursor()

        if cursor:
            query = 'SELECT  * FROM MISCOItemCategories'
            cursor.execute(query)
            results = cursor.fetchall()
            # for each row and column, dump into excel file
            df = pd.DataFrame.from_records(results, columns=[desc[0] for desc in cursor.description])
            df.to_excel('MasterCategory.xlsx', index=False)
            return Response("Exported to excel file")
        else:
            return Response("No data found")
        
class ExportMasterItemAPIView(APIView):
    def get(request,*args):
        server = '10.29.15.169'
        database = 'YokogawaDB_1505'
        username = 'sa'
        password = 'Yokogawa@12345'
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = connection.cursor()
        if cursor:
            query = 'SELECT  * FROM MISCOItems'
            cursor.execute(query)
            results = cursor.fetchall()
            # for each row and column, dump into excel file
            df = pd.DataFrame.from_records(results, columns=[desc[0] for desc in cursor.description])
            df.to_excel('MasterItem.xlsx', index=False)
            return Response("Exported to excel file")
        else:
            return Response("No data found")
        

# # Import Data from Excel to Database   
class ImportUserBulkData(APIView):
    def post(self, request, Format=None):
        file = request.FILES['file']
        if file:
            df = pd.read_excel(file)
            df = df.where(pd.notnull(df), None)
            df['FunctionalRoleId'] = df['FunctionalRoleId'].fillna(0).astype(int)
            df['DepartmentId'] = df['DepartmentId'].fillna(0).astype(int)
            df['GroupId'] = df['GroupId'].fillna(0).astype(int)
            df['OrgDepartmentId'] = df['OrgDepartmentId'].fillna(0).astype(int)
            df['OrgOfficeId'] = df['OrgOfficeId'].fillna(0).astype(int)
            # fix NaTType does not support utcoffset
            df['DOB'] = df['DOB'].fillna(pd.to_datetime('1900-01-01'))
            df['DOJ'] = df['DOJ'].fillna(pd.to_datetime('1900-01-01'))
            password = make_password('Yokogawa@12345')

            for index, row in df.iterrows():
                OrgDepartmentId = OrgDepartment.objects.get(id=row['OrgDepartmentId'])
                if row['EmployeeNo'] is not None:
                    User.objects.create(
                        username=row['EmployeeNo'],
                        name=row['Name'],
                        email = row['EMail'],
                        password=password,
                        OrgDepartmentId = OrgDepartmentId,

                        GlobalEmpNo = row['GlobalEmpNo'],
                        YGSAccountCode = row['YGSAccountCode'],
                        DomainId = row['DomainId'],
                        YGSCostCenter = row['YGSCostCenter'],
                        CostCenter = row['CostCenter'],
                        Sex = row['Sex'],
                        DOB = row['DOB'],
                        BoolContract = row['BoolContract'],
                        DOJ = row['DOJ'],
                        DepartmentId = row['DepartmentId'],
                        GroupId = row['GroupId'],
                        DeptCode = row['DeptCode'],
                        Grade = row['Grade'],
                        Designation = row['Designation'],
                        FunctionalRoleId = row['FunctionalRoleId'],
                        OldEmail = row['OldEMail'],
                        HODEmpNo = row['HODEmpNo'],
                        BoolHOD = row['BoolHOD'],
                        MobileNo = row['MobileNo'],
                    )
            return Response({'status': 'success', 'message': 'File uploaded successfully'})

        else:
            return Response("No file found")


class ImportOrgDepartmentBulkData(APIView):
    def post(self, request, Format=None):
        file = self.request.FILES['file']
        if file:
            df = pd.read_excel(file)
            df = df.where(pd.notnull(df), None)
            df['OrgDepartmentId'] = df['OrgDepartmentId'].fillna(0).astype(int)
            df['DepartmentHeadXX'] = df['DepartmentHeadXX'].fillna(0).astype(int)
            df['BUWalletId'] = df['BUWalletId'].fillna(0).astype(int)
            df['RRProcessName'] = df['RRProcessName'].fillna('null').astype(str)
            for index, row in df.iterrows():
                orgdepartment = OrgDepartment.objects.filter(Name=row['OrgDepartment'])
                if orgdepartment:
                    orgdepartment.update(
                        Name = row['OrgDepartment'],
                        Head = row['DepartmentHeadXX'],
                        BUWallet = row['BUWalletId'],
                        RRProcessName = row['RRProcessName'],
                    )
                else:
                    OrgDepartment.objects.create(
                        Name = row['OrgDepartment'],
                        Head = row['DepartmentHeadXX'],
                        BUWallet = row['BUWalletId'],
                        RRProcessName = row['RRProcessName'],
                    )
            return Response({'status': 'success', 'message': 'File uploaded successfully'})
        else:
            return Response("No file found")


class ImportOrgDepartmentHeadBulkData(APIView):
    def post(self, request, Format=None):
        file = self.request.FILES['file']
        if file:
            df = pd.read_excel(file)
            df = df.where(pd.notnull(df), None)
            df['OrgDepartmentId'] = df['OrgDepartmentId'].fillna(0).astype(int)
            df['Head'] = df['Head'].fillna(0).astype(str)
            df['Designation'] = df['Designation'].fillna('null').astype(str)
            df['OrgOfficeId'] = df['OrgOfficeId'].fillna(0).astype(int)

            for index, row in df.iterrows():
                OrgDepartmentId = OrgDepartment.objects.get(id=row['OrgDepartmentId'])
                if OrgDepartmentId:
                    OrgDepartmentHead.objects.create(
                        OrgDepartment = OrgDepartmentId,
                        Head = row['Head'],
                        Designation = row['Designation'],
                        OrgOffice = row['OrgOfficeId'],
                    )
            return Response({'status': 'success', 'message': 'File uploaded successfully'})
        else:
            return Response("No file found")
      

class ImportDepartmentBulkData(APIView):
    def post(self, request, Format=None):
        file = request.FILES['file']
        if file:
            df = pd.read_excel(file)
            df = df.where(pd.notnull(df), None)
            # df['FunctionalRoleId'] = df['FunctionalRoleId'].fillna(0).astype(int)
            # df['DepartmentId'] = df['DepartmentId'].fillna(0).astype(int)
            # df['GroupId'] = df['GroupId'].fillna(0).astype(int)
            # df['OrgDepartmentId'] = df['OrgDepartmentId'].fillna(0).astype(int)
            # df['OrgOfficeId'] = df['OrgOfficeId'].fillna(0).astype(int)
            # # fix NaTType does not support utcoffset
            # df['DOB'] = df['DOB'].fillna(pd.to_datetime('1900-01-01'))
            # df['DOJ'] = df['DOJ'].fillna(pd.to_datetime('1900-01-01'))
            for index, row in df.iterrows():
                department = MasterDepartment.objects.filter(DepartmentName=row['DepartmentName'])
                if department.exists():
                    department.update(
                        DepartmentName = row['DepartmentName'],
                        DepartmentHead = row['DepartmentHead'],
                        DepartmentAdministrator = row['DepartmentAdministrator'],
                        DepartmentSubAdministrator = row['DepartmentSubAdministrator'],
                        BUCode = row['BUCode'],
                        BoolInUse = row['BoolInUse'],
                    )
                else:
                    MasterDepartment.objects.create(
                            DepartmentName = row['DepartmentName'],
                            DepartmentHead = row['DepartmentHead'],
                            DepartmentAdministrator = row['DepartmentAdministrator'],
                            DepartmentSubAdministrator = row['DepartmentSubAdministrator'],
                            BUCode = row['BUCode'],
                            BoolInUse = row['BoolInUse'],
                    )              
                
            return Response({'status': 'success', 'message': 'File uploaded successfully'})

        else:
            return Response("No file found")
        

class ImportCostCenterBulkData(APIView):
    def post(self, request, Format=None):
        file = request.FILES['file']
        if file:
            df = pd.read_excel(file)
            df = df.where(pd.notnull(df), None)

            for index, row in df.iterrows():
                costcenter = MasterCostCenter.objects.filter(CostCenter=row['CostCenter'])
                if costcenter.exists():
                    costcenter.update(
                        CostCenter = row['CostCenter'],
                        BUSA = row['BUSA'],
                        IsExisting = row['IsExisting'],
                    )
                else:
                    MasterCostCenter.objects.create(
                        CostCenter = row['CostCenter'],
                        BUSA = row['BUSA'],
                        IsExisting = row['IsExisting'],
                    )              
                
            return Response({'status': 'success', 'message': 'File uploaded successfully'})

        else:
            return Response("No file found")
        

class ImportMasterCategory(APIView):
    def post(self, request, Format=None):
        file = request.FILES['file']
        if file:
            df = pd.read_excel(file)
            df = df.where(pd.notnull(df), None)

            for index, row in df.iterrows():
                data = MasterCategory.objects.filter(ItemCategory=row['ItemCategory'])
                if data.exists():
                    data.update(
                        ItemCategory = row['ItemCategory'],
                        BoolInUse = row['BoolInUse'],
                    )
                else:
                    MasterCategory.objects.create(
                        ItemCategory = row['ItemCategory'],
                        BoolInUse = row['BoolInUse'],
                    )
            return Response({'status': 'success', 'message': 'File uploaded successfully'})
        else:
            return Response("No file found")
        

class ImportMasterItem(APIView):
    def post(self, request, Format=None):
        file = request.FILES['file']
        if file:
            df = pd.read_excel(file)
            df = df.where(pd.notnull(df), None)

            for index, row in df.iterrows():
                # "MasterCategory" is the foreign key of "MasterItem" model tThen create MasterItem object
                category = MasterCategory.objects.filter(CategoryId=row['ItemCategoryId'])
                if category.exists():
                    MasterItem.objects.create(
                        ItemName = row['ItemName'],
                        ItemCategoryId = category[0],
                        UnitPrice = row['UnitPrice'],
                        BoolInUse = row['BoolInUse'],
                    )
                else:
                    MasterCategory.objects.create(
                        ItemName = row['ItemName'],
                        ItemCategoryId = category[0],
                        UnitPrice = row['UnitPrice'],
                        BoolInUse = row['BoolInUse'],
                    )
                    
            return Response({'status': 'success', 'message': 'File uploaded successfully'})
        else:
            return Response("No file found")
    
