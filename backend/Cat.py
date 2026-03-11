class Cat():
    def __init__(self, limit=1, page=0, order="ASC", has_breeds=0, breed_ids=None, category_ids=None, sub_id=None):
        self.limit = limit
        self.page = page
        self.order = order
        self.has_breeds = has_breeds
        self.breed_ids = breed_ids
        self.category_ids = category_ids
        self.sub_id = sub_id