
# NEW (to be considered)

## Terminology

### distinguish use of attributes: title, id, term, name
- `ID`
	- **dictionary** has an `id` that replaces the role of `title` 
	- `id` is a unique identifier for each **entry** in the dictionary
- will there be a special identifier 
- IF the dictionary is part of a "set" like the ICPP chapters, we MUST define a corresponding identifier AND decide whether it appears in the `meta`, `entry`, or both

### validation

- MUST detect and "handle" (compare/combine) plurals (eg. CHG/CHGs) when searching abbreviations
- MUST normalize diacritics (eg. **C&# 233;** is **Cé** in French)
- MUST find >1 spaces with single spaces
- MUST find and delete any spaces (and any other punctuation) before or after quotes `"` in `entry` element
- MUST replace smart quotes, apostrophes with dumb ones
- SHOULD add metadata or attribute called `[[[entry detection/selection method??]]]` indicating which tool was used to generate each dictionary entry (spacy, RAKE, YAKE, etc.)
- MUST detect exact duplicates in `@term` using everything between `entry term="  "` (see examples below). Currently, validator is marking "apium graveolens" (and others) as "duplicate terms not allowed apium graveolens"
	- entry term="apium graveolens co2 extract"
	- entry term="apium graveolens egypt"
	- entry term="apium graveolens essence"
	- entry term="apium graveolens extract"
- Consider whether we should replace greek characters with text throughout, or add alternative (symbol or text) as synonym

### syntax
- in consideration of humans who visually/manually create, manage and edit dictionaries and/or curate sets of dictionaries, the following would make their jobs easier:
	- `attributes` SHOULD be ordered (or automatically reordered) uniformly for all dictionaries
	- `entry` to allow for an attribute such as `FOR REVIEW` (preferably in capital letters) to bring questionable entries to the attention of a human
	- otherwise, some other code-commenting method
	- this would likely be most useful/convenient if placed at the very beginning of an entry, so aberrations would stick out like a sore thumb and not be lost in a sea of wrapped (or not) text


# SCHEMA

## managing dictionary sets

- When a set (collection/compilation/volume/compendium) of dictionaries are created from a  source of information on a **general topic** composed of **chapter-specific sub-topics** (i.e. ICCP Climate Reports), it SHOULD be the case that each entry `<term/>` occurs in only ONE (1) `dictionary` in that `set`, and ONLY in the `dictionary` for the chapter in which the `term` is most relevant.
- `terms` occuring with relatively equal frequency across a range of chapter `dictionaries` forming  the `set` (at minimum, in two or more (>1) chapters), SHOULD be assigned/moved to a unique `dictionary` of "set-common" terms for the general topic.
- Automating this redistribution of `terms` among `dictionaries` in a `set` would be determined (among other possible factors like, chapter title) by  frequency. Thus at least two new attributes (which MAY be deleted after `term` redistribution and `set` consolidation are complete) include:
	- `@source=""` — which requires a step for the user/agent to define the name of the chapter and source, prior to beginning term extraction
	- `@#term_frequency` 
- This will then allow another script (to be created) to compare the frequency of terms appearing in each chapter, and move (or suggest to a human for moving) the term in the most relevant dictionary, and removing it from all others.

# GENERAL RULES

- `entry` MUST have attributes:
- NOTE. case-and space-sensitivity is still being worked out.
- `entry` MAY have attributes

- `@wikidataID` . This should be a single Q- or P-item referring directly to the concept (i.e. NOT a document about it, or an object using it.
- `@wikipediaPage` (default is ENglish Wikipedia - we may revisit this) . The page SHOULD be compatible with the `@wikidataID` (NOTE: what happens if there is no EN?)
- `@id` . We MAY introduce IDs for `entry`s and decouple from `term`. Syntax and maintenance yet to be determined

- `term` This acts as an ID within the dictionary. Dictionaries MUST NOT have duplicate terms. The term should not contain spaces or punctuation. (multiword terms should be joined with `_`). (NOTE `term` is still messy. It is overloaded (an identifier and a search term. We may wish to create separate `id` . NOTE: case-insensitive terms SHOULD be lowercase. Case-sensitive or space-sensitive terms (e.g. `United Nations`, `FAO` ) should retain their case, in which case they SHOULD have a separate
- `name` . This is historically the long form of a term. It is often identical with the term, in which case it can be omitted (NOTE Messy. Suggest moving to an `@id` based on the `term` . `entry` MAY have `@name` which SHOULD be different from `@term`

## content format







# ELEMENTS

## dictionary

####  PETER These first three seem to conflict:
- `dictionary` MUST be well-formed XML but are not schema-valid.
- `dictionary` MAY use common XML languages (HTML, SVG) without namespaces (name collisions are avoided by design)
- `dictionary` MUST NOT have a namespace.

- all syntax is case-sensitive and values MUST default to `xml:lang='en'`
- `dictionary` element and attribute names MUST be chosen from 33-127 (ASCII core) and SHOULD be chosen from `[a-z_]+` Numerals SHOULD NOT be used.
	- is this rule to be applied throughout the entire XML?
- `dictionary` MUST have balanced quotations 
	- Content within xml tags that include quotes such as ``<entry term=“…”\>`` MUST NOT have odd numbers of quotation marks (” ”)

- `dictionary` MUST have single root element `dictionary`
- 
#### PETER Resolve: title vs id, and how/whether to match file name (see same issue in `@title` of meta)
- `dictionary` MUST have `@title`  or `@id` attribute (`@` means attribute)
- `dictionary` file name must match `title` or `id` in `meta`
- 
- `dictionary` MUST have `@version` . Values MUST be of form `major.minor.point` where fields are digits, starting `0.0.1`. `point` SHOULD be increased with each commit. `minor` SHOULD be discussed with community
- `dictionary` SHOULD not have other attributes
- `dictionary` MUST have at least one entry
	- (Is there a max limit (as spreadsheets have)?
	- If, so.. can we split automatically in pt1, pt2 etc? Can those be “run” concurrently with results showing as if they were one dictionary?)
- `dictionary` SHOULD contain child elements from:
	- `meta` (or `frontmatter`?) 
	- `entry`
	- `desc` and `metadata` (to be debated)`


## meta/front matter (decide name for this)

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
- Format: **?????????????**

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
- Format: text (could be a name of a person or computer program)

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




## entry

### <term/>
- attribute of `entry`
- Required: YES
- entry must have a term
- `term` may have synonyms for searching
- `term` should be trimmed and multiword terms should include single-spaces.
- `term` are generally flattened to lowercase but some must retain uppercase (e.g. UN, SDGs)
- `term` (not to be confused with `id`, `label` or `name`) is a word or phrase used to describe a thing or to express a concept, especially in a particular kind of language or branch of study (the lexical representation of the concept that is generally accepted in real world use)
- `term` formatting:
	- terms are generally EN and generally use `[A-Za-z0-9_-]+`
	- Other punctuation should be avoided (`',()` etc) but may be required (e.g. for chemicals)
	- Characters above 128 (diacritics, symbols, ideographs, etc.) must be encoded as Unicode
	- Greek characters should be replaced by `alpha`, etc but *may* be used in synonyms
	- URL-encoding (e.g. %20) or XML entities (`&amp;`) should not be used

### synonym
- attribute of `entry`
- Required: NO

### desc
#### PETER:
to maximize immediate human comprehension and useabiity, should we spell out `description` instead of `desc`? would a few extra characters kill us? Also, for the same reason, the dictionary and entry @descriptions SHOULD be distinct
- child of `entry`
- Required: OPTIONAL
- Format: ``<desc source="SOURCE">DESCRIPTION</desc>``
- Newlines in descriptions can logically be replaced by space (e.g. for tools with flowing text).
- Descriptions should not include line breaks, paragraphs, lists, etc.)
- descriptions may contain well-formed HTML markup but cannot rely on it being honoured.

### desc source
- child of `entry`
- Required: OPTIONAL
- Format: ``<desc source="SOURCE">DESCRIPTION</desc>``
- 

### wikidata_ID
- child of `entry`
- Required: OPTIONAL
- Format: number
	- numbers and letters?
- *MUST* the letters "ID" be capitalized in `wikidata_ID` ?

### wikipedia_URL
- child of `entry`
- Required: OPTIONAL
- Format: URL

### raw
- 

## other ids? 
- if no wikidata exists, but there is a chebi id or the IDC-11, do we use it? is there a tool like spaCy for such things that would also return the source's id?
