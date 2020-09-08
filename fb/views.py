from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import MyPost, MyProfile, FollowUser, PostLike, PostComment
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'fb/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #follow system
        followedList = FollowUser.objects.filter(followed_by = self.request.user.myprofile)
        followedPost = []
        for f in followedList:
            followedPost.append(f.profile)
        
        #search system
        si = self.request.GET.get('si')
        if si == None:
            si = ''
        postList = MyPost.objects.filter(Q(uploaded_by__in=followedPost)).filter(
            Q(subject__icontains=si)).filter(Q(msg__icontains=si)).order_by('-id')
        
        
        #like system
        for p1 in postList:
            p1.liked = False
            Liked = PostLike.objects.filter(post=p1, liked_by = self.request.user.myprofile)
            if Liked:
                p1.liked = True
            Liked = PostLike.objects.filter(post=p1)
            p1.likecount = Liked.count()
       
        context={
            'mypost_list': postList,
            
        }
        
        return context
    


@method_decorator(login_required, name='dispatch')
class About(TemplateView):
    template_name = 'fb/about.html'


@method_decorator(login_required, name='dispatch')
class Contact(TemplateView):
    template_name = 'fb/contact.html'

# MyPost Views starts here
@method_decorator(login_required, name='dispatch')
class MyPostListView(ListView):
    model = MyPost
    def get_queryset(self):
        si = self.request.GET.get('si')
        if si == None:
            si = ''
        postList =  MyPost.objects.filter(Q(uploaded_by=self.request.user.myprofile)).filter(Q(subject__icontains=si)).filter(Q(msg__icontains=si)).order_by('-id')
        for p in postList:
            p.liked = False
        Liked = PostLike.objects.filter(post = p, liked_by = self.request.user.myprofile)
        if Liked:
            p.liked = True
        Liked = PostLike.objects.filter(post = p)
        p.likecount = Liked.count()
        
        return postList


@method_decorator(login_required, name='dispatch')
class MyPostDetailView(DetailView):
    model = MyPost 


@method_decorator(login_required, name='dispatch')
class MyPostCreateView(CreateView):
    model = MyPost
    fields = ['subject', 'msg', 'pic']
    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user.myprofile
        self.object.save()
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class MyPostUpdateView(UpdateView):
    model = MyPost
    fields = ['subject', 'msg', 'pic']
    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user.myprofile
        self.object.save()
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class MyPostDeleteView(DeleteView):
    model = MyPost

def postLike(request, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.create(post = post, liked_by = request.user.myprofile)
    return redirect('/fb/home')

def postUnlike(request, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.filter(post = post, liked_by = request.user.myprofile).delete()
    return redirect('/fb/home')

def postComment(request, pk):
    #Comment System
    post = MyPost.objects.get(pk=pk)
    comment = request.GET.get('comment')
    postComment = PostComment.objects.create(post=post, msg=comment, commented_by=request.user.myprofile)
   # print(postComment)
    postComment.save()
    return redirect('/fb/home')

def viewcomments(request, pk):
    comment = PostComment.objects.all()
    context = {'comment':comment}
    return render(request, '/fb/home.html', context)

#MyPost views ends here

#MyProfileView Starts here


@method_decorator(login_required, name='dispatch')
class MyProfileListView(ListView):
    model = MyProfile
    def get_queryset(self):
        si = self.request.GET.get('si')
        if si == None:
            si = ''
        profileList = MyProfile.objects.filter(Q(name__icontains=si) | Q(address__icontains=si) | Q(
            gender__icontains=si) | Q(status__icontains=si)).order_by('-id')
        for p in profileList:
            p.followed = False
            Follow = FollowUser.objects.filter(profile = p, followed_by = self.request.user.myprofile)
            if Follow:
                p.followed = True
        return profileList


@method_decorator(login_required, name='dispatch')
class MyProfileDetailView(DetailView):
    model = MyProfile

class MyProfileUpdateView(UpdateView):
    model = MyProfile
    fields = ['name', 'age', 'address', 'status', 'gender', 'phone', 'description', 'profile_pic']

def follow(request, pk):
    user = MyProfile.objects.get(pk=pk) #GET THE PROFILE AND PUT IT INTO PROFILE THAT HAS BEEN FOLLOWED
    FollowUser.objects.create(profile=user, followed_by=request.user.myprofile)
    return redirect('/fb/myprofile')

def unfollow(request, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by=request.user.myprofile).delete()
    return redirect('/fb/myprofile')
