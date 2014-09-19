

class DisplayPager:
    
    def __init__(self, num_hits, items_per_page=10, result_start_offset=0):
        assert(items_per_page >= 1)
        assert(result_start_offset >= 0)
        
        self.show_pager = False     # No need to show the page if only 1 page is available

        # Numbers to start with
        self.num_hits = num_hits
        self.items_per_page = items_per_page
        self.result_start_offset = result_start_offset
        
        self.current_page = 1#self.get_current_page()
        # figure out current page from result_start_offset
        
        
        self.num_page_buttons = 5
        
        # to calculate
        self.num_pages = 0

        self.first_page = None
        self.previous_page = None
        
        self.next_page = None
        self.last_page = None

        self.page_menu_range = None
        
        self.pager_calculated = False
        
        self.calculate_pager_items()
    
    def em_current_page(self, page_num):
        assert(type(page_num) is int)
        
        if self.current_page == page_num:
            return '<b>%s</b>' % page_num
        
        return page_num
        
    def show(self):
        
        page_menu = [self.em_current_page(x) for x in self.page_menu_range]
        
        test_str = """
------------
page settings
------------
current page: %s

num pages: %s 

menu: %s

first|prev|next|last: %s | %s | %s | %s
------------

""" % (self.current_page\
    , self.num_pages\
    , page_menu
    , self.first_page
    , self.previous_page
    , self.next_page
    , self.last_page
    )
        print(test_str)
        
    def get_current_page(self):
        # start on page 1
        if self.result_start_offset == 0:    
            return 1
        
        # only enough results for 1 page
        if self.num_hits <= self.items_per_page:
            return 1

        # calculate page number based on offset
        current_page_num = self.result_start_offset / self.items_per_page
        if (self.result_start_offset % self.items_per_page) > 1:
               current_page_num += 1 
        return current_page_num
        
    def get_solr_offset(self):
        """
        if items_per_page == 10:
            page 1 offset: 0
            page 2 offset: 10
            page 3 offset: 20
        """
        if self.pager_calculated is False:
            self.calculate_pager_items()
            
        return (self.current_page - 1) * (self.items_per_page)
    
    def calculate_pager_items(self):
        if self.num_hits >= 0 and self.num_hits <= self.items_per_page:
            # no need for a pager
            return 
            
        self.num_pages = (self.num_hits / self.items_per_page) 
        if ( self.num_hits % self.items_per_page) > 0:
            self.num_pages += 1
        
        self.current_page = self.get_current_page()
        
        # set first_page, previous_page, next_page, last_page
        #
        if self.current_page > 1:
            self.first_page = 1
            self.previous_page = self.current_page - 1
        
        if self.current_page < self.num_pages:
            self.last_page = self.num_pages
            self.next_page = self.current_page + 1
        
        # list of page menu numbers to display
        #
        odd_pages = False
        if (self.num_page_buttons % 2) > 0:
            odd_pages = True

        # how many page buttons do we need
        page_button_count = min(self.num_pages, self.num_page_buttons)
        
        # calculate the mid_button
        if odd_pages: 
            mid_button = (page_button_count / 2) + 1    # 1, 2, 3, 4, 5 -> "mid page is 3"
            num_left = page_button_count / 2
            num_right = num_left
        else: 
            mid_button = (page_button_count / 2)    # 1, 2, 3, 4 -> "mid page is 2"
            num_left = (page_button_count / 2) - 1
            num_right = page_button_count / 2 
        
        # calculate the page range
        if False:#self.current_page < mid_button:
            self.page_menu_range =  [999]
            pass # for now
            #self.page_menu_range = range(1, mid_button) + range(mid_button, page_button_count+1)    
        else:# odd_pages:
            leftmost_page = self.current_page - num_left
            rightmost_page = self.current_page + num_right
            self.page_menu_range = range(leftmost_page, self.current_page) \
                            + [self.current_page]\
                            + range(self.current_page+1, rightmost_page + 1)
            

        self.pager_calculated = True

if __name__=='__main__':
    p = DisplayPager(num_hits=26, items_per_page=5, result_start_offset=21)
    p.show()
    #print (p.num_pages)
    #print (p.page_menu_range)
    