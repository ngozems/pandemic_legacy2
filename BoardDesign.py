class Map:
    def __init__(self):
        self.NewYork = Location("New York", "city")
        self.Washington = Location("Washington", "city")
        self.Jacksonville = Location("Jacksonville", "city")
        self.Sao_Paulo = Location("Sao_Paulo", "city")
        self.London = Location("London", "city")
        self.Cairo = Location("Cairo", "city")
        self.Lagos = Location("Lagos", "city")
        self.Tripoli = Location("Tripoli", "city")
        self.Istanbul = Location("Istanbul", "city")
        self.New_Urk = Location("New_Urk", "haven")
        self.Matrix = Location("Matrix", "haven")
        self.Elysium = Location("Elysium", "haven")

        self.NewYork.create_paths([self.Washington, self.Jacksonville, self.New_Urk])
        self.Washington.create_paths([self.Jacksonville, self.NewYork])
        self.Jacksonville.create_paths([self.Washington, self.Elysium])
        self.Sao_Paulo.create_paths([self.Elysium, self.Lagos])
        self.London.create_paths([self.New_Urk])
        self.Cairo.create_paths([self.Tripoli, self.Matrix])
        self.Lagos.create_paths([self.Sao_Paulo, self.Elysium])
        self.Tripoli.create_paths([self.Cairo, self.Matrix])
        self.Istanbul.create_paths([self.Cairo, self.Matrix])
        self.New_Urk.create_paths([self.Londen, self.NewYork, self.Matrix, self.Elysium])
        self.Matrix.create_paths([self.New_Urk, self.Cairo, self.Tripoli, self.Istanbul])
        self.Elysium.create_paths([self.Sao_Paulo, self.Lagos, self.New_Urk, self.Jacksonville, self.Matrix])

        self.city_list = [self.NewYork,
                          self.Washington,
                          self.Sao_Paulo,
                          self.Lagos,
                          self.London,
                          self.Cairo,
                          self.Tripoli,
                          self.Istanbul]

class Location:
    def __init__(self, name, location_type):
        self.name = name
        self.paths = []
        self.location_type = location_type
        self.supplies = 0
        self.plagues = 0

    def create_paths(self, path_list):
        self.paths = path_list
