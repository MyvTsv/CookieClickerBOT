class CookieUpgrade:
    
    def __init__(self, id, name, cps = 0):
        self._id = id
        self._name = name
        self._cost = 0
        self._cps = cps
        self._level = 0
    
    def set_cost(self, cost):
        self._cost = cost
    
    def get_cost(self):
        return self._cost
    
    def set_cps(self, cps):
        self._cps = cps
        
    def get_cps(self):
        return self._cps

    def set_level(self, level):
        self._level = level
    
    def get_level(self):
        return self._level

    def __str__(self):
        return f"Upgrade: {self._name} | Cost: {self._cost} | CPS: {self._cps} | Level: {self._level}"
