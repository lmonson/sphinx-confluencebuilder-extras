from sphinxcontrib.mermaid import render_mm
from docutils.nodes import Structural, Element, General
from docutils import nodes
from sphinxcontrib.mermaid import MermaidError
from sphinxcontrib.mermaid import logger as mermaid_logger
from sphinxcontrib.mermaid import mermaid
from sphinxcontrib.mermaid import render_mm
from .storage_format import ac_macro, confluence_tag, ac_rich_text_body, text, property_map

def generic_visit_mermaid(self, node):
    try:
        fname, _ = render_mm(
            self, node['code'], node['options'], 'png', 'mermaid')
    except MermaidError as exc:
        mermaid_logger.warning('mermaid code %r: ' % node['code'] + str(exc))
        raise nodes.SkipNode

    img_node = nodes.image(uri=fname, alt=node.get('alt', ''))
    if 'align' in node:
        img_node['align'] = node['align']
    node.replace_self(img_node)
    self.visit_image(img_node)

    property_map(
        self,
        img_node,
        {
            "Property __1__": "Value One"
        }
    )
    # with ac_macro(self, img_node) as _, \
    #         ac_rich_text_body(self, img_node) as _, \
    #         confluence_tag(self, img_node, "table") as _, \
    #         confluence_tag(self, img_node, "tbody") as _:
    #     with confluence_tag(self, img_node, "tr"):
    #         with confluence_tag(self,img_node,"th"):
    #             text(self, "Property One")
    #         with confluence_tag(self,img_node,"td"):
    #             text(self, "Value One")

def generic_depart_mermaid(self, node):
    pass

class mermaid(nodes.General, nodes.Inline, nodes.Element):
    pass

def add_mermaid_for_confluence(app):
    app.add_node(mermaid,
                 confluence=(generic_visit_mermaid, generic_depart_mermaid),
                 override=True)
