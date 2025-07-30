from pathlib import Path
from legacy.assets import assets
import dagster as dg

from legacy.resources.my_legacy_api_client import MyLegacyApiClient

# For legacy dagster projects, this was the best practice

# defs = dg.Definitions(
#     assets=dg.load_assets_from_modules([assets]),
#     resources={
#         'my_legacy_api_client': MyLegacyApiClient(api_key='donttellme')
#     }
# )

# In newer projects you will only use the auto loading features
# @dg.definitions
# def defs():
#     return dg.load_from_defs_folder(project_root=Path(__file__).parent.parent.parent)


# This is a combination of auto loading and manually registering assets and resources.
@dg.definitions
def defs():
    return (
        dg.Definitions.merge(
            dg.Definitions(
                assets=dg.load_assets_from_modules([assets]),
                resources={
                    'my_legacy_api_client': MyLegacyApiClient(api_key='donttellme')
                }
            ),
            dg.load_from_defs_folder(project_root=Path(__file__).parent.parent.parent)
        )
    )

