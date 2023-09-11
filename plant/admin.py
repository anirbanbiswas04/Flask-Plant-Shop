from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.form import SecureForm, ImageUploadField
from flask_admin.contrib.sqla import ModelView
import PIL
from flask_wtf.csrf import _FlaskFormCSRF
from wtforms.meta import DefaultMeta
from plant import app, db
from flask import redirect, current_app, session
from flask_login import current_user
import os


app.config['FLASK_ADMIN_SWATCH'] = 'yeti'

class DashboardView(AdminIndexView):

    def is_visible(self):
        return False

admin = Admin(app, name='Plant Admin', template_mode='bootstrap4', index_view=DashboardView())

media_path = os.path.join(os.path.dirname(__file__), 'images/')

try:
    os.mkdir(media_path)
except OSError:
    pass

from plant.shop.models import Category, Product, Order, OrderItem

class CustomSecureForm(SecureForm):
    class Meta(DefaultMeta):
        csrf_class = _FlaskFormCSRF
        csrf_context = session

        @property
        def csrf_secret(self):
            return current_app.config.get('WTF_CSRF_SECRET_KEY',
                                          current_app.secret_key)

class CategoryAdmin(ModelView):
    form_base_class = CustomSecureForm
    form_columns = ['name', 'slug']
    column_searchable_list = ['name']
    column_filters = ['name']
    form_excluded_columns = ['products']
    edit_modal = True

    def is_accessible(self):
        return True if current_user.is_authenticated and current_user.is_superuser else False

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/admin')
    
class ProductAdmin(ModelView):
    form_base_class = CustomSecureForm
    form_columns = ['name', 'category', 'slug', 'price', 'description', 'how_to_maintain', 'where_to_keep', 'image']
    page_size = 15
    column_searchable_list = ['name', 'description', 'price']
    column_filters = ['category.name', 'price']
    column_editable_list = ['name', 'category', 'price', 'description', 'how_to_maintain', 'where_to_keep', 'image']
    column_exclude_list = ['how_to_maintain', 'where_to_keep']
    can_view_details = True

    form_extra_fields = {
        'image': ImageUploadField(
            'Image', 
            base_path=media_path
            )
    }

    def on_model_delete(self, model):
        if model.image:
            try:
                image_path = os.path.join(media_path, model.image)
                os.remove(image_path)
            except:
                pass

    def is_accessible(self):
        return True if current_user.is_authenticated and current_user.is_superuser else False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/admin')

class OrderAdmin(ModelView):
    form_base_class = CustomSecureForm
    page_size = 15
    form_columns = ['full_name', 'email_address', 'city', 'postal_code', 'state', 'phone_no', 'nearest_landmark', 'created_at', 'is_shipped', 'total_amount']
    column_searchable_list = ['full_name', 'email_address', 'phone_no', 'total_amount']
    column_filters = ['is_shipped']
    column_editable_list = ['is_shipped']
    can_export = True
    inline_models = (OrderItem,) 
    can_delete = False
    can_view_details = True

    def is_accessible(self):
        return True if current_user.is_authenticated and current_user.is_superuser else False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/admin')
    
    column_default_sort = ('created_at', True)
    
class MediaAdmin(FileAdmin):
    form_base_class = CustomSecureForm
    def is_accessible(self):
        return True if current_user.is_authenticated and current_user.is_superuser else False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/admin')

admin.add_view(ProductAdmin(Product, db.session))
admin.add_view(CategoryAdmin(Category, db.session))
admin.add_view(OrderAdmin(Order, db.session))
admin.add_view(MediaAdmin(media_path, '/images/', name='Media Files'))