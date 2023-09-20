from dataclasses import dataclass
from typing import Callable

from ..browser import *
from ..interface import (IBrowserControlData as IBCD, INode)
from ..my_util import *


class SearchParameter:    
    def __init__(self, xpath, attribute_selector, sifter):
        self.__xpath = xpath
        self.__attribute_selector = attribute_selector
        self.__sifter = sifter
        
    def get_next_values(self, bc, get) -> list[WebElement]:
        """
        Args:
            get (callable): 値を取得する関数, 引数はxpath
            attribute (callable): WebElementから、aタブやtext等を取得するための関数
        """
        
        result = []
        @tail_recursion
        def loop(elems: Iterable[WebElement]):
            elem = elems.pop(0)
            nonlocal result
            
            self.__attribute_selector(elem)\
                |pipe| self.__sifter\
                |pipe| result.append

            if len(elems) == 0:
                return result
            else:
                return loop(elems)
                    
        return loop(get(bc, self.__xpath))
                    
class SearchParameterPattern:
    def __init__(self, key_param, url_param, elems_get_proc=search_element_all, pre_proc=identity) -> None:
        self.__key_param = key_param
        self.__url_param = url_param
        self.__elems_get_proc = elems_get_proc
        self.__pre_proc = pre_proc
    
    #func:textとlinkのペアに対して行う関数
    #text_filter, link_filter: それぞれのlistに対して行う関数
    def key_url_pair(self, ibc: INode, node: INode):
        """獲得したファイルの名前とurlを返す。返り値をNodeのコンストラクタに渡すことを想定している"""        
        #if self.key_param is None or self.url_param is None:
        #    return [*zip([node.key + 'の授業タブ'], [to_all_tab_link(node.url)])]
        #else:
        
        self.__pre_proc(node)
        return [*zip(
            self.__key_param.get_next_values(ibc, self.__elems_get_proc),
            self.__url_param.get_next_values(ibc, self.__elems_get_proc))]
        
class SearchParameterContainer:
    browser_control_data: IBCD = None

    @staticmethod
    def next_key_url(node: INode) -> list[tuple[str, str]]:
        """
            渡されたnodeのtree_heightを確認し、次のnodeのkeyとurlを返す。\n
            この関数ではwebへのアクセスが生じるため注意
        """
        #absを取ることで、負の値が入らないように
        return __parameters[abs(node.tree_height)].key_url_pair(SearchParameterContainer.browser_control_data, node)

def __get_text(elem: WebElement) -> str:
    return elem.text

def __get_url(elem: WebElement) -> str:
    return elem.get_attribute('href')

def __move(inode):
    move(SearchParameterContainer.browser_control_data, inode.url)

def __move_and_click(inode: INode):
    __move(SearchParameterContainer.browser_control_data, inode)
    click_all_sections(SearchParameterContainer.browser_control_data)

def __key_parameter(xpath, sifter=identity):
    return SearchParameter(xpath, __get_text, sifter)

def __url_parameter(xpath):
    return SearchParameter(xpath, __get_url, identity)

__parameters: list[SearchParameterPattern] = [
    #添字とtree_heightを一致させる
    #root -> 授業一覧
    SearchParameterPattern(
        pre_proc=identity,
        key_param=__key_parameter("//div[@class='YVvGBb z3vRcc-ZoZQ1']", sifter=text_filter),
        url_param=__url_parameter("//a[@class='onkcGd ZmqAt Vx8Sxd']")
    ),
    
    #授業一覧 -> 授業タブ
    SearchParameterPattern(
        key_param=__key_parameter("//a[contains(@guidedhelpid, 'classworkTab')]"),
        url_param=__url_parameter("//a[contains(@guidedhelpid, 'classworkTab')]")
    ),
    
    #授業タブ -> 授業タブのファイル一覧
    SearchParameterPattern(
        pre_proc=__move_and_click,
        key_param=__key_parameter("//span[@class='YVvGBb UzbjTd']"),
        url_param=__url_parameter("//a[contains(@aria-label, '表示')]")
    ),
    
    #ファイル一覧
    SearchParameterPattern(
        pre_proc=__move,
        key_param=__key_parameter("//div[@class='A6dC2c QDKOcc VBEdtc-Wvd9Cc zZN2Lb-Wvd9Cc']"),
        url_param=__url_parameter("//a[@class='vwNuXe JkIgWb QRiHXd MymH0d maXJsd']")
    )
]