import django_filters
from django.utils.timezone import datetime
from rest_framework.exceptions import ValidationError

from .models import Like


class LikeFilter(django_filters.FilterSet):

    start_date = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        required=True,
    )

    end_date = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte", required=True
    )

    post_id = django_filters.NumberFilter(field_name="post__id")

    class Meta:
        model = Like
        fields = ("start_date", "end_date", "post_id")

    def is_valid(self):
        is_valid = super().is_valid()
        start_date = self.request.query_params.get("start_date", "")
        end_date = self.request.query_params.get("end_date", "")

        if start_date and end_date:
            if datetime.strptime(start_date, "%Y-%m-%d") > datetime.strptime(
                end_date, "%Y-%m-%d"
            ):
                raise ValidationError(
                    {"start_date": "Start date must be earlier than end date"}
                )

        return is_valid
