

## HTML macro

A page with just an HTML macro within it.

```html
<p class="auto-cursor-target">
    <br />
</p>

<ac:structured-macro ac:name="html" ac:schema-version="1" ac:macro-id="09956335-3913-4d37-9927-12850784f303">
    <ac:plain-text-body><![CDATA[hello]]></ac:plain-text-body>
</ac:structured-macro>

<p>
    <br />
</p>

```

A page with an HTML macro and an embedded script tag

```html
<p class="auto-cursor-target">
    <br />
</p>
<ac:structured-macro ac:name="html" ac:schema-version="1" ac:macro-id="09956335-3913-4d37-9927-12850784f303">
    <ac:plain-text-body><![CDATA[<script>
        console.log("hello");
        </script>]]>
    </ac:plain-text-body>
</ac:structured-macro>

<p class="auto-cursor-target"><br /></p>

```