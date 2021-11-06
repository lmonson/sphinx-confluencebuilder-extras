import sphinx
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from .storage_format import property_map

from contextlib import contextmanager

@contextmanager
def ac_macro(builder, node, ac_name):
    yield builder.body.append(builder._start_ac_macro(node, ac_name))
    builder.body.append( builder._end_ac_macro(node))

@contextmanager
def ac_rich_text_body(builder, node):
    yield  builder.body.append(builder._start_ac_rich_text_body_macro(node))
    builder.body.append( builder._end_ac_rich_text_body_macro(node))

@contextmanager
def ac_plain_text_body(builder, node):
    yield builder.body.append( builder._start_ac_plain_text_body_macro(node))
    builder.body.append( builder._end_ac_plain_text_body_macro(node))




@contextmanager
def confluence_tag(builder, node, name):
    start =builder._start_tag( node, name)
    end =builder._end_tag(node)
    yield builder.body.append( start )
    builder.body.append( end )

@contextmanager
def text(builder, text_content):
    builder.body.append(text_content)


@contextmanager
def property_table(builder, node):
    with ac_macro(builder, node, "details") as _, \
            ac_rich_text_body(builder, node) as _, \
            confluence_tag(builder, node, "table") as _, \
            confluence_tag(builder, node, "tbody") as _:
        yield None

def property(builder, node, key, value ):
    with confluence_tag(builder, node, "tr"):
        with confluence_tag(builder,node,"th"):
            text(builder, key)
        with confluence_tag(builder,node,"td"):
            text(builder, value)



def kebab_case_to_camel_case(s):
    """
    convert a kebab case string to a camel case string
    A utility function to help convert a kebab case string into a camel case
    string. This is to help convert directive options typically defined in kebab
    case to Confluence macro parameters values which are typically required to
    be in camel case.
    Args:
        s: the string to convert
    Returns:
        the converted string
    """
    s = ''.join(list(map(lambda x: x.capitalize(), s.split('-'))))
    s = s[0].lower() + s[1:]
    return s

class pageproperties(nodes.Element):
    def astext(self):
        return self.get('alt', '')

class pageproperty(nodes.Element):
    def astext(self):
        return self.get('alt', '')


class PageProperty(Directive):
    """
    Directive to insert arbitrary page properties markup.
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 99
    final_argument_whitespace = False

    def run(self):

        property_name = " ".join(self.arguments)

        node = pageproperty()
        node.property_name = property_name
        self.state.nested_parse( self.content, self.content_offset, node );
        return [node]

class hillchart(nodes.Element):
    def astext(self):
        return self.get('alt', '')

class Hillchart(Directive):
    """
   Directive to insert arbitrary page properties markup.
   """
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        hillchart_title = " ".join(self.arguments)
        node = hillchart()
        node.hillchart_title = hillchart_title
        node.block_text = self.block_text

        self.state.nested_parse( self.content, self.content_offset, node );

        return [node]

def confluence_visit_hillchart(self, node):
    js_args = node.block_text.split('\n');
    js_args = [ x for x in map( lambda x: x.strip(), js_args ) ]
    js_args = [ x for x in map( lambda x : f'"{x}"', js_args ) ]
    js_args = ",".join( js_args )

    html_text = f"""
    <script type="module">
        import {{hillChart}} from "https://cdn.skypack.dev/ez-conf-hillchart";
        
        hillChart(
            "{node.hillchart_title}",
            [ {js_args} ]
        );
    </script>
    """
    with ac_macro(self, node, "html"):
        with ac_plain_text_body(self,node):
            text(self, html_text);
    raise nodes.SkipChildren()

def confluence_depart_hillchart(self, node):
    pass


class PageProperties(Directive):
    """
    Directive to insert arbitrary page properties markup.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        # import pydevd_pycharm
        # pydevd_pycharm.settrace('localhost', port=8089, stdoutToServer=True, stderrToServer=True)

        node = pageproperties()
        self.state.nested_parse( self.content, self.content_offset, node );
        # params = node.setdefault('params', {})
        # print(f"\n\n {self.options}\n\n")
        #
        # for k, v in self.options.items():
        #     print(f"\t{k} : {v}")
        #     params[kebab_case_to_camel_case(k)] = v
        return [node]

def property_map(builder, node, d:dict):
    with property_table(builder,node):
        for key in d:
            value = d[key]
            property(builder, node, key, value)

def confluence_visit_pageproperties(self, node):
    # block_labels = {}
    # for k,v in node['params']:
    #     block_labels[k] = v
    # block_labels["extra"] = "extra value"
    # output_node = pageproperties()
    # node.replace_self( output_node )
    #
    # property_map( self, output_node, block_labels )
    # print(f"\n visitor: {self} {dir(self)}")
    # from sphinxcontrib.confluencebuilder.translator.storage import ConfluenceStorageFormatTranslator
    # x = ConfluenceStorageFormatTranslator()

    property_children =[ c for c in node.children if isinstance(c,pageproperty)]

    with property_table(self, node):
        for child in property_children:
            # print(f"\nCCC: {child.property_name}")
            with confluence_tag(self, node, "tr"):
                with confluence_tag(self,node,"th"):
                    text(self, child.property_name)
                with confluence_tag(self,node,"td") as td_tag:
                    for tnode in child.children:
                        # print(f"\n\nTNODE {tnode}")
                        tnode.walkabout( self )
                        # self.dispatch_visit( tnode );

    raise nodes.SkipChildren()

def confluence_depart_pageproperties(self, node):
    pass


def confluence_visit_pageproperty(self, node):
    raise nodes.SkipNode()

def confluence_depart_page_property(self, node):
    pass

def setup(app):
    app.add_node(pageproperties,
                 # html=(html_visit_mermaid, None),
                 # latex=(latex_visit_mermaid, None),
                 # texinfo=(texinfo_visit_mermaid, None),
                 # text=(text_visit_mermaid, None),
                 # man=(man_visit_mermaid, None),
                 confluence=(confluence_visit_pageproperties, confluence_depart_pageproperties),
                 )
    app.add_node(pageproperty,
                 # html=(html_visit_mermaid, None),
                 # latex=(latex_visit_mermaid, None),
                 # texinfo=(texinfo_visit_mermaid, None),
                 # text=(text_visit_mermaid, None),
                 # man=(man_visit_mermaid, None),
                 confluence=(confluence_visit_pageproperty, confluence_depart_page_property),
                 )

    app.add_directive('pageproperties', PageProperties)
    app.add_directive("pageproperty", PageProperty)




    app.add_directive('hillchart', Hillchart)
    app.add_node(
        hillchart,
        confluence=(confluence_visit_hillchart,confluence_depart_hillchart)
    )

    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}