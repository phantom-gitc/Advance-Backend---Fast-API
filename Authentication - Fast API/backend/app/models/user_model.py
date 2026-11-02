from typing import Any, Dict


def serialize_user(user: Dict[str, Any]) -> Dict[str, Any]:
    # Convert MongoDB document into clean dictionary and hide password hash
    if not user:
        return {}
    return {
        "id": str(user["_id"]),
        "full_name": user.get("full_name", ""),
        "email": user.get("email", ""),
        "role": user.get("role", "user"),
        "is_active": user.get("is_active", True),
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at"),
    }
