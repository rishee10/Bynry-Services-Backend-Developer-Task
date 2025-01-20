from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from .models import ServiceRequest

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('track_requests')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

@method_decorator(login_required, name='dispatch')
class SubmitRequestView(View):
    def get(self, request):
        return render(request, 'submit_request.html')

    def post(self, request):
        type_of_service = request.POST['type_of_service']
        details = request.POST['details']
        attached_file = request.FILES.get('attached_file')

        ServiceRequest.objects.create(
            customer=request.user,
            type_of_service=type_of_service,
            details=details,
            attached_file=attached_file
        )
        return redirect('track_requests')

@method_decorator(login_required, name='dispatch')
class TrackRequestsView(View):
    def get(self, request):
        requests = ServiceRequest.objects.filter(customer=request.user).order_by('-created_at')
        return render(request, 'track_requests.html', {'requests': requests})

@method_decorator(login_required, name='dispatch')
class ManageRequestsView(View):
    def get(self, request):
        if not request.user.is_staff:
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        requests = ServiceRequest.objects.all().order_by('-created_at')
        return render(request, 'manage_request.html', {'requests': requests})

    def post(self, request):
        if not request.user.is_staff:
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        request_id = request.POST['request_id']
        status = request.POST['status']

        service_request = ServiceRequest.objects.get(id=request_id)
        service_request.status = status
        if status == 'Resolved':
            service_request.resolved_at = timezone.now()
        service_request.save()

        return JsonResponse({'success': True})
