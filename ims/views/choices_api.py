from rest_framework.viewsets import ViewSet
from drf_spectacular.utils import extend_schema

from stock.constants import StockMovementEnum
from auth_user.constants import MethodEnum, RoleEnum
from tenant.constants import AuthenticationTypeEnum, DatabaseStrategyEnum
from notification.constants import NotificationTypeEnum

from utils.constants import SeverityEnum
from utils.response import generate_response


def choice_tuple_to_dict(choices):

    return [{"value": ch[0], "label": ch[1]} for ch in choices]


class ConstantsAPIView(ViewSet):

    @extend_schema(exclude=True)
    def get_constants(self, request):

        data = {}

        data["role_types"] = choice_tuple_to_dict(RoleEnum.choices)
        data["method_types"] = choice_tuple_to_dict(MethodEnum.choices)
        data["severity_types"] = choice_tuple_to_dict(SeverityEnum.choices)
        data["stock_types"] = choice_tuple_to_dict(StockMovementEnum.choices)
        data["notification_types"] = choice_tuple_to_dict(NotificationTypeEnum.choices)
        data["authentication_types"] = choice_tuple_to_dict(
            AuthenticationTypeEnum.choices
        )
        data["database_strategy_types"] = choice_tuple_to_dict(
            DatabaseStrategyEnum.choices
        )

        return generate_response(data=data)
