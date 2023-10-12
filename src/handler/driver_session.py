from dataclasses import *
from typing import Callable
from pathlib import Path
from urllib.parse import *

from ..browser import *
from ..interface import (IBrowserControlData as IBCD, INodeProperty)
from ..my_util import *


@dataclass
class SearchParameter:
    xpath: str
    attribute_selector: Callable[[WebElement], str]
    sifter: Callable[[str], str]
    
    @classmethod
    def key_parameter(cls, xpath, sifter=identity):
        return cls(xpath, lambda e: e.text, sifter)
    
    @classmethod
    def url_parameter(cls, xpath):
        return cls(xpath, lambda e: e.get_attribute('href'), identity)
        
    def get_next_values(self, bc, get) -> list[WebElement]:
        """
        Args:
            get (callable): 値を取得する関数, 引数はxpath
            attribute (callable): WebElementから、aタブやtext等を取得するための関数
        """
        result = []
        def loop(elems: Iterable[WebElement]):
            nonlocal result
            if len(elems) == 0:
                return result
            else:
                elem = elems.pop(0)                
                self.attribute_selector(elem)\
                    |pipe| self.sifter\
                    |pipe| result.append
                return loop(elems)
                    
        return loop(get(bc, self.xpath))

@dataclass
class SearchParameterPattern:
    key_param: SearchParameter = field(default=None)
    url_param: SearchParameter = field(default=None)
    elems_get_proc: Callable[[IBCD, str], list[WebElement]] = field(default=search_element_all)
    pre_proc: Callable[[IBCD, INodeProperty], tuple[str, str]] = field(default=identity)
    
    #func:textとlinkのペアに対して行う関数
    #text_filter, link_filter: それぞれのlistに対して行う関数
    def key_url_pair(self, ibc: IBCD, node: INodeProperty) -> tuple[str, str] | Any:
        """獲得したファイルの名前とurlを返す。返り値をNodeのコンストラクタに渡すことを想定している"""
        if self.key_param is None or self.url_param is None:
            #listで包むのは、Nodeのコンストラクタに渡す前にfor ~ inで一度展開され、そののちにunpackされるため
            return [self.pre_proc(ibc, node)]
        else:
            self.pre_proc(ibc, node)
            return zip(
                self.key_param.get_next_values(ibc, self.elems_get_proc),
                self.url_param.get_next_values(ibc, self.elems_get_proc))
        
@dataclass
class DriverSession:
    bc: IBCD = None
    save_dir: Path = Path('./Save')

    def next_key_url(self, node: INodeProperty):
        """
            渡されたnodeのtree_heightを確認し、次のnodeのkeyとurlを返す。\n
            この関数ではwebへのアクセスが生じるため注意
        """
        #負の値が入らないように
        return parameters[max(0, node.tree_height)].key_url_pair(self.bc, node)

    def close(self):
        if self.bc is not None:
            del self.bc

def __move_and_click(bc: IBCD, url: str):
    move(bc, url)
    click_all_sections(bc)

def __url_parse(f: Callable[[ParseResult], Any]) -> Callable[[Callable[[str], Any]], Any]:
    def _inner(url: str) -> Any:
        parse = urlparse(url)
        return f(parse)
    return _inner

def __url_add(object_selector: Callable[[ParseResult], str], add: str) -> Callable[[Callable[[ParseResult], str]], str]:
    """
    Args:
        object_selector (Callable[[ParseResult], str]): ParseResultを受け取り、pathやqueryなど扱いたい部分を返す関数\n
        add (str): 追加したい文字列。文字列は末尾に追加される

    Returns:
        Callable: ParseResultを受け取る
    """
    def _inner(parse: ParseResult) -> str:
        return parse._replace(path=object_selector(parse) + add).geturl()
    return _inner

def __url_replace(object_selector: Callable[[ParseResult], str], old: str, new: str) -> Callable[[Callable[[ParseResult], str]], str]:
    """
    Args:
        object_selector (Callable[[ParseResult], str]): ParseResultを受け取り、pathやqueryなど扱いたい部分を返す関数\n
        replace (str): 置換したい文字列

    Returns:
        Callable: ParseResultを受け取る
    """
    def _inner(parse: ParseResult) -> str:
        return parse._replace(path=object_selector(parse).replace(old, new)).geturl()
    return _inner

def __url_to_drive(x: ParseResult | str) -> str:
    if isinstance(x, ParseResult):
        url = x.geturl()
    else:
        url = x
        
    file_id = url.split('/')[-2]
    return f'https://drive.google.com/u/1/uc?id={file_id}&export=download'

parameters: list[SearchParameterPattern] = [
    #添字とtree_heightを一致させる
    #root -> 授業一覧
    SearchParameterPattern(
        pre_proc=lambda bc, n: move(bc, n.url),
        key_param=SearchParameter.key_parameter("//div[@class='YVvGBb z3vRcc-ZoZQ1']"),
        url_param=SearchParameter.url_parameter("//a[@class='onkcGd ZmqAt Vx8Sxd']")),
    
    #授業一覧 -> 授業タブ -> 授業タブのファイル一覧
    SearchParameterPattern(
        #urlを授業タブのurlに整形する。そののち、それぞれの授業タブをクリックしてファイルのurlを読み込ませる
        pre_proc=lambda bc, n:
            __move_and_click(
                bc=bc,
                url=__url_parse(lambda parse:
                    __url_add(lambda x: x.path, '/t/all')(parse)
                        |pipe| __url_parse(identity) #次の関数への繋ぎ
                        |pipe| __url_replace(lambda x: x.path, old='/c/', new='/w/'))(n.url)),
        key_param=SearchParameter.key_parameter("//span[@class='YVvGBb UzbjTd']"),
        url_param=SearchParameter.url_parameter("//a[contains(@aria-label, '表示') and not(contains(@aria-label, '課題'))]")),
    
    #ファイルを取得
    SearchParameterPattern(
        pre_proc=lambda bc, n: move(bc, n.url),
        key_param=SearchParameter.key_parameter("//div[@class='A6dC2c QDKOcc VBEdtc-Wvd9Cc zZN2Lb-Wvd9Cc']"),
        url_param=SearchParameter.url_parameter("//a[@class='vwNuXe JkIgWb QRiHXd MymH0d maXJsd']")),
    
    #urlにアクセスし、ファイルを取得
    SearchParameterPattern(
        pre_proc=lambda bc, n:(None,
            __url_to_drive(n.url)
                |pipe| (lambda url: donwload(
                    bc=bc, 
                    url=url,
                    file_path=
                        DriverSession.save_dir.joinpath(n.to_path())
                            |pipe| (lambda p: None if p.exists() else p\
                                |arrow| (lambda p: p.parent.mkdir(parents=True, exist_ok=True)) #ダウンロード先のフォルダが存在しない場合は作成する
                                |arrow| (lambda p: bc.download_path_change(p)))))))
]