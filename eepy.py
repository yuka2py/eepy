#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
eepy 0.3.6 - Python コード埋め込み形のシンプルなテンプレートエンジンです。

Author:
    yuka2py

Lisence:
    Artistic License 2.0

Description:

    NOTATION:
        "<%" と "%>" で囲まれた範囲に、Python コードを埋め込むことができます。
        
                <% a = 10 %>
        
        *** 以下、"<%" と "%>" で囲まれた Python コードの範囲を「コードパート」と表記します ***

        ----
        "<%" 自体を文字列として表したい時には、"<%%" と記述してエスケープします。
        
                <div> <%% </div>    --->    <div> <% </div>
        
        ----
        "<%= expression %>" と書くと、このコードパートは expression の結果に置換されます。
        filter が指定されている場合、expression の結果は全て filter を経由して出力されます。
        filter を適用したくない任意の箇所では、<%=r と書くことで、filter 処理をスキップ出来ます。

            # filter = cgi.escape
            <% hoge = "<b>" -%>
            <%= hoge %>          --->        &lt;b&gt;
            <%=r hoge %>         --->        <b>
        
        ----
        "<%-" と "-%>" と書くと、トリムモードになります。
        "<%-" は、行頭から "<%-" までの空白（\s）を削除します。
        "-%>" は、"-%>" から行末までの空白（\s）と改行（\n）を削除します。

        ----
        コードパートでの if, elif, else, try, except などの使用で、ブロックが開始されます。
        また、複数のコードパートに分かれる、単一のブロックコンテキスト（if ～ elif ～ else の組など）は、
        "end" で終端を明示する必要があります。 

            <%- for i in xrange(10): -%>
                <%- if i % 2: -%>
                    odd<br />
                <%- else: -%>
                    even<br />
                <%- end -%>
            <%- end -%>
        
        上の例示ではインデントを行っていますが、ブロックの終端は、"end" によって明示される為、
        この時、実際にはインデントは必要ありません（Pythonista は「え～！」と非難の声を上げるかも知れませんが）。
        よって、この例示は、次のように書き換えることが出来ます。
        
            <%- for i in xrange(10): -%>
            <%- if i % 2: -%>odd<br />
            <%- else: -%>even<br />
            <%- end -%>
            <%- end -%>
        
        必要であれば、全てを１行に書くこともできます。
        この事により、Python のインデントブロックに制限されることなく、
        テンプレートの可読性を優先してテンプレート記述することが出来ます。
        また、テンプレートの可読性を高めるために "end" は次の様なバリエーションを許容します。
        
            <%- end if -%>
            <%- end for -%>
            <%- end with #comment... -%>
        
        また、次のように、インラインブロックも記述できます。

            <%- if age < 20: notice=u"No smoking!" -%>
        
        それから、単一のコードパート内にブロックを記述する時、end は必要としません。
        次のように、通常の Python インデントによるブロックを利用できます。
        
            <%-
                for i in xrange(10):
                    if i % 2:
                        concat("odd<br />")
                    else:
                        concat("even<br />")
            -%>
        
            *** 但し、このように単一のコードパートに複数行記述する場合、開始行（= "<%-" の行）にはコードを記述できません ***

        *** 制限（複数行コードパートと単一のインデントブロック） ***
        複数行のコードパートを用いる場合、単一のブロックコンテキスト（if ～ elif ～ else の組など）は、
        ひとつのコードパート内に全て記述する必要があります。
        例えば以下の例はいずれも正しく動作しません。
        
        ex.1:
            複数行のコードパートに記述された for や if のブロックコンテキストが、
            他のコードパートに分割されているので NG
        
                <%-
                    for i in xrange(10):
                        if i % 2:
                            -%>odd<br /><%-
                        else:
                            -%>even<br /><%-
                -%>
            
            正しく書き直すと、

                <%- for i in xrange(10): -%>
                        <%- if i % 2: -%>odd<br />
                        <%- else: -%>even<br />
                        <%- end if -%>
                <%- end for -%>

        ex.2:
            else が複数行のコードパートに書かれているにも関わらず、
            対となる if が別のコードパートに分割しているので NG
            
                <%- if age < 20: -%>
                    <b>No smoking!</b>
                <%-
                    else:
                        concat(renderer.render("smoking_area.html"))
                -%>
            
            正しく書き直すと、

                <%- if age < 20: -%>
                    <b>No smoking!</b>
                <%- else: -%>
                    <%- concat(renderer.render("smoking_area.html")) -%>
                <%- end if -%>
            
            または、

                <%- if age < 20: -%>
                    <b>No smoking!</b>
                <%- else: concat(renderer.render("smoking_area.html")) -%>
            
                *** インラインブロックで記述すると、ブロックが継続しないのが自明な為、"end" は不要です ***
            

    --------------------------------
    RENDERING:

        Template クラス:
            Template クラスを用いて、次のようにレンダリングできます。
            詳細はクラスおよびメソッドの __doc__ を参照ください。
             
                template = codecs.open("template.html", encoding="utf8")
                t = Template(template)
                result = t.render({"varname":value, ...}, filter=cgi.escape)

        Renderer クラス:
            Renderer を使用すると、より便利に処理できます。
            特にキャッシュが利用できる価値が大きいです。
            詳細はクラスおよびメソッドの __doc__ を参照ください。
            
                r = Renderer(
                                base = "/application/templates", 
                                cache = eepy.cache.FileCacheStorage(), 
                                filter = eepy.helper.escape_xml, 
                                encoding = "utf8")
                result = r.render("template.html", vars)


    --------------------------------
    ABOUT A CHARACTER CODE:
    
        eepy は、全て unicode で処理しています。
        テンプレートを文字列で提供する時は unicode 文字列としてください。
        テンプレートをファイルで提供する時はファイル適切なエンコーディングを指定してください。
        
            t = Template(codecs.open("template.html", encoding="utf8"))
            result = t.render()
            
            r = renderer(encoding="utf8")
            result = r.render("template.html")
        
        テンプレート変数の文字列は、unicode にしてください。
        例えば、入力データが str (utf-8) の場合、unicode へ decode してから eepy にデータを渡します。
        
            vars = {"title": "ほげ".decode("utf-8")}
            result = r.render("template.html", vars)
        
        テンプレート内の Python コードパートに記載する文字列は、
        全て unicode の記法としてください。
        
            <%- title=u"ほげほげ物語" -%>
        
        レンダリング結果も unicode で返ります。
        utf-8 の出力結果を得たい時は、例えば次のように encode できます。
        
            result = r.render("template.html", vars).encode("utf-8")
        
        なお、もし文字コードについて（なるべく）混乱したくない時は、
        テンプレートやテンプレート変数などの文字コードを、
        全て default encoding と一致させることをお勧めします。

    --------------------------------
    Example 1:
    
        template.html (utf8):
        
            <%-
                fmt = u" %%%dd" % len(str(max**2))
                def format(n):
                    return fmt % n
            -%>
            <%=r u"< %s >" % title %>
            <%- for y in range(1, max+1): -%>
            <%- for x in range(1, max+1): -%>
            <%= format(x * y) -%>
            <%- end %>
            <%- end -%>

        code:
        
            import eepy
            vars = {
                "title": u"The times table"
                "max": 9,
            }
            file = codecs.open("template.html", encoding="utf8")
            t = eepy.Template(file)
            print t.render(vars, filter=eepy.helper.escape_xml)
        
        output:
        
            < The times table >
              1  2  3  4  5  6  7  8  9
              2  4  6  8 10 12 14 16 18
              3  6  9 12 15 18 21 24 27
              4  8 12 16 20 24 28 32 36
              5 10 15 20 25 30 35 40 45
              6 12 18 24 30 36 42 48 54
              7 14 21 28 35 42 49 56 63
              8 16 24 32 40 48 56 64 72
              9 18 27 36 45 54 63 72 81

    --------------------------------
    Example 2: (Using Renderer, extends, block and include)
    
        templates/index.html (utf8):
       
            <%- extends("layout.html", title="Using Extends, Block and Include") -%>
            <%- with block("body"): -%>
                <table>
                    <thead>
                        <%- include("row.html", name="NAME", value="VALUE") -%>
                    </thead>
                    <tbody>
                    <%- for name, value in data.items(): -%>
                        <%- include("row.html") -%>
                    <%- end for-%>
                    </tbody>
                </table>
            <%- end with -%>

        templates/partial.html:

                        <tr>
                            <th><%= name %></th>
                            <td><%= value %></td>
                        </tr>

        templates/layout.html:

            <html>
            <head>
                <title><%= title %></title>
            </head>
            <body>
                <%- with block("body"): pass -%>
            </body>
            <html>
        
        code:
         
            import eepy
            r = eepy.Renderer(
                        base = "./templates",
                        cache = eepy.cache.FileCacheStorage(),
                        vars = eepy.helper.__dict__,
                        filter = eepy.helper.escape_xml,
                        encoding = "utf8")
             print r.render("index.html", {"data": {"name": "yuka2py", "age": 36}})

        output:
        
            <html>
            <head>
                <title>Extends, Block and Include</title>
            </head>
            <body>
                <table>
                    <thead>
                        <tr>
                            <th>NAME</th>
                            <td>VALUE</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th>age</th>
                            <td>36</td>
                        </tr>
                        <tr>
                            <th>name</th>
                            <td>yuka2py</td>
                        </tr>
                    </tbody>
                </table>
            </body>
            <html>

