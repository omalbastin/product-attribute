# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

_logger = logging.getLogger(__name__)


try:
    from odoo.addons.base_multi_image.hooks import (
        pre_init_hook_for_submodules,
        uninstall_hook_for_submodules,
    )
except ImportError:
    _logger.info("Cannot import base_multi_image hooks")


def pre_init_hook(env):
    pre_init_hook_for_submodules(env, "product.template", "image_1920")
    pre_init_hook_for_submodules(env, "product.product", "image_variant_1920")

def post_init_hook(env):
    product_images = env['base_multi_image.image'].search([
        ('owner_model', '=', 'product.product'),
    ])
    for image in product_images:
        product = env['product.product'].browse(image.owner_id)
        image.write({'owner_model': 'product.template',
                     'owner_id': product.product_tmpl_id.id,
                     'product_variant_ids': [(6, 0, [image.owner_id])]})


def uninstall_hook(env):
    """Remove multi images for models that no longer use them."""
    uninstall_hook_for_submodules(env, "product.template")
    uninstall_hook_for_submodules(env, "product.product")
