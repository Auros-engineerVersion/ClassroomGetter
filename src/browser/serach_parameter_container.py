from dataclasses import dataclass

from src import my_util
from src.browser.browser_controls import BrowserControl
from src.interface.i_node import INode

@dataclass(frozen=True)
class SearchParameter:
    xpath: str
    regex: str
    filter_func: callable
        
    def next_values(self, acquiring_func: callable) -> list:
        return map(
            self.filter_func,
            acquiring_func(self.xpath, self.regex)(self.filter_func)
        )
        
@dataclass(frozen=True)
class SearchParameterPattern:
    pattern_name: str
    text_param: SearchParameter
    link_param: SearchParameter
    pre_proc: callable
    
    #func:textとlinkのペアに対して行う関数
    #text_filter, link_filter: それぞれのlistに対して行う関数
    def elements(self, node: INode) -> list[tuple[str, str]]:
        self.pre_proc(node)
        if self.text_param == None or self.link_param == None:
            return my_util.convert_to_tuple([node.key + '授業タブ'], [my_util.to_all_tab_link(node.url)])
        else:
            return list(
                map(
                    my_util.convert_to_tuple,
                    self.text_param.next_values(BrowserControl.elements),
                    self.link_param.next_values(BrowserControl.elements)
                )
            )
        
class SearchParameterContainer:
    get_text = lambda elem: elem.text
    get_link = lambda elem: elem.get_attribute('href')
    def __move_page_and_click(node: INode):
        BrowserControl.move(node.url)
        BrowserControl.click_all_sections()
    
    parameters: list[SearchParameterPattern] = [
        #添字とtree_heightを一致させる
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
            ),
            pre_proc=lambda node: BrowserControl.move(node.url)
        ),
        SearchParameterPattern(
            pattern_name='LessonTab',
            text_param=None,
            link_param=None,
            pre_proc=my_util.do_nothing
        ),
        SearchParameterPattern(
            pattern_name='Sections',
            text_param=SearchParameter(
                "//span[@class='YVvGBb UzbjTd']",
                ".+",
                get_text
            ),
            link_param=SearchParameter(
                "//a[contains(@aria-label, '資料を表示')]",
                ".*/details$",
                get_link
            ),
            pre_proc=__move_page_and_click
        ),
        SearchParameterPattern(
            pattern_name='Details',
            text_param=SearchParameter(
                "//div[@class='A6dC2c QDKOcc VBEdtc-Wvd9Cc zZN2Lb-Wvd9Cc']",
                ".+",
                get_text
            ),
            link_param=SearchParameter(
                "//a[@class='vwNuXe JkIgWb QRiHXd MymH0d maXJsd']",
                '.*/file/d.*',
                get_link
            ),
            pre_proc=lambda node: BrowserControl.move(node.url)
        )
    ]

    @staticmethod
    def elements(node: INode):
        #簡易化のため
        id: int = node.tree_height
        params = SearchParameterContainer.parameters
        if len(params) > id:
            return params[id].elements(node)
        else:
            return []