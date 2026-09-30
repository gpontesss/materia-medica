#import "/lib/page.typ": numbered-footer

#set page(
    width: 5in,
    height: 8in,
    margin: (bottom: 0.9in, top: 0.9in, left: 0.55in, right: 0.55in),
    footer: context { link(<outline>, numbered-footer()) },
)

#set text(font: ("EB Garamond", "Noto Serif Devanagari"))
#set par(justify: true)

#columns(2, outline(depth: 1)) <outline>
#pagebreak()

#for file in sys.inputs.files.split(",") {
    if file != "" {
        include(file)
    }
}
