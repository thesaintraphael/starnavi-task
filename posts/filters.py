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

        is_valid = super().is_valid()
        error_dict = {}

        start_date = DateUtil(
            (self.request.query_params.get("start_date"))
        ).format_str_to_date()
        end_date = DateUtil(
            (self.request.query_params.get("end_date"))
        ).format_str_to_date()

        if start_date and end_date:
            if start_date > end_date:
                error_dict["start_date"] = "Start date must be less/equal than end date"
                error_dict[
                    "end_date"
                ] = "End date must be greater/equal than start date"

            if start_date.month != end_date.month:
                error_dict[
                    "start_date"
                ] = "Start date must be in the same month as end date"

        else:
            error_dict["error"] = "start_date and end_date are required"

        if error_dict:
            raise ValidationError(error_dict)

        return is_valid