"""
from __future__ import with_statement
import sys, re, types, os.path, codecs, traceback


logger = None
""" ログを残したい場合、logging または logging 互換のオブジェクトを指定します。"""


def _module(func):
    """ 関数定義をモジュールに変換するデコレータ。
    関数内での定義が、モジュールのコンテンツになります。
    関数内の最後で、return locals() を書いてください。
    """
    modname = "%s.%s" % (
         sys._getframe(1).f_locals["__name__"], 
         func.__name__)
    mod = types.ModuleType(modname)
    setattr(mod, "__file__", __file__)
    for n, c in func().items():
        setattr(mod, n, c)
    sys.modules[modname] = mod
    return mod


class Template(object):
    """ テンプレートのコンパイルと、レンダリングを行います。
    """

    def __init__(self, template=u"", srccode=None, bytecode=None):
        """ テンプレートデータを保存し、オブジェクトを初期化します。
        また、２次キャッシュの復元の為に、srccode や bytecode データを受理します。
        args:
            template: テンプレート。ファイルまたは unicode 文字列。
            srccode: コンパイル後のソースコード。この引数は通常は指定しません。
            bytecode: コンパイル後のバイトコード。この引数は通常は指定しません。
        """
        self.template = getattr(template, "read", lambda: template)()
        self.srccode = srccode
        self.bytecode = bytecode


    def compile(self):
        """ テンプレートをコンパイルし、srccode と bytecode を準備します。"""
        if not self.bytecode:

            #Compile to src code
            if not self.srccode:
                s = self.template.replace("\r\n","\n").replace("\r","\n")
                c = [u"__buffer= []\n"]
                pos = 0
                indent = 0
                last_inline_block_row = -1
                search = self._regexp_search_code_part.search
                append = lambda s: c.append("%s%s\n" % ("    " * indent, s))
                escape = lambda s: s.replace('"', '\\"').replace("<%%", "<%").replace("%%>", "%>")
        
                while True:
                    last_inline_block_row -= 1
                    code_part = search(s, pos=pos)
        
                    #Write text part
                    text_part = s[pos:code_part.start()] if code_part else s[pos:]
                    if text_part:
                        append(u'__buffer.append(u"""%s""")' % escape(text_part))
                    
                    #End compile
                    if not code_part:
                        break
        
                    #Parse and write code part
                    pos = code_part.end()
                    code_part = code_part.groupdict()
                    code = code_part.get("code").rstrip()
                    code = self._regexp_search_multi_line.sub(" ", code)
        
                    if code_part.get("print_expr"):
                        if code_part.get("raw_mode"):
                            append(u"__buffer.append(__tostr(%s))" % code.lstrip())
                        else:
                            append(u"__buffer.append(__filter(__tostr(%s)))" % code.lstrip())
        
                    elif code:
                        lines = code.lstrip(u" \t").splitlines()
                        
                        #When single line code part
                        if len(lines) == 1:
                            line = lines[0].lstrip()
                            if not line: continue
                            li = self._regexp_parse_line_information.match(line)
                            if li:
                                li = li.groupdict()
                                if li.get("b_start"):
                                    append(line)
                                    if li.get("b_inline"):
                                        last_inline_block_row = 0
                                    else:
                                        indent += 1
                                elif li.get("b_restart"):
                                    if not last_inline_block_row == -1:
                                        indent -= 1
                                    append(line)
                                    if li.get("b_inline"):
                                        last_inline_block_row = 0
                                    else:
                                        indent += 1
                                elif li.get("b_end"):
                                    indent -= 1
                                else:
                                    append(line)
    
                        #When multi line cord part
                        else:
                            if lines.pop(0).rstrip():
                                raise SyntaxError("""Must be Empty at the block start line ("<%"), when write multi lines to code block""")
                            for i, line in enumerate(lines):
                                line = line.rstrip()
                                if line:
                                    base_indent = self._regexp_find_first_char_in_line.search(line).start()
                                    break
                            for line in lines[i:]:
                                line = line.rstrip()
                                if line:
                                    append(line[base_indent:])

                self.srccode = u"".join(c)
                if logger:
                    logger.info("Compiled src code")

            #Compile to byte code
            try:
                self.bytecode = compile(self.srccode, u"<eepy>", u"exec")
                if logger:
                    logger.info("Compiled byte code")
            except SyntaxError, e:
                e.text = u"\n".join(self.srccode.splitlines()[0:e.lineno])
                e.args = ("invalid syntax", ("<eepy>", e.lineno, e.offset, e.text))
                raise e, None, sys.exc_info()[-1]
        
        return self.bytecode


    def render(self, vars={}, filter=lambda s: s):
        """ テンプレートをレンダリングし、結果を返します。
        レンダー結果は、unicode オブジェクトです。
        args:
            vars: テンプレート変数
            filter: <%= の場合の出力フィルタ。html escape などの目的で使用。デフォルトは、何もしないフィルタ。
        """
        locals ={}
        locals.update(vars)
        locals["__template"] = self
        locals["__tostr"] = helper.tostr
        locals["__filter"] = filter
        locals["__after_render"] = []
        bytecode = self.compile()

        try:
            exec bytecode in locals
        except Exception, e :
            if self.srccode and not isinstance(e, SyntaxError):
                m = re.match(".*line (\d+).*", traceback.format_exc(2).splitlines()[-2])
                if m:
                    line = int(m.group(1))
                    e.message = ("%s\n%s" % (e.message, "\n".join(self.srccode.splitlines()[0:line]))).encode("utf-8") #TODO: ここでの encode の文字コードは決めウチでなの？ でも入れないとエラー出力が…
                    e.args = [e.message]
            raise e, None, sys.exc_info()[-1]
        
        result = u"".join(locals["__buffer"])
        
        while locals["__after_render"]:
            hook = locals["__after_render"].pop(0)
            result = hook(result, locals)
            
        return result


    def get_cache_data(self):
        """ ２次キャッシュで保存するテンプレートのデータを dict で返します。
        ここでは、srccode と bytecode を返しています。
        """
        return {"srccode": self.srccode, "bytecode": self.bytecode}


    _regexp_search_code_part = re.compile(ur"""("""
                                    r"""(?P<print_expr><%=(?P<raw_mode>(r )?))"""
                                    r"""|(^[ \t]*<%\-)"""
                                    r"""|(<%(?!%)(?:\-?))"""
                                r""")(?P<code>("([^\\"]|\\.)*"|'([^\\']|\\.)*'|(?:(?!(%>)).))*"""
                                r""")((\-%>\s*?[\n])|([^%]%>))"""
                                , re.M|re.S)
    _regexp_parse_line_information = re.compile(ur"^("
                                       r"(("
                                           r"(?P<b_start>(if|for|try|with|def|class))|"
                                           r"(?P<b_restart>(elif|else|except|finally))"
                                       r")( .*)?:(?P<b_inline> .*)?)"
                                       r"|(?P<b_end>end( ?(if|for|with|try)(\s+#.*)?)?)"
                                       r"|(?P<other>.*)"
                                    r")$")
    _regexp_search_multi_line = re.compile(ur"\s*\\\n\s*")
    _regexp_find_first_char_in_line = re.compile(ur"[^\s]")


