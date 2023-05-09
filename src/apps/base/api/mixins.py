from rest_framework.serializers import BaseSerializer


class SerializerPerAction:
    """
    Mixin that allows to use different serializers for different actions.
    """

    action: str
    serializer_class: BaseSerializer
    action_serializer: dict

    def get_serializer_class(self):
        assert getattr(self, "action_serializer", None) is not None, (
            "'%s' should either include a `action_serializer` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )

        assert isinstance(self.action_serializer, dict), (
            "'%s' `action_serializer` attribute should be a dict."
            % self.__class__.__name__
        )

        assert self.action_serializer.get("default", None) is not None, (
            "'%s' `action_serializer` attribute should have a 'default' key."
            % self.__class__.__name__
        )

        self.serializer_class = self.action_serializer.get(
            self.action, self.action_serializer["default"]
        )

        return super().get_serializer_class()
