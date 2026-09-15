from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Đảm bảo đã import đầy đủ các models này:
from .models import Reward, UserProfile, RedemptionHistory, DepositTransaction, ChatMessage

def home(request):
    rewards = Reward.objects.all()
    return render(request, 'core/home.html', {'rewards': rewards})

@login_required
def redeem_reward(request, reward_id):
    if request.method == 'POST':
        reward = get_object_or_404(Reward, id=reward_id)
        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        if profile.points_balance < reward.points_required:
            messages.error(request, 'Bạn không đủ điểm để đổi quà này!')
            return redirect('home')

        if reward.stock <= 0:
            messages.error(request, 'Món quà này đã hết hàng!')
            return redirect('home')

        # Trừ điểm và giảm tồn kho
        profile.points_balance -= reward.points_required
        profile.save()

        reward.stock -= 1
        reward.save()

        # Tạo lịch sử đổi quà kèm mã Code
        redemption = RedemptionHistory.objects.create(user=request.user, reward=reward)
        messages.success(request, f'Đổi quà thành công! Mã Voucher của bạn là: {redemption.code}')
        return redirect('history')

    return redirect('home')

@login_required
def deposit(request):
    if request.method == 'POST':
        amount = request.POST.get('amount', '0')
        bank_id = "VCB"
        account_no = "1042794878"
        account_name = "Hoang Duc Thai"
        add_info = f"NAP {request.user.username}"
        qr_url = f"https://img.vietqr.io/image/{bank_id}-{account_no}-compact2.png?amount={amount}&addInfo={add_info}&accountName={account_name}"
        
        context = {
            'amount': amount,
            'qr_url': qr_url,
            'bank_name': 'Vietcombank (VCB)',
            'account_no': account_no,
            'account_name': account_name,
            'add_info': add_info,
            'show_qr': True
        }
        return render(request, 'core/deposit.html', context)
    
    return render(request, 'core/deposit.html', {'show_qr': False})


@login_required
def history(request):
    redemptions = RedemptionHistory.objects.filter(user=request.user).order_by('-redeemed_at')
    deposits = DepositTransaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/history.html', {
        'redemptions': redemptions,
        'deposits': deposits
    })
    from django.http import JsonResponse
from .models import ChatMessage # Thêm ChatMessage vào import models của bạn

@login_required
def chat_room(request):
    """Giao diện chat: Admin thấy danh sách User, User thấy khung chat với Admin"""
    if request.user.is_staff:
        users = User.objects.filter(is_staff=False)
        selected_user_id = request.GET.get('user_id')
        selected_user = None
        messages_list = []
        
        if selected_user_id:
            selected_user = get_object_or_404(User, id=selected_user_id)
            messages_list = ChatMessage.objects.filter(
                (Q(sender=request.user) & Q(receiver=selected_user)) |
                (Q(sender=selected_user) & Q(receiver=request.user))
            ).order_by('timestamp')

        return render(request, 'core/admin_chat.html', {
            'users': users,
            'selected_user': selected_user,
            'messages_list': messages_list
        })
    else:
        admin_user = User.objects.filter(is_staff=True).first()
        messages_list = []
        if admin_user:
            messages_list = ChatMessage.objects.filter(
                (Q(sender=request.user) & Q(receiver=admin_user)) |
                (Q(sender=admin_user) & Q(receiver=request.user))
            ).order_by('timestamp')

        return render(request, 'core/user_chat.html', {
            'admin_user': admin_user,
            'messages_list': messages_list
        })

@login_required
def send_message(request):
    """API Gửi tin nhắn 1:1"""
    if request.method == 'POST':
        msg_text = request.POST.get('message', '').strip()
        receiver_id = request.POST.get('receiver_id')
        
        if msg_text and receiver_id:
            receiver = get_object_or_404(User, id=receiver_id)
            chat_msg = ChatMessage.objects.create(
                sender=request.user,
                receiver=receiver,
                message=msg_text
            )
            return JsonResponse({
                'status': 'ok',
                'sender': chat_msg.sender.username,
                'message': chat_msg.message,
                'timestamp': chat_msg.timestamp.strftime('%H:%M')
            })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_messages(request):
    """API Tải tin nhắn mới 1:1"""
    partner_id = request.GET.get('partner_id')
    if not partner_id:
        return JsonResponse({'messages': []})

    partner = get_object_or_404(User, id=partner_id)
    messages_list = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=partner)) |
        (Q(sender=partner) & Q(receiver=request.user))
    ).order_by('timestamp')

    data = [
        {
            'sender': msg.sender.username,
            'message': msg.message,
            'timestamp': msg.timestamp.strftime('%H:%M'),
            'is_me': msg.sender == request.user
        }
        for msg in messages_list
    ]
    return JsonResponse({'messages': data})
def register(request):
    """Trang đăng ký tài khoản người dùng mới"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})