if __name__=='__main__':
    import os, sys
    from os.path import dirname, abspath, join
    d1 = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(d1)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thedata.settings.local")

import pysolr
from  pysolr import Results as PySolrResults

from django.conf import settings

from thedata.utils.msg_util import *

from apps.search.solr_search_formatter import SolrSearchFormatter
from apps.search.solr_results_handler import SolrResultsHandler


class SolrSearcher:
    
    def __init__(self, solr_server_url=None, solr_server_timeout=10):
        if solr_server_url is None:
            solr_server_url = settings.SOLR_SERVER_URL
        if solr_server_timeout is None:
            solr_server_timeout = settings.SOLR_SERVER_TIMEOUT_SECONDS

        # initialize connection to solr
        self.solr_object = pysolr.Solr(solr_server_url, timeout=solr_server_timeout)

        # object to process solr results
        self.searchFormatter = SolrSearchFormatter(**dict(num_rows=10))
        
        # err flags
        self.err_found = False
        self.err_msg = None
        
    def reset_errs(self):
        self.err_found = False
        self.err_msg = None
        
    def add_err(self, err_msg):
        msgt(err_msg)
        self.err_found = True
        self.err_msg = err_msg
        
    def conduct_search(self, qstr, solr_kwargs=None):
        msg('type: %s' % type(qstr))
        if not type(qstr) in  (unicode, str):
            raise TypeError('qstr is not type "unicode" or "str", intead is "%s"' % type(qstr))
        msg('type solr_kwargs: %s' % type(solr_kwargs))

        if not solr_kwargs in (dict, None):
            raise TypeError('kwargs is not type "dict"')
            
        self.reset_errs()
        
        if solr_kwargs is None:
            solr_kwargs = self.searchFormatter.get_solr_kwargs()

        results = None
        #msgt(qstr)
        try:
            results = self.solr_object.search(qstr, **solr_kwargs)
        except pysolr.SolrError as e:
            self.add_err('SOLR ERROR:\n%s' % str(e))    #'solr connection error')
            return

        if type(results) is not PySolrResults:
           raise TypeError()        
           add_err('Expected pysolr.Results object.  Received type: "%s"' % type(results))
           return

        solr_results = SolrResultsHandler(results)
        return solr_results

if __name__=='__main__':
    ss = SolrSearcher()
    ss.conduct_search('Stephen King')
