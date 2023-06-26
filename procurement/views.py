from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .serializers import *

User = get_user_model()
# Create your views here.
class MasterProcurementViewSet(viewsets.ModelViewSet):
    queryset = MasterProcurement.objects.all()
    serializer_class = MasterProcurementSerializer
    attachtmnt_serializer_class = AttachmentsSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        files = self.request.FILES.getlist('Files')
        serializer.save(Created_by=self.request.user)
        for file in files:
            Attachments.objects.create(file=file, request=serializer.instance)
 


    
        
  

from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
class MasterProcurementCreateAPIView(generics.CreateAPIView):
    queryset = MasterProcurement.objects.all()
    serializer_class = MasterProcurementSerializer2
    parser_classes = (MultiPartParser, FormParser)
    

    
class UploadFileViewSet(viewsets.ModelViewSet):
    serializer_class = UploadFileSerializer
    queryset = Attachments.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializers = UploadFileSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
class UploadFilesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES['file']
            filetype = request.POST['filetype']
            print(filetype)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
