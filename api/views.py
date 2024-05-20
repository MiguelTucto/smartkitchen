from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from detection.services import detect_objects

class ProductDetectionView(APIView):
    def post(self, request, *args, **kwargs):
        image_data = request.data.get('image')

        if not image_data:
            return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            detected_products = detect_objects(image_data)
            return Response(detected_products, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
