from django.contrib import admin
from .models import UserProfile, Reward, RedemptionHistory, DepositTransaction

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'points_balance')

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('title', 'points_required', 'stock')

@admin.register(RedemptionHistory)
class RedemptionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'reward', 'code', 'redeemed_at')

@admin.register(DepositTransaction)
class DepositTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'points_added', 'status', 'created_at')
    list_filter = ('status',)

    def save_model(self, request, obj, form, change):
        # Nếu trạng thái chuyển thành COMPLETED thì cộng điểm cho user
        if change:
            old_obj = DepositTransaction.objects.get(pk=obj.pk)
            if old_obj.status != 'COMPLETED' and obj.status == 'COMPLETED':
                profile, _ = UserProfile.objects.get_or_create(user=obj.user)
                profile.points_balance += obj.points_added
                profile.save()
        super().save_model(request, obj, form, change)