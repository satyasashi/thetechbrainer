def banner_path(instance, filename):
    return "user_{0}/banners/{1}".format(instance.blog_author.user.id, filename)


def use_directory_path(instance, filename):
    return "user_{0}/profile-pics/{1}".format(instance.user_fk.user_name.id, filename)


def banner_directory_path(instance, filename):
    return "user_{0}/banners/{1}".format(instance.blog_author.user.username.id, filename)
