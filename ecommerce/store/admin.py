from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Cart, CartItem, ProductHistory, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    
    def get_readonly_fields(self, request, obj=None):
        # Make price readonly if the order already exists
        if obj and obj.id:
            return ['price']
        return []
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Override to set the price field to the product's price when adding a new item"""
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'product' and hasattr(field, 'widget'):
            # Add JavaScript to update price when product changes
            field.widget.attrs['onchange'] = 'updatePrice(this)'
        return field


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Show 3 empty forms for adding images
    fields = ['image', 'image_url', 'alt_text', 'is_primary']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'stock', 'available', 'created_at']
    list_filter = ['available', 'created_at', 'category']
    list_editable = ['price', 'stock', 'available']
    search_fields = ['name', 'description']
    prepopulated_fields = {'name': ('name',)}
    date_hierarchy = 'created_at'
    ordering = ['name']
    inlines = [ProductImageInline]  # Add inline form for product images

    def save_model(self, request, obj, form, change):
        """Override save_model to create history record before saving changes"""
        if change:  # Only create history if this is an edit, not a new product
            # Get the original object from the database
            original_obj = Product.objects.get(pk=obj.pk)
            # Create history record
            ProductHistory.create_from_product(original_obj)
        super().save_model(request, obj, form, change)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    readonly_fields = ['subtotal_price', 'discount_amount', 'total_price']
    
    class Media:
        js = ('js/admin/order_edit.js',)
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure totals are updated"""
        obj.update_totals()
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        """Override save_formset to update prices from products and update order totals"""
        instances = formset.save(commit=False)
        
        # For new items, set price based on the product
        for instance in instances:
            if not instance.price:  # If price is not set
                instance.price = instance.product.price
            instance.save()
            
        # Delete objects marked for deletion
        for obj in formset.deleted_objects:
            obj.delete()
            
        # Update the order totals after all items are saved or deleted
        if formset.model == OrderItem and instances:
            order = form.instance
            order.update_totals()
            
        formset.save_m2m()


class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    date_hierarchy = 'created_at'
    inlines = [CartItemInline]


@admin.register(ProductHistory)
class ProductHistoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name']
    date_hierarchy = 'created_at'
    readonly_fields = ['product', 'data', 'created_at']

    def has_add_permission(self, request):
        return False  # Prevent manual creation of history records


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary', 'alt_text', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name', 'alt_text']
