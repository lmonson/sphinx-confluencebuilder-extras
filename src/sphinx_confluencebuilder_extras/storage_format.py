
from contextlib import contextmanager

@contextmanager
def ac_macro(builder, node):
    yield builder.body.append(builder._start_ac_macro(node, "details"))
    builder.body.append( builder._end_ac_macro(node))

@contextmanager
def ac_rich_text_body(builder, node):
    yield  builder.body.append(builder._start_ac_rich_text_body_macro(node))
    builder.body.append( builder._end_ac_rich_text_body_macro(node))

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
    with ac_macro(builder, node) as _, \
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

def property_map(builder, node, d:dict):
    with property_table(builder,node):
        for key in d:
            value = d[key]
            property(builder, node, key, value)