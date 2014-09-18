

class Pager:
    
    def __init__(self, num_hits, items_per_page=10, current_page=1):

        self.show_pager = False
        self.num_hits = num_hits
        self.items_per_page = items_per_page
        self.current_page = current_page
        
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
            
        if self.current_page > self.num_pages:
            self.current_page = 1
        
        # first last 
        if self.current_page > 1:
            self.first_page = 1
            self.previous_page = self.current_page - 1
        
        if self.current_page < self.num_pages:
            self.last_page = self.num_pages
            self.next_page = self.current_page + 1
        
        # page menu numbers to display
        page_button_count = min(self.num_pages, self.num_page_buttons)
        mid_button = (page_button_count / 2) 
        if (page_button_count % 2) > 0:
            mid_button += 1
        """
        print ('mid_button', mid_button)
        
        # e.g., if display is 5 buttons, this would be page 1 or page 2
        if self.current_page < mid_button:
            self.page_menu_range = range(1, mid_button) + range(mid_button, page_button_count+1)    
        else:
            num_left_right = page_button_count / 2
            print ('num_left_right', num_left_right)
            self.page_menu_range = range(self.current_page - num_left_right, self.current_page)
            self.page_menu_range += range(self.current_page, self.current_page + (num_left_right-1))

            if self.num_page_buttons % 2 > 0:
               self.page_menu_range.append(self.current_page + (num_left_right-1))
        """
        self.pager_calculated = True

if __name__=='__main__':
    p = Pager(num_hits=26, items_per_page=5, current_page=4)
    print (p.num_pages)
    print (p.page_menu_range)
    