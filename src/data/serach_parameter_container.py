from typing import Callable
from dataclasses import dataclass
from selenium.common.exceptions import TimeoutException

from src import my_util
from src.interface.i_node import INode
from src.browser.browser_controls import *
from src.data.browser_control_data import BrowserControlData as bc_data

@dataclass(frozen=True)
class SearchParameter:
    xpath: str
    regex: str
    attribute_func: Callable
        
    def next_values(self, bc_data: bc_data) -> Callable:
        """
        この関数はカリー化されている
        Args:
            acquiring_func (callable):
                この関数は高階関数で無ければならず、最終的にIterableな値を返さなければならない
                
            format_func (callable):
                acquiring_funcの戻り値をこの関数でmapする
        """
        def __acc_func(acquiring_func: Callable) -> Callable:
            def __map(format_func: Callable) -> map:
                return map(
                    format_func,
                    acquiring_func(bc_data, self.xpath, self.regex)(self.attribute_func)
                ) 

            return __map
        return __acc_func
        
@dataclass(frozen=True)
class SearchParameterPattern:
    pattern_name: str
    text_param: SearchParameter
    link_param: SearchParameter
    
    text_filter: callable = my_util.do_nothing
    link_filter: callable = my_util.do_nothing
    pre_proc:    callable = my_util.do_nothing
    
    #func:textとlinkのペアに対して行う関数
    #text_filter, link_filter: それぞれのlistに対して行う関数
    def elements(self, bc_data: bc_data, node: INode) -> list[tuple[str, str]]:
        self.pre_proc((bc_data, node))
        if self.text_param == None or self.link_param == None:
            return my_util.convert_to_tuple([node.key + 'の授業タブ'], [my_util.to_all_tab_link(node.url)])
        else:
            try:
                return my_util.convert_to_tuple(
                        self.text_param.next_values(bc_data)(elements)(self.text_filter),
                        self.link_param.next_values(bc_data)(elements)(self.link_filter)
                    )
            except TimeoutException:
                return []
        
class SearchParameterContainer:
    browser_control_data: bc_data = None
    
    @staticmethod
    def __get_text(elem):
        return elem.text
    
    @staticmethod
    def __get_link(elem):
        return elem.get_attribute('href')

    @staticmethod
    def __move(bc_and_node):
        move(bc_and_node[0], bc_and_node[1].url)
        
    def __move_and_click(bc_and_node):
        SearchParameterContainer.__move(bc_and_node)
        click_all_sections(bc_and_node[0])

    parameters: list[SearchParameterPattern] = [
        #添字とtree_heightを一致させる
        SearchParameterPattern(
            pattern_name='Home',
            text_param=SearchParameter(
                "//div[@class='YVvGBb z3vRcc-ZoZQ1']",
                '.+',
                __get_text
            ),
            link_param=SearchParameter(
                "//a[@class='onkcGd ZmqAt Vx8Sxd']",
                "^.*/c/.{16}$",
                __get_link
            ),
            text_filter = my_util.text_filter,
            pre_proc=__move
        ),
        
        SearchParameterPattern(
            pattern_name='LessonTab',
            text_param=None,
            link_param=None
        ),
        
        SearchParameterPattern(
            pattern_name='Sections',
            text_param=SearchParameter(
                "//span[@class='YVvGBb UzbjTd']",
                ".+",
                __get_text
            ),
            link_param=SearchParameter(
                "//a[contains(@aria-label, '表示')]",
                ".*/details$",
                __get_link
            ),
            pre_proc=__move_and_click
        ),
        
        SearchParameterPattern(
            pattern_name='Details',
            text_param=SearchParameter(
                "//div[@class='A6dC2c QDKOcc VBEdtc-Wvd9Cc zZN2Lb-Wvd9Cc']",
                ".+",
                __get_text
            ),
            link_param=SearchParameter(
                "//a[@class='vwNuXe JkIgWb QRiHXd MymH0d maXJsd']",
                '.*/file/d.*',
                __get_link
            ),
            pre_proc=__move
        )
    ]

    @staticmethod
    def elements(node: INode):
        if len(SearchParameterContainer.parameters) > node.tree_height:
            return SearchParameterContainer.parameters[node.tree_height].elements(SearchParameterContainer.browser_control_data, node)
        else:
            return []