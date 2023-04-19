from dataclasses import dataclass

from src import my_util
from src.browser.browser_controls import BrowserControl

@dataclass(frozen=True)
class SearchParameter:
    def __init__(self, xpath: str, regex: str) -> None:
        self.xpath = xpath
        self.regex = regex
        
    def elements(self, filter: callable) -> list:
        def __search(func: callable):
            return map(
                    lambda arg: func(arg),
                    BrowserControl.elements(xpath=self.xpath, pattern=self.regex)(filter)
                )
            
        return __search
        
@dataclass(frozen=True)
class SearchParameterPattern:
    def __init__(self, pattern_name: str, filter_func: callable, text_param: SearchParameter, link_param: SearchParameter) -> None:
        self.pattern_name = pattern_name
        self.text_param   = text_param
        self.link_param   = link_param
        self.filter_func  = filter_func
        
    def elements(self):
        return map(
            lambda arg: self.filter_func(arg),
            self.text_param.elements(lambda elem: elem.text)
        )
        
class SearchParameterContainer:
    parameters: list = {
        SearchParameterPattern(
            pattern_name='Home',
            text_param=SearchParameter(
                "//div[@class='YVvGBb z3vRcc-ZoZQ1']",
                '.+'
            ),
            link_param=SearchParameter(
                "//a[@class='onkcGd ZmqAt Vx8Sxd']",
                "^.*/c/.{16}$"
            )
        ),
    }

    @staticmethod
    def current_params(id: int) -> SearchParameterPattern:
        if len(SearchParameterContainer.parameters) < id: #最大値を超えたら
            return
        else:
            return SearchParameterContainer.parameters[id]
        
    @staticmethod
    def validate_function(num: int):
        params = SearchParameterContainer.current_params(num)

SearchParameter.elements(print)