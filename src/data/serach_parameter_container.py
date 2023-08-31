from typing import Callable
from dataclasses import dataclass
from selenium.common.exceptions import TimeoutException

from interface import *
from src.my_util import *
from src.browser.browser_controls import *

@dataclass(frozen=True)
class SearchParameter:
    xpath: str
    regex: str
    attribute_func: Callable
        
    def next_values(self, bc_data: IBrowserControlData) -> Callable[[Callable], Callable]:
        """
        この関数はカリー化されている
        Args:
            format_func (callable):
                acquiring_funcの戻り値をこの関数でmapする
                
            acquiring_func (callable):
                この関数は高階関数で無ければならず、最終的にIterableな値を返さなければならない
                
            filter_func (callable):
                acquiring_funcの戻り値をこの関数でfilterする
        """
        def __filter_func(format_func: Callable) -> Callable[[Callable], Callable]:
            def __acquiring_func(acquiring_func: Callable) -> Callable[[Callable], map]:
                def __map(filter_func: Callable) -> map:
                    return map(
                        format_func,
                        filter_func(acquiring_func(bc_data, self.xpath, self.regex)(self.attribute_func))
                    ) 
                return __map
            return __acquiring_func
        return __filter_func
        
@dataclass(frozen=True)
class SearchParameterPattern:
    pattern_name: str
    text_param: SearchParameter
    link_param: SearchParameter
    
    text_format: Callable = do_nothing
    link_format: Callable = do_nothing
    pre_proc:    Callable = do_nothing
    
    #func:textとlinkのペアに対して行う関数
    #text_filter, link_filter: それぞれのlistに対して行う関数
    def name_elements_pair(self, bc_data: IBrowserControlData, node: INode):
        def __functions(acc_f: Callable, filter_f: Callable):
            self.pre_proc((bc_data, node))
            if self.text_param == None or self.link_param == None:
                return convert_to_tuple([node.key + 'の授業タブ'], [to_all_tab_link(node.url)])
            else:
                return convert_to_tuple(
                        self.text_param.next_values(bc_data)(self.text_format)(acc_f)(filter_f),
                        self.link_param.next_values(bc_data)(self.link_format)(acc_f)(filter_f)
                    )
        return __functions
        
class SearchParameterContainer:
    browser_control_data: IBrowserControlData = None
    
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
            text_format = text_filter,
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
        param = SearchParameterContainer.parameters
        if len(param) > node.tree_height:
            return param[node.tree_height].\
                name_elements_pair(
                    SearchParameterContainer.browser_control_data,
                    node
                )(search_element_all, elements_filter)
        else:
            return []