from django.contrib import admin
from app.models import ( Restaurants, 
                        RestaurantFinance, 
                        Review, 
                        Menu, 
                        Inventory, 
                        CostumerOrder, 
                        Staff, 
                        ShiftManager )

@admin.register(Restaurants)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ('name', # Columns shown in the list view of Admin
                     'date_opened',
                      'restaurant_type',
                      'nick_name',
                      'capacity',
                      'get_income', 'get_expenditure', 'sales') # Custom methods  
    search_fields = ('name', 'nick_name') # Adds a search box for these fields
    list_filter = ('restaurant_type','capacity') # Filter

    def get_income(self, obj):
        finanace = RestaurantFinance.objects.filter(restaurant = obj).first()
        return finanace.income if finanace else 'N/A'
    get_income.short_description = 'Income'

    def get_expenditure(self, obj):
        finance = RestaurantFinance.objects.filter(restaurant = obj).first()
        return finance.expenditures if finance else 'N/A'
    get_expenditure.short_description = 'Expenditures'

    def sales(self, obj): # Self represents the admin instance, obj represents the model row instance
        finance = RestaurantFinance.objects.filter(restaurant = obj).first()
        return finance.sales if finance else 'N/A'
    sales.short_description = 'Sales'


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
                    'name',
                    'price',
                    'is_available',
                    )
    search_fields = ('name','restaurant',)
    list_filter = ('restaurant','price','is_available',)

    def is_available(self, obj):
        inventory = Inventory.objects.filter(name = obj.name).first()
        return True if inventory.quantity > 0 else False
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
    
@admin.register(CostumerOrder)
class 

admin.site.register(CostumerOrder)
admin.site.register(Staff)
admin.site.register(ShiftManager)