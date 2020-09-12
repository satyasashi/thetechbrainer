# from django.conf import settings
#
#
# def banner_path(instance, filename):
#     return "user_{0}/banners/{1}".format(instance.blog_author.user.id, filename)
#
#
# def category_img_path(instance, filename):
#     return "category/{0}/{1}".format(instance.category_name, filename)
#
#
# def get_category_img_thumbnail_path(category_name, img_name):
#     img_name = img_name.split("/")[-1]
#     thumbnail_path = settings.MEDIA_ROOT+"/category/"+str(category_name)+"/thumbnails/"+img_name
#     return thumbnail_path
#
#
# def use_directory_path(instance, filename):
#     return "user_{0}/profile-pics/{1}".format(instance.user_fk.user_name.id, filename)
#
#
# def banner_directory_path(instance, filename):
#     return "user_{0}/banners/{1}".format(instance.blog_author.user.username.id, filename)
