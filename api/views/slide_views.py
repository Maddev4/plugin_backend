from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Slide
from ..serializers import SlideSerializer

class SlideViewSet(viewsets.ModelViewSet):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer

    @action(detail=False, methods=['post'], url_path='search')
    def search_slides(self, request):
        """POST /api/slides/search"""
        try:
            user_query = request.data.get('userQuery')
            num_results = request.data.get('numResults', 10)

            if not user_query:
                return Response(
                    {'error': 'userQuery is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Implement your search logic here
            # queryset = self.get_queryset()
            # # Simple example: search in content
            # slides = queryset.filter(content__icontains=user_query)[:num_results]
            
            # serializer = self.get_serializer(slides, many=True)
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request):
        """POST /api/slides"""
        try:
            user_query = request.data.get('userQuery')
            gaps_to_fill = request.data.get('gapsToFill', {})

            if not user_query:
                return Response(
                    {'error': 'userQuery is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create slide data
            slide_data = {
                'file_name': 'new_slide.pptx',  # You would generate this
                'slide_num': '1',  # You would calculate this
                'template_id': 'template001',
                'shaped_id': 'shapeSet003',
                'content': {
                    'changes': [
                        {
                            'objectId': 'titleBox',
                            'action': 'updateText',
                            'newValue': gaps_to_fill.get('title', '')
                        },
                        {
                            'objectId': 'subtitleBox',
                            'action': 'updateText',
                            'newValue': gaps_to_fill.get('subtitle', '')
                        }
                    ]
                }
            }

            # serializer = self.get_serializer(data=slide_data)
            # serializer.is_valid(raise_exception=True)
            # self.perform_create(serializer)

            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({
                "slideId": "11b3be17-5e7c-4d32-a4d6-9446f5ce09ac",
                "templateId": "template001",
                "shapedId": "shapeSet003",
                "changesJSON": [
                    {
                        "objectId": "titleBox",
                        "action": "updateText",
                        "newValue": "Introducing SecureAI"
                    },
                    {
                        "objectId": "subtitleBox",
                        "action": "updateText",
                        "newValue": "Revolutionary AI for the Enterprise"
                    },
                    {
                        "objectId": "mainImage",
                        "action": "updateImage",
                        "newValue": "security_shield.png"
                    }
                ],
                "dateUploaded": "2024-07-10T08:15:00Z"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def partial_update(self, request, pk=None):
        """PATCH /api/slides/{slideId}"""
        try:
            # Validate request
            user_edit_query = request.data.get('userEditQuery')
            if not user_edit_query:
                return Response(
                    {'error': 'userEditQuery is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the slide
            # try:
            #     slide = self.get_object()
            # except Slide.DoesNotExist:
            #     return Response(
            #         {'error': 'Slide not found'}, 
            #         status=status.HTTP_404_NOT_FOUND
            #     )

            # Process the user's edit query
            # Here you would implement your logic to interpret the query
            # This is a simplified example
            # changes = []
            # object_ids = []

            # if "bullet" in user_edit_query.lower():
            #     changes.append({
            #         "objectId": "bulletList1",
            #         "action": "updateText",
            #         "newValue": "New bullet point based on query"
            #     })
            #     object_ids.append("bulletList1")

            # if "image" in user_edit_query.lower():
            #     changes.append({
            #         "objectId": "mainImage",
            #         "action": "updateImage",
            #         "newValue": "new_image.png"
            #     })
            #     object_ids.append("mainImage")

            # # Update the slide's content with the changes
            # if not slide.content:
            #     slide.content = {}
            # slide.content['changes'] = changes
            # slide.save()

            # Return the response in the required format
            # response_data = {
            #     "slideId": str(slide.slide_id),
            #     "objectIds": object_ids,
            #     "changes": changes,
            #     "dateModified": slide.date_uploaded.isoformat()
            # }
            response_data = {
                "slideId": "11b3be17-5e7c-4d32-a4d6-9446f5ce09ac",
                "objectIds": ["bulletList1", "mainImage"],
                "changes": [
                    {
                        "objectId": "bulletList1",
                        "action": "updateText",
                        "newValue": "New bullet point based on query"
                    },
                    {
                        "objectId": "mainImage",
                        "action": "updateImage",
                        "newValue": "new_image.png"
                    }
                ],
                "dateModified": "2024-03-15T09:20:00Z"
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )