from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
	"""
	Custom permission to allow only the author of blog to edit the blog.
	"""
	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		# Write permissons are only granted to authors of blog.
		return obj.blog_author == request.user


class HasAuthorGroupOrReadOnly(permissions.BasePermission):
	"""Only users with Author group can post new blog."""
	def has_permission(self, request, view):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		# post permission is only for author group.
		return request.user.groups.filter(name='author').exists()