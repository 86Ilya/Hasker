from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


from Hasker.profile.models import HaskerUser
from Hasker.api.serializers import HaskerUserCreateSerializer, HaskerUserUpdateSerializer
from Hasker.api.views.base_manage_view import BaseManageView


class SignUpView(generics.CreateAPIView):
    serializer_class = HaskerUserCreateSerializer


class GetUserInfoView(generics.RetrieveAPIView):
    serializer_class = HaskerUserCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    queryset = HaskerUser.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


class UpdateDestroyProfileView(GetUserInfoView, generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = HaskerUserUpdateSerializer


class ProfileManageView(BaseManageView):
    """
    get:
    Return user profile data

    put:
    Update user profile data

    patch:
    Patch user profile data

    post:
    Create a new user instance
    """

    VIEWS_BY_METHOD = {
        'DELETE': UpdateDestroyProfileView.as_view,
        'GET': GetUserInfoView.as_view,
        'PUT': UpdateDestroyProfileView.as_view,
        'POST': SignUpView.as_view,
        'PATCH': UpdateDestroyProfileView.as_view
    }
