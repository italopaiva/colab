#!/usr/bin/env python
# encoding: utf-8
"""
other.py

Created by Sergio Campos on 2012-01-10.
"""

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _

from colab import solrutils
from colab.super_archives import queries


def home(request):
    """Index page view"""

    latest_threads = queries.get_latest_threads()
    hottest_threads = queries.get_hottest_threads()

    template_data = {
        'hottest_threads': hottest_threads[:6],
        'latest_threads': latest_threads[:6],
        'type_count': solrutils.count_types(sample=1000),
        'latest_docs': solrutils.get_latest_collaborations(6),
    }
    return render_to_response('home.html', template_data,
                              context_instance=RequestContext(request))


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        sort = request.GET.get('o')
        type_ = request.GET.get('type')
        page_number = int(request.GET.get('p', 1))
        results_per_page = int(request.GET.get('per_page', 16))

    filters = {
        'Type': type_,
    }

    query = solrutils.build_query(query, filters)

    # Query Solr for results
    solr_dict_resp = solrutils.select(query, results_per_page,
                                      page_number, sort)

    docs = solrutils.SolrPaginator(solr_dict_resp, page_number)

    template_data = {
        'docs': docs,
        'anonymous': _(u'anônimo'),
        'q': query,
        'type': type_,
    }

    return render_to_response('search.html', template_data,
                              RequestContext(request))