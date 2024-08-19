from nautobot.apps.tables import BaseTable, ToggleColumn
from nautobot.extras.tables import StatusTableMixin


class MyTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        fields = "__all__"
