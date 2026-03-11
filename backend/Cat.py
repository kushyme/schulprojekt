class Cat():
    def __init__(self, limit: int=1, page: int=0, order: str="ASC", has_breeds: int=0, breed_ids: str=None, category_ids: int=None, sub_id: str=None):
        self.limit = limit
        self.page = page
        self.order = order
        self.has_breeds = has_breeds
        self.breed_ids = breed_ids
        self.category_ids = category_ids
        self.sub_id = sub_id
        self.id = None
        self.width = None
        self.height = None
        self.url = None
        self.breeds = [{
            self.weight: { self.imperial: str, self.metric: str },
            self.id: str,
            self.temperament: str,
            self.origin: str,
            self.country_codes: str,
            self.country_code: str,
            self.life_span: str,
            self.wikipedia_url: str
        }]
