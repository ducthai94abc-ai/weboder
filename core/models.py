from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    points_balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.points_balance} điểm"

class Reward(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    points_required = models.IntegerField()
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='rewards/', blank=True, null=True)

    def __str__(self):
        return self.title

class RedemptionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    redeemed_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            # Tự động tạo mã Voucher ngẫu nhiên dạng VOUCHER-XXXXXX
            self.code = f"VC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.reward.title} ({self.code})"

class DepositTransaction(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Chờ duyệt'),
        ('COMPLETED', 'Thành công'),
        ('FAILED', 'Thất bại'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(help_text="Số tiền VND (1.000 VNĐ = 1 điểm)")
    points_added = models.IntegerField(help_text="Số điểm sẽ nhận")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Nạp {self.amount:,}đ ({self.get_status_display()})"
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Từ {self.sender.username} đến {self.receiver.username if self.receiver else 'Tất cả'}: {self.message[:20]}"