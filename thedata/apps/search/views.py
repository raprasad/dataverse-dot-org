from __future__ import print_function

from datetime import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext

from django.db.models import Q

from thedata.utils.msg_util import *

from apps.search.forms import BasicSearchForm
from apps.search.solr_searcher import SolrSearcher

def view_basic_search(request):

    d = {}
    if request.POST:
        search_form = BasicSearchForm(request.POST)
        if search_form.is_valid():
            ss = SolrSearcher()
            search_results = ss.conduct_search(search_form.cleaned_data['search_term'])
            d['search_results'] = search_results
            d['search_term'] = search_form.cleaned_data['search_term']
            search_form = BasicSearchForm({ 'search_term' : search_form.cleaned_data['search_term'] })
            #search_form = BasicSearchForm()
    else:
        search_form = BasicSearchForm()

    d['search_form'] = search_form
        
    return render_to_response('search/view_basic_search.html'\
                              , d\
                              , context_instance=RequestContext(request))

    