class Renderer(object):
    """ ファイルベースでテンプレートを読み込み、処理します。
    ファイルを読み込む、ベースディレクトリを指定できます。
    オンメモリに Template インスタンスがキャッシュされます。
    ファイルや、その他のストレージを利用した２次キャッシュを利用することが出来ます。
    レンダリングの際に使われる共通のテンプレート変数を設定できます。
    """
    def __init__(self, base=None, cache=None, filter=lambda s: s, vars={}, encoding=sys.getdefaultencoding()):
        """
        args:
            base: 読み込みファイルのベースディレクトリの指定
            cache: ２次キャッシュの実装クラスの指定
            filter: <%= で値の出力の前に通過するフィルタ。html escape などの目的に使用
            vars: レンダリングに使われる共通のテンプレート変数。
            encoding: 入力ファイルのエンコード指定。未指定の時、sys.getdefaultencoding() の値
        """
        self.vars = vars
        self.base = base
        self.cache = cache
        self.filter = filter
        self.encoding = encoding
        self.fastcache = {}


    def clear(self):
        self.fastcache = {}


    def render(self, path, vars={}, filter=None):
        """ ファイルを指定し、レンダリング結果を返します。
        args:
            path: ファイルパス。フルパスまたは self.base からの相対パスで指定
            vars: テンプレート変数。__init__ で設定した vars より優先
        """
        if self.base:
            path = os.path.join(self.base, path)
        
        #Use fast cache
        if path in self.fastcache:
            if logger: logger.info("Use fast cache (path=%s)" % repr(path))
            t = self.fastcache.get(path)
        #Use 2nd cache
        elif self.cache:
            t = self.cache.get(path)
            if not t:
                #Load and compile template
                if logger: logger.info("Load template file (path=%s)" % repr(path))
                t = Template(codecs.open(path, encoding=self.encoding))
                t.compile()
                self.cache.set(path, t)
            self.fastcache[path] = t
        #Load and compile template
        else:
            if logger: logger.info("Load template file (path=%s)" % repr(path))
            t = Template(codecs.open(path, encoding=self.encoding))
            self.fastcache[path] = t
        
        locals = self.vars.copy()
        locals.update(vars)
        locals["renderer"] = self
        return t.render(locals, filter or self.filter)


