from django.db.models import Count
from django.db.models.functions import ExtractYear
import plotly
import plotly.graph_objs as go
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
        '''Popualte drop down with queryset'''
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

class GraphListView(VoterListView):
    '''Show all fields for one graph'''
    template_name = 'voter_analytics/graphs.html'
    paginate_by = None
    def get_context_data(self, **kwargs):
        '''Load our graphs'''
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset() 

        # 1) Bar chart: voters by year of birth
        by_year = (voters.annotate(year=ExtractYear('dob'))
                        .values('year')
                        .annotate(n=Count('id'))
                        .order_by('year'))
        x = [row['year'] for row in by_year]
        y = [row['n'] for row in by_year]
        fig = go.Bar(x=x, y=y)
        context['graph_div_birth'] = plotly.offline.plot(
            {"data": [fig],
            "layout_title_text": f"Voter distribution by Year of Birth (n={voters.count()})"},
            auto_open=False, output_type="div")

        # 2) Pie chart: voters by party
        by_party = voters.values('party').annotate(n=Count('id')).order_by('-n')
        labels = [row['party'] for row in by_party]
        values = [row['n'] for row in by_party]
        fig = go.Pie(labels=labels, values=values)
        context['graph_div_party'] = plotly.offline.plot(
            {"data": [fig],
            "layout_title_text": "Voter distribution by Party Affiliation"},
            auto_open=False, output_type="div")

        # 3) Bar chart: how many voted in each election
        x = ELECTIONS
        y = [voters.filter(**{e: True}).count() for e in ELECTIONS]
        fig = go.Bar(x=x, y=y)
        context['graph_div_elections'] = plotly.offline.plot(
            {"data": [fig],
            "layout_title_text": "Vote Count by Election"},
            auto_open=False, output_type="div")

        return context




