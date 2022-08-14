import django_filters
from rest_framework.exceptions import ValidationError

from .models import Like
from mainapp.utils import DateUtil


class LikeFilter(django_filters.FilterSet):

    date_from = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        required=True,
    )

    date_to = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        required=True,
    )

    post_id = django_filters.NumberFilter(field_name="post__id")

    class Meta:
        model = Like
        fields = ("date_from", "date_to", "post_id")

    def is_valid(self):
        self.validate_datetime(self.request)
        return super().is_valid()

    @staticmethod
    def validate_datetime(request) -> None:

        error_dict = {}

        date_from = DateUtil(request.query_params.get("date_from"))
        date_to = DateUtil(request.query_params.get("date_to"))

        if date_from.date and date_to.date:

            if date_from.is_str_in_datetime_format() and date_to.is_str_in_datetime_format():

                if date_from.format_str_to_date() > date_to.format_str_to_date():
                    error_dict[
                        "date_from"
                    ] = "date_from must be less/equal than date_to"

            else:
                error_dict["error"] = "dates must be in YYYY-MM-DD format"

        else:
            error_dict["error"] = "date_from and date_to are both required"

        if error_dict:
            raise ValidationError(error_dict)
