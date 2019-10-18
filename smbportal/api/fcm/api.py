from __future__ import absolute_import
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.viewsets import ModelViewSet
from fcm_django.api.rest_framework import (
    is_user_authenticated,
    DeviceSerializerMixin,
    DeviceViewSetMixin,
    AuthorizedMixin
)
from fcm_django.models import FCMDevice
from django.db.models import Q



class UniqueRegistrationSerializerMixin(Serializer):
    def validate(self, attrs):
        devices = None
        primary_key = None
        request_method = None

        if self.initial_data.get("registration_id", None):
            if self.instance:
                request_method = "update"
                primary_key = self.instance.id
            else:
                request_method = "create"
        else:
            if self.context["request"].method in ["PUT", "PATCH"]:
                request_method = "update"
                primary_key = attrs["id"]
            elif self.context["request"].method == "POST":
                request_method = "create"

        Device = self.Meta.model
        # if request authenticated, unique together with registration_id and
        # user
        user = self.context['request'].user
        if request_method == "update":
            if user is not None and is_user_authenticated(user):
                devices = Device.objects.filter(
                    registration_id=attrs["registration_id"]) \
                    .exclude(id=primary_key)
                if (attrs["active"]):
                    devices.filter(~Q(user=user)).update(active=False)
                devices = devices.filter(user=user)
            else:
                devices = Device.objects.filter(
                    registration_id=attrs["registration_id"]) \
                    .exclude(id=primary_key)
        elif request_method == "create":
            if user is not None and is_user_authenticated(user):
                devices = Device.objects.filter(
                    registration_id=attrs["registration_id"])
                devices.filter(~Q(user=user)).update(active=False)
                devices = devices.filter(user=user, active=True)
            else:
                devices = Device.objects.filter(
                    registration_id=attrs["registration_id"])
        '''
         Here we override the default exception thrown by fcm_django in case
         of existing device on POST. We make POST idempotent, returning the 
         existing instance. This requires the override of the serializer.create()
         method
        '''
        if devices:
            return {'_device_instance':devices[0]}

        # We force active to be True, otherwise the empty field validation sets this field to False
        attrs['active'] = True
        return attrs


class FCMDeviceSerializer(ModelSerializer, UniqueRegistrationSerializerMixin):
    class Meta(DeviceSerializerMixin.Meta):
        model = FCMDevice

        extra_kwargs = {"id": {"read_only": False, "required": False}}

    def create(self, validated_data):
        '''
         In case the validated data contains ths cutom _device_instance property
         we return its content, i.e. the already existing device instance
        '''
        device = validated_data.get('_device_instance')
        if device:
            return device
        return super(FCMDeviceSerializer, self).create(validated_data)


# ViewSets
class FCMDeviceViewSet(DeviceViewSetMixin, ModelViewSet):
    queryset = FCMDevice.objects.all()
    serializer_class = FCMDeviceSerializer


class FCMDeviceAuthorizedViewSet(AuthorizedMixin, FCMDeviceViewSet):
    pass