@_module
def cache():
    """ ２次キャッシュ関連のモジュール
    """
    import marshal

    class CacheStorage(object):
        """ ２次キャッシュの処理実装の為の抽象クラス。"""
        def __init__(self, builder=Template):
            self.builder = builder
    
        def get(self, path):
            data = self._load(path)
            if data:
                if data.pop("__cache_timestamp__") == os.path.getmtime(path):
                    return self.builder(**data)
                if logger: logger.info("Cache is old (file=%s)"  % repr(path))
            return None
    
        def set(self, path, template):
            data = template.get_cache_data()
            data["__cache_timestamp__"] = os.path.getmtime(path)
            return self._store(path, data)
    
        def unset(self, path):
            return self._delete(path)
    
        def _load(self, path):
            raise NotImplementedError("%s#_load(): not implemented yet." % self.__class__.__name__)
    
        def _store(self, path, template):
            raise NotImplementedError("%s#_store(): not implemented yet." % self.__class__.__name__)
    
        def _delete(self, path):
            raise NotImplementedError("%s#_delete(): not implemented yet." % self.__class__.__name__)
        
        def cachename(self, key):
            return "%s.cache" % key


    class FileCacheStorage(CacheStorage):
        """ marshal を用いて、２次キャッシュをファイルに保存する CacheStorage 実装クラス。
        """
        def _load(self, path):
            path = self.cachename(path)
            if logger: logger.info("Load cache file (file=%s)" % repr(path))
            if not os.path.isfile(path):
                return None
            with open(path, "rb") as f:
                dump = f.read()
            return marshal.loads(dump)
        
        def _store(self, path, data):
            path = self.cachename(path)
            if logger: logger.info("Store cache file (file=%s)" % repr(path))
            dump = marshal.dumps(data)
            import random
            _tmp_ = "%s%s"  % (path, str(random.random())[1:])
            with open(_tmp_, 'wb') as f:
                f.write(dump)
            os.rename(_tmp_, path)
        
        def _delete(self, path):
            path = self.cachename(path)
            if os.path.isfile(path):
                os.unlink(path)


    class GaeMemcacheCacheStorage(CacheStorage):
        """ GAE の Memcache を２次キャッシュに利用する CacheStorage 実装クラス """
        
        def __init__(self, lifetime=0, builder=Template):
            CacheStorage.__init__(self, builder)
            self.lifetime = lifetime
        
        def _load(self, key):
            from google.appengine.api import memcache
            key = self.cachename(key)
            if logger: logger.info("Load memcache (key=%s)" % repr(key))
            return memcache.get(key)
        
        def _store(self, key, data):
            if "bytecode" in data:
                data.pop("bytecode")
            from google.appengine.api import memcache
            key = self.cachename(key)
            if logger: logger.info("Store memcache (key=%s)" % repr(key))
            res = memcache.set(key, data, self.lifetime)
            if not res and logger: logger.info("Failed to store memcache (key=%s)" % repr(key))
        
        def _delete(self, key):
            from google.appengine.api import memcache
            memcache.delete(self.cachename(key))
    
    return locals()


