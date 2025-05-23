class BaseService:
    def __init__(self, repository):
        self.repository = repository

    def get(self, id: int):
        return self.repository.get(id)

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_multi(skip=skip, limit=limit)

    def create(self, obj_in):
        return self.repository.create(obj_in)

    def update(self, id: int, obj_in):
        db_obj = self.get(id)
        if not db_obj:
            return None
        return self.repository.update(db_obj, obj_in)

    def delete(self, id: int):
        return self.repository.remove(id)
