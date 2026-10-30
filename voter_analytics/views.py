from django.db.models import Min, Max
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
'''
Name : Tim Nguyen
Email : tim7@bu.edu
Description : Show Voter data view
'''

ELECTIONS = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

class VoterListView(ListView):
    '''View to display voter results'''
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = "voters"
    paginate_by = 100
    def get_queryset(self):
        qs = super().get_queryset().order_by('last_name', 'first_name')
        g = self.request.GET
        #populate our list of options
        if g.get('party'):
            qs = qs.filter(party=g['party'])
        if g.get('min_dob'):
            qs = qs.filter(dob__year__gte=int(g['min_dob']))
        if g.get('max_dob'):
            qs = qs.filter(dob__year__lte=int(g['max_dob']))
        if g.get('voter_score'):
            qs = qs.filter(voter_score=int(g['voter_score']))
        for e in ELECTIONS:
            if g.get(e):
                qs = qs.filter(**{e: True})
        return qs
    def get_context_data(self, **kwargs):
        #get context data of selections
        context = super().get_context_data(**kwargs)

        # Dropdown choices
        context['parties'] = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
        r = Voter.objects.aggregate(lo=Min('dob'), hi=Max('dob'))
        context['years'] = [str(y) for y in range(r['lo'].year, r['hi'].year + 1)]
        context['scores'] = [str(s) for s in range(6)]

        # keep filters in the Next/Previous links
        q = self.request.GET.copy()
        q.pop('page', None)
        context['query_string'] = q.urlencode()
        return context

class VoterDetailView(DetailView):
    '''Show all fields for one voter'''
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'



