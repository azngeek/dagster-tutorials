from typing import Any

from pydantic import Field

import dagster as dg


class MyLegacyApiClient(dg.ConfigurableResource):

    api_key: str = Field(..., description="Secret API Key")

    def __init__(self, **data: Any):
        super().__init__(**data)