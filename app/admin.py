from django.contrib import admin
from app.models import ( Restaurants, 
                        RestaurantFinance, 
                        Review, 
                        Menu, 
                        Inventory, 
                        CustomerOrder, 
                        Staff, 
                        ShiftManager )

@admin.register(Restaurants)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = (
                    'name',
                    'date_opened',
                    'capacity',
                    'nick_name',
                    'profitable'
    )
    
    def profitable(self, obj):
        finance = RestaurantFinance.objects.filter(restaurant = obj).first()
        if finance:
            return finance.is_profitable_bool
        return False
    profitable.short_description = 'Profitable ?'

@admin.register(RestaurantFinance)
class RestaurantFinanceAdmin(admin.ModelAdmin):
    list_display = ('restaurant',
                    'income',
                    'expenditures',
                    'sales',
                    'revenue',)
    search_fields = ('restaurant',)
    list_filter = ('income','expenditures','sales',)

    def revenue(self, obj):
        return obj.income - obj.expenditures
    revenue.short_description = 'Profit'
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name',
                    'review_type',
                    'rating',
                    'review_target',
                    'did_user_leave_a_comment',
                    )
    search_fields = ('customer_name','review_target',)
    list_filter = ('customer_name','review_type','rating')

    def did_user_leave_a_comment(self, obj):
        return True if obj.comment else False
    did_user_leave_a_comment.short_description = 'comment_present'

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('restaurant',
                    'inventory_item',  
                    'price',
                    'is_available',
                    )
    search_fields = ('inventory_item__name', 'restaurant',)
    list_filter = ('restaurant', 'price', 'is_available',)

    def is_available(self, obj):
        inventory = Inventory.objects.filter(name=obj.inventory_item.name).first()
        return True if inventory and inventory.quantity > 0 else False
    is_available.short_description = 'available'

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('restaurant',
                    'name',
                    'in_stock',
                    )
    search_fields = ('restaurant','name',)
    list_filter = ('restaurant',)

    def in_stock(self, obj):
        return True if obj.quantity > 0 else False
    in_stock.short_description = 'available'
    
@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = (
        'restaurant',
        'customer_name',
        'order_price',
        'item_list',
        'item_count',
    )
    search_fields = ('restaurant__name', 'customer_name',)
    list_filter = ('restaurant', 'order_price', 'customer_name',)

    def item_list(self, obj):
        return ", ".join([item.inventory_item.name for item in obj.items.all()])
    item_list.short_description = 'Items in Order'

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Total Items'

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('full_name',
                    'role',
                    )
    search_fields = ('name','surname',)
    list_filter = ('name','role',)

    def full_name(self, obj):
        return f"{obj.name} {obj.surname}"
    full_name.short_description = 'Full Name'


@admin.register(ShiftManager)
class ShiftManagerAdmin(admin.ModelAdmin):
    list_display = ('staff',
                    'role',
                    'shift_duration',
                    )
    search_fields = ('staff',)
    list_filter = ('staff',)

    def role(self, obj):
        return obj.staff.role
    
    
    def shift_duration(self, obj):
        return (obj.end_time - obj.start_time).total_seconds() / 3600
    shift_duration.short_description = 'Duration'