import dagster as dg


@dg.asset()
def old_asset() -> bool:
    """
    This is an example, how assets looked in the past. So prior Dagster 1.10
    Assets would not be autoloaded but instead registered manually in the definitions.py file
    """
    pass