#import "/lib/page.typ": numbered-footer

#set page(
    width: 5in,
    height: 8in,
    margin: (bottom: 0.9in, top: 0.9in, left: 0.55in, right: 0.55in),
    footer: context { link(<outline>, numbered-footer()) },
)

#set text(font: ("EB Garamond", "Noto Serif Devanagari"))
#set par(justify: true)

// Entry files arrive as four comma-separated groups (see the Makefile), one per
// part of the book.
#let include-group(spec) = {
    for file in spec.split(",") {
        if file != "" {
            include(file)
        }
    }
}

// A part divider: a centered heading alone on its own page. Entry headings are
// pushed down one level while a group is included (`#set heading(offset: 1)`
// below), so the document hierarchy is:
//     level 1 = part   >   level 2 = entry title   >   level 3 = entry section
#let part(title) = {
    pagebreak(weak: true)
    v(2fr)
    align(center, text(size: 1.9em, heading(level: 1, numbering: none, title)))
    v(3fr)
    pagebreak(weak: true)
}

// Table of contents, three levels deep and styled per level so the hierarchy
// stays scannable in two narrow columns: parts bold with space above them,
// entry titles bold, section names smaller and indented beneath their entry.
#show outline.entry.where(level: 1): it => {
    v(1.1em, weak: true)
    strong(text(size: 1.15em, it))
}
#show outline.entry.where(level: 2): it => {
    v(0.35em, weak: true)
    strong(it)
}
#show outline.entry.where(level: 3): it => text(size: 0.82em, it)

#columns(2, outline(depth: 3, indent: 0.6em)) <outline>
#pagebreak()

#part[Substances]
#set heading(offset: 1)
#include-group(sys.inputs.at("substances", default: ""))
#set heading(offset: 0)

#part[Recipes & Formulas]
#set heading(offset: 1)
#include-group(sys.inputs.at("formulas", default: ""))
#set heading(offset: 0)

#part[Miscellaneous]
#set heading(offset: 1)
#include-group(sys.inputs.at("misc", default: ""))
#set heading(offset: 0)

#part[Glossary]
#set heading(offset: 1)
#include-group(sys.inputs.at("glossary", default: ""))
#set heading(offset: 0)
