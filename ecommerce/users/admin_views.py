from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db.models import Count, Sum, Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to check if user is admin/staff"""
    def test_func(self):
        return self.request.user.is_staff


class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'users/admin/user_list.html'
    context_object_name = 'users'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('profile', 'groups')
        search_query = self.request.GET.get('search', '')
        user_type = self.request.GET.get('user_type', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) | 
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
            
        if user_type:
            if user_type == 'staff':
                queryset = queryset.filter(is_staff=True, is_superuser=False)
            elif user_type == 'admin':
                queryset = queryset.filter(is_superuser=True)
            elif user_type == 'customer':
                queryset = queryset.filter(is_staff=False, is_superuser=False)
                
        return queryset.order_by('-date_joined')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['user_type'] = self.request.GET.get('user_type', '')
        
        # Count different user types
        context['total_users'] = User.objects.count()
        context['total_staff'] = User.objects.filter(is_staff=True, is_superuser=False).count()
        context['total_admins'] = User.objects.filter(is_superuser=True).count()
        context['total_customers'] = User.objects.filter(is_staff=False, is_superuser=False).count()
        
        return context


class UserDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = User
    template_name = 'users/admin/user_detail.html'
    context_object_name = 'user_obj'  # Use user_obj to avoid conflict with the request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_obj = self.get_object()
        
        # Get profile information
        try:
            context['profile'] = user_obj.profile
        except Profile.DoesNotExist:
            context['profile'] = None
            
        # Get order information if store app has Order model
        try:
            from store.models import Order
            context['orders'] = Order.objects.filter(user=user_obj).order_by('-created_at')
            context['order_count'] = context['orders'].count()
            context['total_spent'] = context['orders'].aggregate(Sum('total_price'))['total_price__sum'] or 0
        except (ImportError, AttributeError):
            context['orders'] = []
            context['order_count'] = 0
            context['total_spent'] = 0
            
        return context


class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/admin/user_form.html'
    success_url = reverse_lazy('users:admin_user_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        
        # Create profile
        Profile.objects.create(user=user)
        
        # Set staff status if chosen
        user_type = self.request.POST.get('user_type', 'customer')
        if user_type == 'staff':
            user.is_staff = True
            user.save()
        elif user_type == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()
            
        # Add to appropriate group
        group_name = 'Customer' if user_type == 'customer' else 'Staff'
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        
        messages.success(self.request, f'User "{user.username}" has been created successfully!')
        return response
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New User'
        context['button_label'] = 'Create User'
        return context


class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/admin/user_form.html'
    
    def get_success_url(self):
        return reverse('users:admin_user_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            context['profile_form'] = ProfileUpdateForm(
                self.request.POST,
                instance=self.get_profile_instance()
            )
        else:
            context['profile_form'] = ProfileUpdateForm(instance=self.get_profile_instance())
            
        context['title'] = f'Edit User: {self.object.username}'
        context['button_label'] = 'Update User'
        return context
        
    def get_profile_instance(self):
        try:
            return self.object.profile
        except Profile.DoesNotExist:
            return Profile(user=self.object)
            
    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']
        
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            
            # Make sure profile is linked to user
            profile.user = self.object
            profile.save()
            
            # Update user type
            user_type = self.request.POST.get('user_type', None)
            if user_type:
                if user_type == 'admin':
                    self.object.is_staff = True
                    self.object.is_superuser = True
                elif user_type == 'staff':
                    self.object.is_staff = True
                    self.object.is_superuser = False
                else:  # customer
                    self.object.is_staff = False
                    self.object.is_superuser = False
                self.object.save()
            
            messages.success(self.request, f'User "{self.object.username}" has been updated successfully!')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'users/admin/user_confirm_delete.html'
    success_url = reverse_lazy('users:admin_user_list')
    context_object_name = 'user_obj'
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        username = user.username
        
        # Don't allow deleting yourself
        if user == request.user:
            messages.error(request, "You cannot delete your own account!")
            return redirect(self.success_url)
        
        # Proceed with deletion
        user.delete()
        messages.success(request, f'User "{username}" has been deleted successfully!')
        return redirect(self.success_url)


class ResetUserPasswordView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = SetPasswordForm
    template_name = 'users/admin/reset_password.html'
    context_object_name = 'user_obj'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object
        return kwargs
    
    def get_success_url(self):
        return reverse('users:admin_user_detail', kwargs={'pk': self.object.pk})
        
    def form_valid(self, form):
        form.save()
        messages.success(self.request, f'Password for user "{self.object.username}" has been reset successfully!')
        return super().form_valid(form)
