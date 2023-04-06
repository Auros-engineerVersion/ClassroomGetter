from urllib.parse import urljoin

class FNode:
    def __init__(self, year, name, num) -> None:
        self.year = year
        self.name = name
        self.num = num
        pass
    
    def path(self) -> str:
        temp = urljoin(self.year, self.name)
        result = urljoin(temp, self.num)
        return result