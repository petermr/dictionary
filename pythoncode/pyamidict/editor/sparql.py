# resources
"""
sparql tools - experimental
"""


"""
SELECT DISTINCT ?wikidata ?wikidataLabel ?wikipedia ?wikidataAltLabel ?wikidataDescription ?hindi ?hindiLabel ?hindialtlabel ?hindiwikipedia ?tamil ?tamilLabel ?tamilaltlabel ?tamilwikipedia ?spanish ?spanishaltlabel ?spanishLabel ?pt ?ptLabel ?ptaltlabel ?kn ?knLabel ?knaltlabel ?de ?deLabel ?dealtlabel ?sa ?saLabel ?saaltlabel ?ml ?mlLabel ?mlaltlabel ?fr ?frLabel ?fraltlabel ?zh ?zhLabel ?zhaltlabel ?ICD_10 WHERE {
  ?wikidata wdt:P31/wdt:P279* wd:Q12136.
   OPTIONAL { ?wikipedia schema:about ?wikidata; schema:isPartOf <https://en.wikipedia.org/> }
   OPTIONAL { ?hindiwikipedia schema:about ?wikidata; schema:isPartOf <https://hi.wikipedia.org/> }
   OPTIONAL { ?tamilwikipedia schema:about ?wikidata; schema:isPartOf <https://ta.wikipedia.org/> }
   OPTIONAL { ?wikidata wdt:P494 ?ICD_10. }
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en".

## Selecting the prefered label 
    ?wikidata skos:altLabel ?wikidataAltLabel ; rdfs:label ?wikidataLabel; schema:description  ?wikidataDescription          
  } 
   SERVICE wikibase:label {
    bd:serviceParam wikibase:language "hi".
## Selecting the prefered label
    ?wikidata skos:altLabel ?hindialtlabel .
    ?wikidata rdfs:label ?hindiLabel .
    ?wikidata schema:description ?hindi ;
  } 
  
"""


EN = ("english",    "en")
ES = ("spanish",    "es")
FR = ("french",     "fr")
HI = ("hindi",      "hi")
PT = ("portuguese", "pt")
TA = ("tamil",      "ta")
UR = ("urdu",       "ur")

SYMBOLS = {
    "__CLASS_SUBCLASS": "wdt:P31/wdt:P279*",
    "__ISA": "P31",
    "__COUNTRY_P": "P17",
}

WIKIBASE_LABEL = "wikibase:label"
WIKIBASE_LANGUAGE = "wikibase:language"

BD_SERVICE_PARAM = "bd:serviceParam"

END = "end"
START = "start"
SERVICE_PARAM = "service_param"
SKOS = "skos"
Q_WIKIDATA = "?wikidata"
LABEL = "Label"
ALT_LABEL = "altLabel"
RDFS_LABEL = "rdfs:label"
SKOS_ALT_LABEL = "skos:altLabel"
DESCRIPTION = "description"
SCHEMA_DESCRIPTION = "schema:description"

DOT = "."
SEMICOLON = ";"
SP = " "

class Sparql():

    def __init__(self):
        pass
        self.selectables = []
        self.triples = []
        self.languages = []

    """
       SERVICE wikibase:label {
        bd:serviceParam wikibase:language "hi".
    ## Selecting the prefered label
        ?wikidata skos:altLabel ?hindialtlabel .
        ?wikidata rdfs:label ?hindiLabel .
        ?wikidata schema:description ?hindi ;
      } 
      
    """
    def create_lang_service(self, language, *, fields=None):
        service = "SERVICE" + " " + WIKIBASE_LABEL + " " + "{\n"
        service = service + " " + BD_SERVICE_PARAM + " " + WIKIBASE_LANGUAGE + SP + '"' + language[1] + '"' + DOT + "\n"
#        if SKOS in fields or True:
        service = service + " " + Q_WIKIDATA + " " + SKOS_ALT_LABEL + " " + "?" + language[1] + ALT_LABEL + DOT + "\n"
#        if LABEL in fields or True:
        service = service + " " + Q_WIKIDATA + " " + RDFS_LABEL + " " + "?" + language[1] + LABEL + DOT + "\n"
