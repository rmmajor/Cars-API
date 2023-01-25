from rest_framework.viewsets import ModelViewSet
from rest_access_policy import AccessPolicy


class DefaultAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "authenticated",
            "effect": "allow",
        },
        {
            "action": ["create", "destroy", "update", "partial_update"],
            "principal": "admin",
            "effect": "allow",
        },
    ]
