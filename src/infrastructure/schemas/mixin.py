from datetime import datetime

from annotated_types import Timezone
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
        comment="Timestamp when created"
    )

    last_modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),  # Crucial for auto-update
        nullable=True,
        comment="Timestamp when the record was last modified"
    )
