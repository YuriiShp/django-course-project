from django.contrib.auth.models import Group
from rest_framework import permissions


"""Check if user is in the certain group"""
def is_in_group(user, group_name):

    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


class HasGroupPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # Get a mapping of methods -> required group
        required_group_mapping = getattr(view, "required_groups", {})

        # Determine the required groups for this particular request methods
        required_groups = required_group_mapping.get(request.method, [])

        # rquest user has admin permission
        if request.user.is_staff:
            return True

        # request user is not admin but is in permited groups
        res_list = []
        for  group_name in required_groups:
            if group_name != '__all__':
                res_list.append(is_in_group(request.user, group_name))
            else:
                res_list.append(True)
        return all(res_list)
