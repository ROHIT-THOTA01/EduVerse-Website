from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView,View
from courses.models import Course,Lesson,Category
from memberships.models import UserMembership
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        context['category'] = category
        return context

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

class CourseListView(ListView):
    context_object_name = 'courses'
    template_name = 'courses/course_list.html'
    model = Course


class CourseDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'
    model = Course
    login_url = '/accounts/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        lessons = course.lessons
        context['lessons'] = lessons
        
        # Check if user has access to this course
        has_access = False
        try:
            user_membership = UserMembership.objects.get(user=self.request.user)
            if user_membership.membership:
                user_membership_type = user_membership.membership.membership_type
                course_allowed_membership_type = course.allowed_memberships.all()
                if course_allowed_membership_type.filter(membership_type=user_membership_type).exists():
                    has_access = True
        except UserMembership.DoesNotExist:
            pass
        
        context['has_access'] = has_access
        
        # Get demo/free preview lessons (accessible to all users)
        demo_lessons = lessons.filter(is_free_preview=True)
        context['demo_lessons'] = demo_lessons
        context['has_demo_lessons'] = demo_lessons.exists()
        
        # Get first lesson for initial video display
        # Show video player if user has access OR if there are demo lessons
        context['showing_demo'] = False  # Default value
        if lessons and lessons.exists():
            # Prioritize showing a demo lesson if available and user doesn't have access
            if not has_access and demo_lessons.exists():
                first_lesson = demo_lessons.first()
                context['first_lesson'] = first_lesson
                context['showing_demo'] = True
            elif has_access:
                first_lesson = lessons.first()
                context['first_lesson'] = first_lesson
                # Check if the first lesson is actually a demo lesson
                if first_lesson and first_lesson.is_free_preview:
                    context['showing_demo'] = True
                else:
                    context['showing_demo'] = False
        return context

class LessonDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        
        # Check if lesson is a free preview (accessible to all users)
        if lesson.is_free_preview:
            context = {'lesson': lesson, 'is_demo': True}
            return render(request, "courses/lesson_detail.html", context)
        
        # Check if user has a membership for paid lessons
        try:
            user_membership = UserMembership.objects.get(user=request.user)
            if user_membership.membership:
                user_membership_type = user_membership.membership.membership_type
                course_allowed_membership_type = course.allowed_memberships.all()
                context = { 'lesson': None }
                if course_allowed_membership_type.filter(membership_type=user_membership_type).exists():
                    context = {'lesson': lesson, 'is_demo': False}
                else:
                    messages.info(request, 'You need to upgrade your membership to access this lesson.')
            else:
                context = { 'lesson': None }
                messages.info(request, 'You need to select a membership to access this lesson.')
        except UserMembership.DoesNotExist:
            context = { 'lesson': None }
            messages.info(request, 'You need to create a membership to access this lesson.')
        
        return render(request, "courses/lesson_detail.html", context)