@_module
def helper():
    """ コア ヘルパを収めたモジュール
    """
    import contextlib

    def buffer_frame_locals(locals = None):
        """ __buffer を含む local コンテキストを取得する。
        所得したコンテキストを用いて、レンダリングのフローを変えたり、
        __buffer に内容を追加するヘルパを書くことができます。
        詳しくは、helper.capture などの実装を参考にしてください。
        """
        if locals is None:
            for i in xrange(2, 99):
                locals = sys._getframe(i).f_locals
                if "__buffer" in locals:
                    return locals
        else:
            return locals


    def include(path, capture_as=None, **vars):
        """ 子テンプレートを読み込んでレンダリングし、concat または locals に保存する。
        子テンプレートには、現在の locals を引数 vars で上書きしたテンプレート変数が渡されます。
        args:
            path: 子テンプレートの path
            capture_as が指定されている場合、指定された名前で locals に保存します。未指定の時、concat
            **vars: include 先に渡す追加のテンプレート変数
        """
        locals = buffer_frame_locals().copy()
        locals.update(vars)
        if "renderer" in locals:
            result = locals["renderer"].render(path, locals)
        else:
            result = Template(path).render(locals)
        if capture_as:
            locals[capture_as] = result
        else:
            concat(result, locals)


    def extends(path, **vars):
        """ path で指定されたテンプレートを親テンプレートとし、ブロックに基づき拡張した結果を返す。
        ブロックは block ヘルパで定義します。
        親テンプレートには、現在のテンプレート処理直後の locals を引数 vars で上書きしたテンプレート変数が渡されます。
        args:
            path: 親テンプレートの path
            **vars: extends 先に渡す追加のテンプレート変数
        """
        def do_extends(result, locals):
            locals.update(vars)
            if "renderer" in locals:
                return locals["renderer"].render(path, locals)
            else:
                return Template(path).render(locals)

        locals = buffer_frame_locals()
        locals["__after_render"].insert(0, do_extends)


    @contextlib.contextmanager
    def block(blockname="content"):
        """ with 句で囲んだ範囲をブロックとして登録する。
        既に保存されたブロックがある時、ブロックの内容を保存されたブロックで置き換えます。
        保存されたブロックが無い時、ブロックの内容をそのまま出力し、ブロックを保存します。
        このヘルパは通常、extends と組み合わせて使用します。
        args:
            blockname: ブロックの名前
        """
        locals = buffer_frame_locals()
        locals.setdefault("__blocks", {})

        #既に保存されたブロックがあれば、保存している内容を出力し、ここでのキャプチャ結果は破棄
        if blockname in locals["__blocks"]:
            buffer, locals["__buffer"] = locals["__buffer"], list()
            yield
            locals["__buffer"] = buffer
            locals["__buffer"].append(locals["__blocks"][blockname]) #仕様：利用後も削除せずに残しておく
        
        #保存されたブロックが無ければ、キャプチャ結果をブロックとして保存し、出力もする
        else:
            buffer, locals["__buffer"] = locals["__buffer"], list()
            yield
            captured = u"".join(locals["__buffer"])
            locals["__buffer"] = buffer
            locals["__buffer"].append(captured)
            locals["__blocks"][blockname] = captured


    @contextlib.contextmanager
    def capture(name_or_callback, _locals=None):
        """ with 句で囲んだ範囲をキャプチャし __buffer に格納するか、コールバック関数に処理を委ねる
        args:
            name_or_callback: キャプチャした内容を格納する変数名またはコールバック関数。
                        コールバック関数の呼び出し形式：callback(captured, locals)
            _locals: 通常使わない。呼び出し元で _locals が既に取得されている時、処理高速化の為に _locals を引き渡す。
        """
        locals = buffer_frame_locals(_locals)
        buffer, locals["__buffer"] = locals["__buffer"], list()
        yield
        captured = u"".join(locals["__buffer"])
        locals["__buffer"] = buffer
        if isinstance(name_or_callback, types.FunctionType):
            name_or_callback(captured, locals)
        else:
            if isinstance(name_or_callback, tuple):
                container, name = name_or_callback
            else:
                container, name = locals, name_or_callback
            container[name] = captured


    def captured_as(name):
        """ name で指定された変数を concat する。
        name が存在した場合 True を、name が存在しない時、Flase を返す。
        これにより、name が見つからない場合のデフォルト表示などを実現できます。
        args:
            name: 変数名。通常、capture() で指定した name
        ex:
            <%- if captured_as("body"): -%>
                ... default content ...
                <%- end -%>
        """
        locals = buffer_frame_locals()
        if isinstance(name, tuple):
            container, name = name
        else:
            container = locals
        if name in container:
            concat(container[name], locals)
            return True
        else:
            return False


    def concat(text, _locals=None):
        """ __buffer に単に text を追加する
        args:
            _locals: 通常使わない。呼び出し元で _locals が既に取得されている時、処理高速化の為に _locals を引き渡す。
        """
        _locals = buffer_frame_locals(_locals)
        _locals["__buffer"].append(tostr(text))


    def cycle(*values):
        """ 与えた値を繰り返し表示するジェネレータオブジェクトを返す。
        args:
            *values: 繰り返し表示する値を列挙する
        ex:
            cycle = cycle("Hoge", "Page")
            <%= cycle() %>    --->    "Hoge"
            <%= cycle() %>    --->    "Page"
            <%= cycle() %>    --->    "Hoge"
            <%= cycle() %>    --->    "Page"
        """
        def _cycle(values):
            n = len(values)
            i = 0
            while True:
                yield values[i]
                i = (i + 1) % n
        return _cycle(values).next


    def escape_xml(text):
        """ xml 文字列中の特殊文字をエスケープして返す。
        args:
            text: 対象文字列
        """
        return tostr(text).replace(u"&", u"&amp;").replace(u"<", u"&lt;").replace(u">", u"&gt;").replace(u"'", u"&#39;").replace(u'"', u"&quot;")


    def tostr(val, encoding=sys.getdefaultencoding(), errors="ignore"): #TODO: 名前を touni とかにする？
        """ 値を unicode に変換して返す。
        None の時 null-string を返す。
        args:
            val: 対象の値
            encoding: val が str の時、デコードに利用する encording
            errors: val が str の時、デコードに利用する errors
        """
        if val is None:
            return u""
        elif isinstance(val, unicode):
            return val
        elif isinstance(val, str):
            return unicode(val, encoding, errors)
        else:
            return unicode(val)

    return locals()

