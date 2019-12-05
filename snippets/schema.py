from rest_framework import schemas
from rest_framework.compat import coreapi, coreschema


custom_schema = schemas.ManualSchema(
    fields=[
        coreapi.Field(
            "id",
            required=True,
            location="path",
            schema=coreschema.String(
                title="ID",
                description="Foobar ID.",
            )
        ),
        coreapi.Field(
            "foobar",
            location="query",
            schema=coreschema.String(
                title="Foobar",
                description="Foobar?",
            )
        ),
    ],
    description="",
)