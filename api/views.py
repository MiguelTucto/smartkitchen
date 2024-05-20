from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from detection.services import detect_objects

class ProductDetectionView(APIView):
    def post(self, request, *args, **kwargs):
        image_data = request.data.get('image')

        if not image_data:
            print("No image provided.")
            return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            print("Received image data.")
            detected_products = detect_objects(image_data)
            print("Detected products:", detected_products)
            return Response(detected_products, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error processing image:", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)