#        if DESCRIPTION in fields or True:
        service = service + " " + Q_WIKIDATA + " " + SCHEMA_DESCRIPTION + " " + "?" + language[1] + SEMICOLON + "\n"
        service = service + "} # end SERVICE " + "\n"
        return service

    def add_selectable(self, str):
        if str.startswith("?"):
            self.selectables.append(str)

    def add_triple(self, subj, pred, obj):
        if pred.startswith("__"):
            pred = self.lookup(self)
        triple = (subj, pred, obj)
        self.triples.append(triple)
        self.add_selectable(subj)
        self.add_selectable(pred)
        self.add_selectable(obj)

    """
    OPTIONAL { 
        ?wikipedia schema:about ?wikidata; 
        ?wikipedia schema:isPartOf <https://en.wikipedia.org/> 
        }
    """

    def create_select(self, distinct=True):
        query = "SELECT "
        if distinct:
            query = query + " DISTINCT "
        for selectable in self.selectables:
            query =  query + " " + selectable
        return query

    @staticmethod
    def create_where(param):
        if (START == param):
            return "WHERE {"
        if (END == param):
            return "} # end WHERE \n"
        print("bad where param ", param)

    @staticmethod
    def create_triple(triple):
        tt = triple[0] + " " + triple[1] + " " +  triple[2]
        return tt

    def create_triples(self, optional=False):
        triplesx = []
        for triple in self.triples:
            tt = ""
            if optional:
                tt = "OPTIONAL { "
            tt = tt + Sparql.create_triple(triple)
            if optional:
                tt = tt + " } # end OPTIONAL"
            triplesx.append(tt)
        return triplesx

    def create_whole_query(self):

        query_select = self.create_select(distinct=True)
        where0 = self.create_where("start")
        query_triples0 = self.create_triples(optional=False)
        query_triples1 = self.create_triples(optional=True)
        lang_services = []
        for language in self.languages:
            lang_services.append(self.create_lang_service(language))
        where1 = self.create_where("end")
        query = query_select + "\n"
        query = query + where0 + "\n"
        for query_triple in query_triples0:
            query = query + query_triple + "\n"
        for query_triple in query_triples1:
            query = query + query_triple + "\n"
        for lang_service in lang_services:
            query = query + lang_service
        query = query + where1
        query = query + self.create_limit()

        return query

    def add_languages(self, langs):
        for lang in langs:
            self.add_language(lang)
        pass

    def add_language(self, lang):
        if lang not in self.languages:
            self.languages.append(lang)

    # sets limit of hits (anything other than positive integer set to None)
    def set_limit(self, limit):
        self.limit = None
        if type(limit) == int:
            self.limit = limit
        else:
            self.limit = None
        pass

    def create_limit(self):
        if self.limit is not None:
            return "    LIMIT " + str(self.limit) + "\n"
        return ""

    def lookup(self, symbol):
        result = None
        if symbol in symbols:
            result = symbols[target]
        else:
            print("cannot resolve symbol", tsymbol)
            result = None
        return result


def main():
    """
    return
    """
    sp = Sparql()
    sp.set_limit(1000)
    sp.add_triple("?item", "wdt:P31/wdt:P279*", "?")
    sp.add_triple("?c", "PRED2", "?d")
    sp.add_languages([HI, PT])
    query = sp.create_whole_query()
    """
    ss = sp.create_lang_service(HI)
    query = query + ss
    print(ss)
    ss = sp.create_lang_service(PT)
    query = query + ss
    """
    print(query)



#========================

if __name__ == "__main__":
    main()
else:
    main()


