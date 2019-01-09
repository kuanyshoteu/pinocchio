# generic

from django.db.models import Q
from rest_framework import generics, mixins
 
from squads.models import Squad
from .permissions import IsOwnerOrReadOnly
from .serializers import SquadSerializer


class SquadAPIView(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = SquadSerializer
    #queryset                = Squad.objects.all()

    def get_queryset(self):
        qs = Squad.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                    Q(title__icontains=query)|
                    Q(content__icontains=query)
                    ).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class SquadRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = SquadSerializer
    permission_classes      = [IsOwnerOrReadOnly]
    #queryset                = Squad.objects.all()

    def get_queryset(self):
        return Squad.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return Squad.objects.get(pk=pk)


