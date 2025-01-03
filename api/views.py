from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Slide
from .serializers import SlideSerializer

class SlideViewSet(viewsets.ModelViewSet):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer

    @action(detail=False, methods=['post'], url_path='search')
    def search_slides(self, request):
        """POST /api/slides/search - Search slides"""
        try:
            # Get search parameters from request data
            #   "userQuery": "sustainable operating models",
            #   "numResults": 10
            search_user_query = request.data.get('userQuery', '')
            search_name_result = request.data.get('numResults', '')

            # Filter queryset based on search parameters
            # queryset = self.get_queryset()
            # if search_title:
            #     queryset = queryset.filter(title__icontains=search_title)
            # if search_content:
            #     queryset = queryset.filter(content__icontains=search_content)

            # Serialize and return results
            # serializer = self.get_serializer(queryset, many=True)
            return Response({
                "slides": [
                    {
                        "slideId": "156fcb95-cc9d-4f60-9d7e-7d293d26db13",
                        "slideNum": "1",
                        "fileName": "full_ppt.pptx",
                        "dateUploaded": "2024-07-01T10:15:30Z",
                        "content": {
                            "tags": ["IsTitleSlide", "HasCompanyBranding"]
                        }
                    },
                    {
                        "slideId": "9ac983f0-295f-4aea-bbb1-4b0dbcf70fe6",
                        "slideNum": "2",
                        "fileName": "ops_sustainability.pptx",
                        "dateUploaded": "2024-07-03T09:10:00Z",
                        "content": {
                            "tags": ["Topic_StrategyStructure"]
                        }
                    }
                ]
            })

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request):
        """GET /api/slides/ - List all slides"""
        # slides = self.get_queryset()
        # serializer = self.get_serializer(slides, many=True)
        return Response([{"id": 1, "title": "Slide 1", "content": "Content 1"}])

    def create(self, request):
        """POST /api/slides/ - Create a new slide"""
        print('Create request: ', request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """GET /api/slides/{id}/ - Get a specific slide"""
        slide = self.get_object()
        serializer = self.get_serializer(slide)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """PUT /api/slides/{id}/ - Update a slide"""
        slide = self.get_object()
        serializer = self.get_serializer(slide, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """DELETE /api/slides/{id}/ - Delete a slide"""
        slide = self.get_object()
        self.perform_destroy(slide)
        return Response(status=status.HTTP_204_NO_CONTENT) 