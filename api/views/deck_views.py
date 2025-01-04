from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Deck
from ..serializers import DeckSerializer
from ..services.s3_service import S3Service, S3ServiceError
from ..utils.mockup import mockup_deck

class DeckViewSet(viewsets.ModelViewSet):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call parent's __init__
        try:
            self.s3_service = S3Service.get_instance()
        except S3ServiceError as e:
            print(f"S3 Service Error: {str(e)}")
            self.s3_service = None

    def create(self, request):
        """POST /api/decks"""
        try:
            user_query = request.data.get('userQuery')
            relevant_product = request.data.get('relevantProduct')

            if not user_query:
                return Response(
                    {'error': 'userQuery is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create a new deck
            # deck_data = {
            #     'title': user_query[:200],  # Limit to max length
            #     'description': user_query,
            #     'relevant_product': relevant_product or ''
            # }

            # serializer = self.get_serializer(data=deck_data)
            # serializer.is_valid(raise_exception=True)
            # deck = serializer.save()

            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            if not self.s3_service:
                return Response(
                    {"error": "S3 service unavailable"}, 
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            sections = mockup_deck['storylineSlides']['sections']
            for section in sections:
                for subsection in section['subSections']:
                    for slide in subsection['slides']:
                        slide_id = slide['slideId']
                        presigned_url = self.s3_service.get_presigned_url(slide_id)
                        if presigned_url:
                            slide['presignedUrl'] = presigned_url
            
            mockup_deck['storylineSlides']['sections'] = sections
            
            return Response(
                mockup_deck,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    # detail=False means this action is not for a single object (no pk in URL)
    # methods specifies which HTTP methods are allowed (POST in this case) 
    # url_path customizes the URL pattern (will be /api/decks/slides_from_file_name)
    @action(detail=False, methods=['post'], url_path='slides_from_file_name')
    def get_slides_from_file_name(self, request):
        """POST /api/decks/slides_from_file_name"""
        try:
            slides = request.data
            if not slides:
                return Response(
                    {'error': 'slides is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not self.s3_service:
                return Response(
                    {"error": "S3 service unavailable"}, 
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
                
            # base64_only = self.s3_service.convert_selected_slides_to_base64(slides)
            base64_only, slide_ids = self.s3_service.convert_pptx_to_base64(slides)
            if not base64_only or not slide_ids:
                return Response(
                    {'error': 'No slides found for given slides'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            return Response(
                {'base64Only': base64_only, 'slideIds': slide_ids}, 
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
