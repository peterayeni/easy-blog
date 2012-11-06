from easy_blog.models import Config

def config(request):
    """
    Adds configuration information to the context.

    To employ, add the conf method reference to your project
    settings TEMPLATE_CONTEXT_PROCESSORS.

    Example:
        TEMPLATE_CONTEXT_PROCESSORS = (
            ...
            "easy_blog.context_processors.config",
        )
    """
    return {'easy_blog_config': Config.get_current()}
