from nautobot.apps.tables import BaseTable
from nautobot.apps.tables import ToggleColumn
from nautobot.extras.tables import StatusTableMixin


class MyTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        fields = ("pk", "my_field1", "my_field2")
