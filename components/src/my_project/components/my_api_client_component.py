import dagster as dg

from legacy.resources.my_legacy_api_client import MyLegacyApiClient

class MyApiClientScaffolder(dg.Scaffolder):
    """Scaffolds a template shell script alongside a filled-out defs.yaml file."""

    def scaffold(self, request: dg.ScaffoldRequest) -> None:
        dg.scaffold_component(
            request,
            {
                "api_key": "<your_api_key>"
            },
        )

@dg.scaffold_with(MyApiClientScaffolder)
class MyApiClientComponent(dg.Component, dg.Model, dg.Resolvable):
    """COMPONENT SUMMARY HERE.

    COMPONENT DESCRIPTION HERE.
    """
    api_key: str

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        # Add definition construction logic here.
        return dg.Definitions(
            resources={
                'my_new_strapi_client': MyLegacyApiClient(api_key=self.api_key)
            }
        )