"""
[1]  	QueryUnit	  ::=  	Query
[2]  	Query	  ::=  	Prologue
( SelectQuery | ConstructQuery | DescribeQuery | AskQuery )
ValuesClause
[3]  	UpdateUnit	  ::=  	Update
[4]  	Prologue	  ::=  	( BaseDecl | PrefixDecl )*
[5]  	BaseDecl	  ::=  	'BASE' IRIREF
[6]  	PrefixDecl	  ::=  	'PREFIX' PNAME_NS IRIREF
[7]  	SelectQuery	  ::=  	SelectClause DatasetClause* WhereClause SolutionModifier
[8]  	SubSelect	  ::=  	SelectClause WhereClause SolutionModifier ValuesClause
[9]  	SelectClause	  ::=  	'SELECT' ( 'DISTINCT' | 'REDUCED' )? ( ( Var | ( '(' Expression 'AS' Var ')' ) )+ | '*' )
[10]  	ConstructQuery	  ::=  	'CONSTRUCT' ( ConstructTemplate DatasetClause* WhereClause SolutionModifier | DatasetClause* 'WHERE' '{' TriplesTemplate? '}' SolutionModifier )
[11]  	DescribeQuery	  ::=  	'DESCRIBE' ( VarOrIri+ | '*' ) DatasetClause* WhereClause? SolutionModifier
[12]  	AskQuery	  ::=  	'ASK' DatasetClause* WhereClause SolutionModifier
[13]  	DatasetClause	  ::=  	'FROM' ( DefaultGraphClause | NamedGraphClause )
[14]  	DefaultGraphClause	  ::=  	SourceSelector
[15]  	NamedGraphClause	  ::=  	'NAMED' SourceSelector
[16]  	SourceSelector	  ::=  	iri
[17]  	WhereClause	  ::=  	'WHERE'? GroupGraphPattern
[18]  	SolutionModifier	  ::=  	GroupClause? HavingClause? OrderClause? LimitOffsetClauses?
[19]  	GroupClause	  ::=  	'GROUP' 'BY' GroupCondition+
[20]  	GroupCondition	  ::=  	BuiltInCall | FunctionCall | '(' Expression ( 'AS' Var )? ')' | Var
[21]  	HavingClause	  ::=  	'HAVING' HavingCondition+
[22]  	HavingCondition	  ::=  	Constraint
[23]  	OrderClause	  ::=  	'ORDER' 'BY' OrderCondition+
[24]  	OrderCondition	  ::=  	( ( 'ASC' | 'DESC' ) BrackettedExpression )
| ( Constraint | Var )
[25]  	LimitOffsetClauses	  ::=  	LimitClause OffsetClause? | OffsetClause LimitClause?
[26]  	LimitClause	  ::=  	'LIMIT' INTEGER
[27]  	OffsetClause	  ::=  	'OFFSET' INTEGER
[28]  	ValuesClause	  ::=  	( 'VALUES' DataBlock )?
[29]  	Update	  ::=  	Prologue ( Update1 ( ';' Update )? )?
[30]  	Update1	  ::=  	Load | Clear | Drop | Add | Move | Copy | Create | InsertData | DeleteData | DeleteWhere | Modify
[31]  	Load	  ::=  	'LOAD' 'SILENT'? iri ( 'INTO' GraphRef )?
[32]  	Clear	  ::=  	'CLEAR' 'SILENT'? GraphRefAll
[33]  	Drop	  ::=  	'DROP' 'SILENT'? GraphRefAll
[34]  	Create	  ::=  	'CREATE' 'SILENT'? GraphRef
[35]  	Add	  ::=  	'ADD' 'SILENT'? GraphOrDefault 'TO' GraphOrDefault
[36]  	Move	  ::=  	'MOVE' 'SILENT'? GraphOrDefault 'TO' GraphOrDefault
[37]  	Copy	  ::=  	'COPY' 'SILENT'? GraphOrDefault 'TO' GraphOrDefault
[38]  	InsertData	  ::=  	'INSERT DATA' QuadData
[39]  	DeleteData	  ::=  	'DELETE DATA' QuadData
[40]  	DeleteWhere	  ::=  	'DELETE WHERE' QuadPattern
[41]  	Modify	  ::=  	( 'WITH' iri )? ( DeleteClause InsertClause? | InsertClause ) UsingClause* 'WHERE' GroupGraphPattern
[42]  	DeleteClause	  ::=  	'DELETE' QuadPattern
[43]  	InsertClause	  ::=  	'INSERT' QuadPattern
[44]  	UsingClause	  ::=  	'USING' ( iri | 'NAMED' iri )
[45]  	GraphOrDefault	  ::=  	'DEFAULT' | 'GRAPH'? iri
[46]  	GraphRef	  ::=  	'GRAPH' iri
[47]  	GraphRefAll	  ::=  	GraphRef | 'DEFAULT' | 'NAMED' | 'ALL'
[48]  	QuadPattern	  ::=  	'{' Quads '}'
[49]  	QuadData	  ::=  	'{' Quads '}'
[50]  	Quads	  ::=  	TriplesTemplate? ( QuadsNotTriples '.'? TriplesTemplate? )*
[51]  	QuadsNotTriples	  ::=  	'GRAPH' VarOrIri '{' TriplesTemplate? '}'
[52]  	TriplesTemplate	  ::=  	TriplesSameSubject ( '.' TriplesTemplate? )?
[53]  	GroupGraphPattern	  ::=  	'{' ( SubSelect | GroupGraphPatternSub ) '}'
[54]  	GroupGraphPatternSub	  ::=  	TriplesBlock? ( GraphPatternNotTriples '.'? TriplesBlock? )*
[55]  	TriplesBlock	  ::=  	TriplesSameSubjectPath ( '.' TriplesBlock? )?
[56]  	GraphPatternNotTriples	  ::=  	GroupOrUnionGraphPattern | OptionalGraphPattern | MinusGraphPattern | GraphGraphPattern | ServiceGraphPattern | Filter | Bind | InlineData
[57]  	OptionalGraphPattern	  ::=  	'OPTIONAL' GroupGraphPattern
[58]  	GraphGraphPattern	  ::=  	'GRAPH' VarOrIri GroupGraphPattern
[59]  	ServiceGraphPattern	  ::=  	'SERVICE' 'SILENT'? VarOrIri GroupGraphPattern
[60]  	Bind	  ::=  	'BIND' '(' Expression 'AS' Var ')'
[61]  	InlineData	  ::=  	'VALUES' DataBlock
[62]  	DataBlock	  ::=  	InlineDataOneVar | InlineDataFull
[63]  	InlineDataOneVar	  ::=  	Var '{' DataBlockValue* '}'
[64]  	InlineDataFull	  ::=  	( NIL | '(' Var* ')' ) '{' ( '(' DataBlockValue* ')' | NIL )* '}'
[65]  	DataBlockValue	  ::=  	iri | RDFLiteral | NumericLiteral | BooleanLiteral | 'UNDEF'
[66]  	MinusGraphPattern	  ::=  	'MINUS' GroupGraphPattern
[67]  	GroupOrUnionGraphPattern	  ::=  	GroupGraphPattern ( 'UNION' GroupGraphPattern )*
[68]  	Filter	  ::=  	'FILTER' Constraint
[69]  	Constraint	  ::=  	BrackettedExpression | BuiltInCall | FunctionCall
[70]  	FunctionCall	  ::=  	iri ArgList
[71]  	ArgList	  ::=  	NIL | '(' 'DISTINCT'? Expression ( ',' Expression )* ')'
[72]  	ExpressionList	  ::=  	NIL | '(' Expression ( ',' Expression )* ')'
[73]  	ConstructTemplate	  ::=  	'{' ConstructTriples? '}'
[74]  	ConstructTriples	  ::=  	TriplesSameSubject ( '.' ConstructTriples? )?
[75]  	TriplesSameSubject	  ::=  	VarOrTerm PropertyListNotEmpty | TriplesNode PropertyList
[76]  	PropertyList	  ::=  	PropertyListNotEmpty?
[77]  	PropertyListNotEmpty	  ::=  	Verb ObjectList ( ';' ( Verb ObjectList )? )*
[78]  	Verb	  ::=  	VarOrIri | 'a'
[79]  	ObjectList	  ::=  	Object ( ',' Object )*
[80]  	Object	  ::=  	GraphNode
[81]  	TriplesSameSubjectPath	  ::=  	VarOrTerm PropertyListPathNotEmpty | TriplesNodePath PropertyListPath
[82]  	PropertyListPath	  ::=  	PropertyListPathNotEmpty?
[83]  	PropertyListPathNotEmpty	  ::=  	( VerbPath | VerbSimple ) ObjectListPath ( ';' ( ( VerbPath | VerbSimple ) ObjectList )? )*
[84]  	VerbPath	  ::=  	Path
[85]  	VerbSimple	  ::=  	Var
[86]  	ObjectListPath	  ::=  	ObjectPath ( ',' ObjectPath )*
[87]  	ObjectPath	  ::=  	GraphNodePath
[88]  	Path	  ::=  	PathAlternative
[89]  	PathAlternative	  ::=  	PathSequence ( '|' PathSequence )*
[90]  	PathSequence	  ::=  	PathEltOrInverse ( '/' PathEltOrInverse )*
[91]  	PathElt	  ::=  	PathPrimary PathMod?
[92]  	PathEltOrInverse	  ::=  	PathElt | '^' PathElt
[93]  	PathMod	  ::=  	'?' | '*' | '+'
[94]  	PathPrimary	  ::=  	iri | 'a' | '!' PathNegatedPropertySet | '(' Path ')'
[95]  	PathNegatedPropertySet	  ::=  	PathOneInPropertySet | '(' ( PathOneInPropertySet ( '|' PathOneInPropertySet )* )? ')'
[96]  	PathOneInPropertySet	  ::=  	iri | 'a' | '^' ( iri | 'a' )
[97]  	Integer	  ::=  	INTEGER
[98]  	TriplesNode	  ::=  	Collection | BlankNodePropertyList
[99]  	BlankNodePropertyList	  ::=  	'[' PropertyListNotEmpty ']'
[100]  	TriplesNodePath	  ::=  	CollectionPath | BlankNodePropertyListPath
[101]  	BlankNodePropertyListPath	  ::=  	'[' PropertyListPathNotEmpty ']'
[102]  	Collection	  ::=  	'(' GraphNode+ ')'
[103]  	CollectionPath	  ::=  	'(' GraphNodePath+ ')'
[104]  	GraphNode	  ::=  	VarOrTerm | TriplesNode
[105]  	GraphNodePath	  ::=  	VarOrTerm | TriplesNodePath
[106]  	VarOrTerm	  ::=  	Var | GraphTerm
[107]  	VarOrIri	  ::=  	Var | iri
[108]  	Var	  ::=  	VAR1 | VAR2
[109]  	GraphTerm	  ::=  	iri | RDFLiteral | NumericLiteral | BooleanLiteral | BlankNode | NIL
[110]  	Expression	  ::=  	ConditionalOrExpression
[111]  	ConditionalOrExpression	  ::=  	ConditionalAndExpression ( '||' ConditionalAndExpression )*
[112]  	ConditionalAndExpression	  ::=  	ValueLogical ( '&&' ValueLogical )*
[113]  	ValueLogical	  ::=  	RelationalExpression
[114]  	RelationalExpression	  ::=  	NumericExpression ( '=' NumericExpression | '!=' NumericExpression | '<' NumericExpression | '>' NumericExpression | '<=' NumericExpression | '>=' NumericExpression | 'IN' ExpressionList | 'NOT' 'IN' ExpressionList )?
[115]  	NumericExpression	  ::=  	AdditiveExpression
[116]  	AdditiveExpression	  ::=  	MultiplicativeExpression ( '+' MultiplicativeExpression | '-' MultiplicativeExpression | ( NumericLiteralPositive | NumericLiteralNegative ) ( ( '*' UnaryExpression ) | ( '/' UnaryExpression ) )* )*
[117]  	MultiplicativeExpression	  ::=  	UnaryExpression ( '*' UnaryExpression | '/' UnaryExpression )*
[118]  	UnaryExpression	  ::=  	  '!' PrimaryExpression
| '+' PrimaryExpression
| '-' PrimaryExpression
| PrimaryExpression
[119]  	PrimaryExpression	  ::=  	BrackettedExpression | BuiltInCall | iriOrFunction | RDFLiteral | NumericLiteral | BooleanLiteral | Var
[120]  	BrackettedExpression	  ::=  	'(' Expression ')'
[121]  	BuiltInCall	  ::=  	  Aggregate
| 'STR' '(' Expression ')'
| 'LANG' '(' Expression ')'
| 'LANGMATCHES' '(' Expression ',' Expression ')'
| 'DATATYPE' '(' Expression ')'
| 'BOUND' '(' Var ')'
| 'IRI' '(' Expression ')'
| 'URI' '(' Expression ')'
| 'BNODE' ( '(' Expression ')' | NIL )
| 'RAND' NIL
| 'ABS' '(' Expression ')'
| 'CEIL' '(' Expression ')'
| 'FLOOR' '(' Expression ')'
| 'ROUND' '(' Expression ')'
| 'CONCAT' ExpressionList
| SubstringExpression
| 'STRLEN' '(' Expression ')'
| StrReplaceExpression
| 'UCASE' '(' Expression ')'
| 'LCASE' '(' Expression ')'
| 'ENCODE_FOR_URI' '(' Expression ')'
| 'CONTAINS' '(' Expression ',' Expression ')'
| 'STRSTARTS' '(' Expression ',' Expression ')'
| 'STRENDS' '(' Expression ',' Expression ')'
| 'STRBEFORE' '(' Expression ',' Expression ')'
| 'STRAFTER' '(' Expression ',' Expression ')'
| 'YEAR' '(' Expression ')'
| 'MONTH' '(' Expression ')'
| 'DAY' '(' Expression ')'
| 'HOURS' '(' Expression ')'
| 'MINUTES' '(' Expression ')'
| 'SECONDS' '(' Expression ')'
| 'TIMEZONE' '(' Expression ')'
| 'TZ' '(' Expression ')'
| 'NOW' NIL
| 'UUID' NIL
| 'STRUUID' NIL
| 'MD5' '(' Expression ')'
| 'SHA1' '(' Expression ')'
| 'SHA256' '(' Expression ')'
| 'SHA384' '(' Expression ')'
| 'SHA512' '(' Expression ')'
| 'COALESCE' ExpressionList
| 'IF' '(' Expression ',' Expression ',' Expression ')'
| 'STRLANG' '(' Expression ',' Expression ')'
| 'STRDT' '(' Expression ',' Expression ')'
| 'sameTerm' '(' Expression ',' Expression ')'
| 'isIRI' '(' Expression ')'
| 'isURI' '(' Expression ')'
| 'isBLANK' '(' Expression ')'
| 'isLITERAL' '(' Expression ')'
| 'isNUMERIC' '(' Expression ')'
| RegexExpression
| ExistsFunc
| NotExistsFunc
[122]  	RegexExpression	  ::=  	'REGEX' '(' Expression ',' Expression ( ',' Expression )? ')'
[123]  	SubstringExpression	  ::=  	'SUBSTR' '(' Expression ',' Expression ( ',' Expression )? ')'
[124]  	StrReplaceExpression	  ::=  	'REPLACE' '(' Expression ',' Expression ',' Expression ( ',' Expression )? ')'
[125]  	ExistsFunc	  ::=  	'EXISTS' GroupGraphPattern
[126]  	NotExistsFunc	  ::=  	'NOT' 'EXISTS' GroupGraphPattern
[127]  	Aggregate	  ::=  	  'COUNT' '(' 'DISTINCT'? ( '*' | Expression ) ')'
| 'SUM' '(' 'DISTINCT'? Expression ')'
| 'MIN' '(' 'DISTINCT'? Expression ')'
| 'MAX' '(' 'DISTINCT'? Expression ')'
| 'AVG' '(' 'DISTINCT'? Expression ')'
| 'SAMPLE' '(' 'DISTINCT'? Expression ')'
| 'GROUP_CONCAT' '(' 'DISTINCT'? Expression ( ';' 'SEPARATOR' '=' String )? ')'
[128]  	iriOrFunction	  ::=  	iri ArgList?
[129]  	RDFLiteral	  ::=  	String ( LANGTAG | ( '^^' iri ) )?
[130]  	NumericLiteral	  ::=  	NumericLiteralUnsigned | NumericLiteralPositive | NumericLiteralNegative
[131]  	NumericLiteralUnsigned	  ::=  	INTEGER | DECIMAL | DOUBLE
[132]  	NumericLiteralPositive	  ::=  	INTEGER_POSITIVE | DECIMAL_POSITIVE | DOUBLE_POSITIVE
[133]  	NumericLiteralNegative	  ::=  	INTEGER_NEGATIVE | DECIMAL_NEGATIVE | DOUBLE_NEGATIVE
[134]  	BooleanLiteral	  ::=  	'true' | 'false'
[135]  	String	  ::=  	STRING_LITERAL1 | STRING_LITERAL2 | STRING_LITERAL_LONG1 | STRING_LITERAL_LONG2
[136]  	iri	  ::=  	IRIREF | PrefixedName
[137]  	PrefixedName	  ::=  	PNAME_LN | PNAME_NS
[138]  	BlankNode	  ::=  	BLANK_NODE_LABEL | ANON
"""
"""
Productions for terminals:

[139]  	IRIREF	  ::=  	'<' ([^<>"{}|^`\]-[#x00-#x20])* '>'
[140]  	PNAME_NS	  ::=  	PN_PREFIX? ':'
[141]  	PNAME_LN	  ::=  	PNAME_NS PN_LOCAL
[142]  	BLANK_NODE_LABEL	  ::=  	'_:' ( PN_CHARS_U | [0-9] ) ((PN_CHARS|'.')* PN_CHARS)?
[143]  	VAR1	  ::=  	'?' VARNAME
[144]  	VAR2	  ::=  	'$' VARNAME
[145]  	LANGTAG	  ::=  	'@' [a-zA-Z]+ ('-' [a-zA-Z0-9]+)*
[146]  	INTEGER	  ::=  	[0-9]+
[147]  	DECIMAL	  ::=  	[0-9]* '.' [0-9]+
[148]  	DOUBLE	  ::=  	[0-9]+ '.' [0-9]* EXPONENT | '.' ([0-9])+ EXPONENT | ([0-9])+ EXPONENT
[149]  	INTEGER_POSITIVE	  ::=  	'+' INTEGER
[150]  	DECIMAL_POSITIVE	  ::=  	'+' DECIMAL
[151]  	DOUBLE_POSITIVE	  ::=  	'+' DOUBLE
[152]  	INTEGER_NEGATIVE	  ::=  	'-' INTEGER
[153]  	DECIMAL_NEGATIVE	  ::=  	'-' DECIMAL
[154]  	DOUBLE_NEGATIVE	  ::=  	'-' DOUBLE
[155]  	EXPONENT	  ::=  	[eE] [+-]? [0-9]+
[156]  	STRING_LITERAL1	  ::=  	"'" ( ([^#x27#x5C#xA#xD]) | ECHAR )* "'"
[157]  	STRING_LITERAL2	  ::=  	'"' ( ([^#x22#x5C#xA#xD]) | ECHAR )* '"'
[158]  	STRING_LITERAL_LONG1	  ::=  	"'''" ( ( "'" | "''" )? ( [^'\] | ECHAR ) )* "'''"
[159]  	STRING_LITERAL_LONG2	  ::=  	'" ""' ( ( '"' | '""' )? ( [^"\] | ECHAR ) )* '" ""'
[160]  	ECHAR	  ::=  	'\' [tbnrf\"']
[161]  	NIL	  ::=  	'(' WS* ')'
[162]  	WS	  ::=  	#x20 | #x9 | #xD | #xA
[163]  	ANON	  ::=  	'[' WS* ']'
[164]  	PN_CHARS_BASE	  ::=  	[A-Z] | [a-z] | [#x00C0-#x00D6] | [#x00D8-#x00F6] | [#x00F8-#x02FF] | [#x0370-#x037D] | [#x037F-#x1FFF] | [#x200C-#x200D] | [#x2070-#x218F] | [#x2C00-#x2FEF] | [#x3001-#xD7FF] | [#xF900-#xFDCF] | [#xFDF0-#xFFFD] | [#x10000-#xEFFFF]
[165]  	PN_CHARS_U	  ::=  	PN_CHARS_BASE | '_'
[166]  	VARNAME	  ::=  	( PN_CHARS_U | [0-9] ) ( PN_CHARS_U | [0-9] | #x00B7 | [#x0300-#x036F] | [#x203F-#x2040] )*
[167]  	PN_CHARS	  ::=  	PN_CHARS_U | '-' | [0-9] | #x00B7 | [#x0300-#x036F] | [#x203F-#x2040]
[168]  	PN_PREFIX	  ::=  	PN_CHARS_BASE ((PN_CHARS|'.')* PN_CHARS)?
[169]  	PN_LOCAL	  ::=  	(PN_CHARS_U | ':' | [0-9] | PLX ) ((PN_CHARS | '.' | ':' | PLX)* (PN_CHARS | ':' | PLX) )?
[170]  	PLX	  ::=  	PERCENT | PN_LOCAL_ESC
[171]  	PERCENT	  ::=  	'%' HEX HEX
[172]  	HEX	  ::=  	[0-9] | [A-F] | [a-f]
[173]  	PN_LOCAL_ESC	  ::=  	'\' ( '_' | '~' | '.' | '-' | '!' | '$' | '&' | "'" | '(' | ')' | '*' | '+' | ',' | ';' | '=' | '/' | '?' | '#' | '@' | '%' )
"""
