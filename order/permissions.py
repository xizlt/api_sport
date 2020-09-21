from rest_framework.permissions import SAFE_METHODS, BasePermission


class OrderPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and (obj.user == request.user or request.user.is_staff)
        )

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_authenticated or request.user.is_staff
        )


class ItemViewPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and (obj.order.user.id == request.user.id or request.user.is_staff)
        )

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_authenticated or request.user.is_staff
        )
