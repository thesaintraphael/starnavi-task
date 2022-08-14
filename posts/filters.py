import django_filters
from rest_framework.exceptions import ValidationError

from .models import Like
from mainapp.utils import DateUtil


class LikeFilter(django_filters.FilterSet):

    start_date = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        required=True,
    )

    end_date = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        required=True,
    )

    post_id = django_filters.NumberFilter(field_name="post__id")

    class Meta:
        model = Like
        fields = ("start_date", "end_date", "post_id")

    def is_valid(self):
        self.validate_datetime(self.request)
        return super().is_valid()

    @staticmethod
    def validate_datetime(request) -> None:

        error_dict = {}

        start_date = DateUtil(request.query_params.get("start_date"))
        end_date = DateUtil(request.query_params.get("end_date"))

        if start_date.date and end_date.date:

            if start_date.is_str_in_datetime_format() and end_date.is_str_in_datetime_format():

                if start_date.format_str_to_date() > end_date.format_str_to_date():
                    error_dict[
                        "start_date"
                    ] = "start_date must be less/equal than end_date"

            else:
                error_dict["error"] = "dates must be in YYYY-MM-DD format"

        else:
            error_dict["error"] = "start_date and end_date are both required"

        if error_dict:
            raise ValidationError(error_dict)
