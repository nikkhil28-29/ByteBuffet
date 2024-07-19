# # from django.shortcuts import render

# # # Create your views here.

# # from django.contrib.auth.models import Group, User
# # from rest_framework import permissions, viewsets
# # from .models import FoodItem
# # from tutorial.quickstart.serializers import GroupSerializer, UserSerializer


# # class UserViewSet(viewsets.ModelViewSet):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = User.objects.all().order_by('-created_at')
# #     serializer_class = UserSerializer
# #     permission_classes = [permissions.IsAuthenticated]

# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from snippets.models import Snippet
# from .models import FoodItem
# from snippets.serializers import SnippetSerializer


# @api_view(['GET', 'POST'])
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         food = FoodItem.objects.filter()
#         serializer = SnippetSerializer(food, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)