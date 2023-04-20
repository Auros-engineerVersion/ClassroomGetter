from dataclasses import dataclass

from src import my_util
from src.browser.browser_controls import BrowserControl

@dataclass(frozen=True)
class SearchParameter:
    def __init__(self, xpath: str, regex: str, filter_func: callable) -> None:
        self.xpath = xpath
        self.regex = regex
        self.filter_func = filter_func
        
    def elements(self, func) -> list:
        return map(
            func,
            BrowserControl.elements(xpath=self.xpath, pattern=self.regex)(self.filter_func)
        )
        
@dataclass(frozen=True)
class SearchParameterPattern:
    def __init__(self, pattern_name: str, text_param: SearchParameter, link_param: SearchParameter) -> None:
        self.pattern_name = pattern_name
        self.text_param   = text_param
        self.link_param   = link_param
        
    #func:textとlinkのペアに対して行う関数
    #text_filter, link_filter: それぞれのlistに対して行う関数
    def elements(self, func: callable):
        def __do(text_filter: callable, link_filter: callable):
            return map(
                func,
                self.text_param.elements(text_filter),
                self.link_param.elements(link_filter)
            )
        return __do
        
class SearchParameterContainer:
    get_text = lambda elem: elem.text
    get_link = lambda elem: elem.get_attribute('href')
    
    parameters: list = {
        SearchParameterPattern(
            pattern_name='Home',
            text_param=SearchParameter(
                "//div[@class='YVvGBb z3vRcc-ZoZQ1']",
                '.+',
                get_text
            ),
            link_param=SearchParameter(
                "//a[@class='onkcGd ZmqAt Vx8Sxd']",
                "^.*/c/.{16}$",
                get_link
            )
        ),
    }

    @staticmethod
    def current_params(id: int) -> SearchParameterPattern:
        if len(SearchParameterContainer.parameters) > id: #最大値を超えたら
            return SearchParameterContainer.parameters[id]

SearchParameter.elements(print)