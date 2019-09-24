import os.path
import pkg_resources


RESOURCES_PATH = 'resources'
TEMPLATES_PATH = os.path.join(RESOURCES_PATH, 'templates')
STYLESHEETS_PATH = os.path.join(RESOURCES_PATH, 'stylesheets')
SOURCEVIEW_STYLES_PATH = os.path.join(RESOURCES_PATH, 'gtksourceview-styles')
SOURCEVIEW_LANGUAGES_PATH = os.path.join(RESOURCES_PATH,
                                         'gtksourceview-language-specs')


def template_resource(template_id):
    template_path = os.path.join(TEMPLATES_PATH, '{}.html'.format(template_id))
    return pkg_resources.resource_string(
        'nete',
        template_path).decode('utf-8')


def stylesheet_filename(stylesheet_id):
    stylesheet_filename = os.path.join(
        STYLESHEETS_PATH,
        '{}.css'.format(stylesheet_id))
    return pkg_resources.resource_filename(
        'nete',
        stylesheet_filename)


def sourceview_styles_dir():
    return pkg_resources.resource_filename(
        'nete',
        SOURCEVIEW_STYLES_PATH)


def sourceview_languages_dir():
    return pkg_resources.resource_filename(
        'nete',
        SOURCEVIEW_LANGUAGES_PATH)
