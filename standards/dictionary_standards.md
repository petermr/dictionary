
## NEW: to be considered
1. detect plurals when searching abbreviations (eg. CHG/CHGs) 
2. add metadata or attribute indicating which tool was used to generate each dictionary entry (spacy, RAKE, YAKE, etc.)
3. distinguish use of attributes: term vs name
4. new attribute to tag "For Review" to bring such entries to the attention of a human
5. Must detect and replace unicode characters (eg. `C&#233;`` is `Cé` in French)
6. find multiple spaces with single spaces
7. **In a set of dictionaries from a specific source of information like the ICCP Climate Reports, any specific term should show up in only *one dictionary* in that library set — unless it occurs as frequently in all of them, in which case those terms would be in a dictionary of "volume-wide" terms.** (eg. Some terms and abbreviations may be climate-specific, but not chapter-specific. So in the case of the ICPP reports, we want to ensure extracted abbreviated terms are included only in the chapter in which the term is most relevant.)
- Therefore, when dictionaries are being created from individual ICPP chapters, it would be useful to include two new attributes:
	- `source=""` (which requires a step for the user to input the name of the source, or for it to be detected from the source document as a first step of term extraction)
	- `count=""`
- This will then allow another script (to be created) to compare the frequency of terms appearing in each chapter, and move (or suggest to a human for moving) the term in the most relevant dictionary, and removing it from all others.

# GENERAL RULES

- Dictionaries MUST be *well-formed* XML but are not schema-valid.
- Content within xml tags that include quotes such as ``<entry term=“…”\>`` MUST NOT have odd numbers of quotation marks (” ”)
- `dictionary` has no namespace.
- Common XML languages (HTML, SVG) MAY be used without namespaces (name collisions are avoided by design)
- all syntax is case-sensitive and values MUST default to `xml:lang='en'`
-  element- and attribute-names MUST be chosen from 33-127 (ASCII core) and SHOULD be chosen from `[a-z_]+` Numerals SHOULD NOT be used.
-  `dictionary` MUST have single root element `dictionary`
-  `dictionary` MUST have `@title` attribute (`@` means attribute)
-  `dictionary` MUST have `@version` . Values MUST be of form `major.minor.point` where fields are digits, starting `0.0.1`. `point` SHOULD be increased with each commit. `minor` SHOULD be discussed with community
-   `dictionary` should not have other attributes
-   `dictionary` SHOULD contain child elements from:

-   `entry`
-   `desc`
-   `metadata. (debate the last two)`

-   `dictionary` SHOULD NOT contain other child elements
-   `entry` MUST have attributes:

-    NOTE. case-and space-sensitivity is still being worked out.

-   `entry` MAY have attributes

-    `@wikidataID` . This should be a single Q- or P-item referring directly to the concept (i.e. NOT a document about it, or an object using it.
-   `@wikipediaPage` (default is ENglish Wikipedia - we may revisit this) . The page SHOULD be compatible with the `@wikidataID` (NOTE: what happens if there is no EN?)
-   `@id` . We MAY introduce IDs for `entry`s and decouple from `term`. Syntax and maintenance yet to be determined

-   `term` This acts as an ID within the dictionary. Dictionaries MUST NOT have duplicate terms. The term should not contain spaces or punctuation. (multiword terms should be joined with `_`). (NOTE `term` is still messy. It is overloaded (an identifier and a search term. We may wish to create separate `id` . NOTE: case-insensitive terms SHOULD be lowercase. Case-sensitive or space-sensitive terms (e.g. `United Nations`,  `FAO` ) should retain their case, in which case they SHOULD have a separate
-   `name` . This is historically the long form of a term. It is often identical with the term, in which case it can be omitted (NOTE Messy. Suggest moving to an `@id` based on the `term` .  `entry` MAY have `@name` which SHOULD be different from `@term`

## content format
- must have at least one entry
    - (Is there a max limit (as spreadsheets have)?
    - If, so.. can we split automatically in pt1, pt2 etc? Can those be “run” concurrently with results showing as if they were one dictionary?)


# elements

## meta

### encoding

- child of `meta`
- Required: REQUIRED
- `<?xml version="1.0" encoding="UTF-8"?>`

### title

- child of `meta`
- Required: REQUIRED
- **title** must be match **dictionary’s file name**

### description

- child of `meta`
- Required: REQUIRED
- - Format:
- **title** must be match **dictionary’s file name**

### version

- child of `meta`
- Required: OPTIONAL
- Format: numbers and decimals (0.0.0)

### modificationDate

- child of `meta`
- Required: OPTIONAL
- Format: date?

### modifiedBy

- child of `meta`
- Required: OPTIONAL
- Format: text (could be a name of a person or program

### modificationDetails

- child of `meta`
- Required: OPTIONAL
- Format: text

### author(s)

- child of `meta`
- Required: OPTIONAL
- Format: text

### contributors

- child of `meta`
- Required: OPTIONAL
- Format: text

### datasource(s)

- child of `meta`
- Required: OPTIONAL
- tag: ``<datasource>”…"</datasource>``
- Definition: *I think of this as dictionaries “translated” from existing sources such as Ontobee Ontologies, proprietary databases, webscraped, Dr. Duke, MCID, etc.*


- Format: text, may be URLs or named entities. Example:
	
	``<datasource>[http://www.nipgr.ac.in/Essoildb](http://www.nipgr.ac.in/Essoildb), FDA, Chebli, Ontobee Ontologies, proprietary databases, webscraped, Dr. Duke, MCID</datasource>``

### license

- child of `meta`
- Required: OPTIONAL
- Format: text, numbers, symbols ™ ® © (Possibly not roman text)
- examples:
	- [https://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1](https://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1)
	- [https://github.com/petermr/ami3/blob/master/LICENSE](https://github.com/petermr/ami3/blob/master/LICENSE)


----

## entry

### <term/>

- attribute of `entry`
- Required: YES
- terms are generally EN and generally use `[A-Za-z0-9_-]+`
- Other punctuation should be avoided (`',()` etc) but may be required (e.g. for chemicals)
- Characters above 128 (diacritics, symbols, ideographs, etc.) must be encoded as Unicode
- Greek characters should be replaced by `alpha`, etc but *may* be used in synonyms
- URL-encoding (e.g. %20) or XML entities (`&amp;`) should not be used
- terms may have synonyms for searching
- terms should be trimmed and multiword terms should include single-spaces.
- terms are generally flattened to lowercase but some must retain uppercase (e.g. UN, SDGs)

### desc souce

- child of `entry`
- Required: OPTIONAL
- Format: <desc source="SOURCE">DESCRIPTION</desc>
- Examples:
`<desc source="Manny">A medicinal plant found in North America</desc>`
`<desc source="Wikidata">Infection caused by Candida Albicans"</desc>`

- Newlines in descriptions can logically be replaced by space (e.g. for tools with flowing text).
- Descriptions should not include line breaks, paragraphs, lists, etc.)
- descriptions may contain well-formed HTML markup but cannot rely on it being honoured.



----

### wikidata_ID

- child of `entry`
- Required: OPTIONAL
- Format: number

### wikipedia_URL

- child of `entry`
- Required: OPTIONAL
- Format: URL