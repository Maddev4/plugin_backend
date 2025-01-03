from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Deck
from ..serializers import DeckSerializer
from ..services.s3_service import S3Service, S3ServiceError

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
            
            # presigned_url = self.s3_service.get_presigned_url("070f1910-a717-4600-98fc-a569a5433cb7")
            # print(f'presigned_url: {presigned_url}')
            
            return Response(
                {
                    "deckId": "a97df2fe-434f-4e11-bfa7-804ea575af0b",
                    "storylineSlides": {
                        "sections": [
                            {
                                "sectionName": "introSection",
                                "subSections": [
                                    {
                                        "subSectionName": "introSubSection1",
                                        "slides": [
                                            {
                                                "presignedUrl": "https://www.hindustantimes.com/ht-img/img/2025/01/01/550x309/happy_new_year_2025_wishes_1735700710315_1735700724642.png",
                                                "fileId": "mckinsey.pptx", # "101",
                                                "slideId": "070f1910-a717-4600-98fc-a569a5433cb7"
                                            },
                                            {
                                                "presignedUrl": "https://www.hindustantimes.com/ht-img/img/2024/12/30/original/Screenshot_2024-12-30_at_11.49.43_AM_1735539932468.png",
                                                "fileId": "mckinsey.pptx", # "104",
                                                "slideId": "19c9f5d5-d686-4628-8b60-4b170c839f14"
                                            },
                                            {
                                                "presignedUrl": "https://www.hindustantimes.com/ht-img/img/2024/12/30/original/Screenshot_2024-12-30_at_11.49.35_AM_1735540068745.png",
                                                "fileId": "mckinsey.pptx", # "106",
                                                "slideId": "e12bc08c-c8b8-4f3e-b7ff-eac2552081d8"
                                            },
                                            {
                                                "presignedUrl": "https://www.hindustantimes.com/ht-img/img/2024/12/30/original/Romantic_New_Year_wish_1735540121577.jpg",
                                                "fileId": "mckinsey.pptx", # "108",
                                                "slideId": "3a081d80-703b-4da7-affc-01c6f7c5a416"
                                            }
                                        ]
                                    },
                                    {
                                        "subSectionName": "introSubSection2",
                                        "slides": [
                                            {
                                                "presignedUrl": "https://www.hindustantimes.com/ht-img/img/2024/12/30/original/Screenshot_2024-12-30_at_11.47.28_AM_1735540229541.png",
                                                "fileId": "mckinsey.pptx", # "112",
                                                "slideId": "b0f51192-6792-41bb-92ae-3b30bb788f20"
                                            },
                                            {
                                                "presignedUrl": "https://www.hindustantimes.com/ht-img/img/2024/12/30/original/Screenshot_2024-12-30_at_11.49.18_AM_1735540627838.png",
                                                "fileId": "mckinsey.pptx", # "113",
                                                "slideId": "0f59bddc-ba90-4905-ab2b-8b2621c80905"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "sectionName": "industryOverview",
                                "subSections": []
                            },
                            {
                                "sectionName": "productOverview",
                                "subSections": [
                                    {
                                        "subSectionName": "productSubSection1",
                                        "slides": [
                                            {
                                                "presignedUrl": "https://www.hindustantimes.com/ht-img/img/2024/10/10/550x309/Coach3_1728568380561_1728568394280.jpg",
                                                "fileId": "106",
                                                "slideId": "e426c7dc-5a39-4983-82df-4b20d5a3a2a0"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "sectionName": "caseStudy",
                                "subSections": []
                            },
                            {
                                "sectionName": "conclusion",
                                "subSections": []
                            }
                        ]
                    }
                },
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
