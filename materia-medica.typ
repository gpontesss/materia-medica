#import "/lib/page.typ": numbered-footer

#set page(
    width: 5in,
    height: 8in,
    margin: (bottom: 0.9in, top: 0.9in, left: 0.55in, right: 0.55in),
    footer: context { link(<outline>, numbered-footer()) },
)

#set text(font: ("EB Garamond", "Noto Serif Devanagari"))
#set par(justify: true)

// Entry files arrive as four comma-separated groups (see the Makefile), so the
// book can present substances and formulas as distinct sections rather than one
// undifferentiated alphabetical run.
#let include-group(spec) = {
    for file in spec.split(",") {
        if file != "" {
            include(file)
        }
    }
}

// Section divider: a centered level-1 heading alone on its page, so it also
// appears in the front outline as a marker between the runs of entries.
#let part(title) = {
    pagebreak(weak: true)
    v(2fr)
    align(center, heading(level: 1, numbering: none, title))
    v(3fr)
    pagebreak(weak: true)
}

#columns(2, outline(depth: 1)) <outline>
#pagebreak()

#include-group(sys.inputs.at("reference", default: ""))

#part[Substance Entries]
#include-group(sys.inputs.at("substances", default: ""))

#part[Formulas]
#include-group(sys.inputs.at("formulas", default: ""))

#include-group(sys.inputs.at("glossary", default: ""))
