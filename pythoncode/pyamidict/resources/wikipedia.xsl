<xsl:stylesheet xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>

    <xsl:template match="/">
            <xsl:apply-templates/>
    </xsl:template>

    <!-- identity -->
    <xsl:template match="node()|@*">
      <xsl:copy>
        <xsl:apply-templates select="node()|@*"/>
      </xsl:copy>
    </xsl:template>

    <xsl:template match="entry/@*">
        <xsl:choose>
        <xsl:when test="name()='id'"><xsl:attribute name="IDDDD"><xsl:value-of select="."/></xsl:attribute></xsl:when>
        <xsl:when test="name()='wikipedia'"><xsl:attribute name="wikipediaURL"><xsl:value-of select="."/></xsl:attribute></xsl:when>
        <xsl:when test="name()='wikidata'"><xsl:attribute name="wikidataID"><xsl:value-of select="."/></xsl:attribute></xsl:when>
        <xsl:when test="name()='wikipediaPage' or name()='description'"></xsl:when>
        <xsl:when test="starts-with(name(),'_p') or  starts-with(name(),'_q')"><xsl:value-of select="."/></xsl:when>
        <xsl:otherwise><xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute><xsl:message>UNKNOWN<xsl:value-of select="name()"/></xsl:message></xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="entry">
      <xsl:copy>
        <xsl:apply-templates select="node()|@*[not(name()='description')]"/>
        <xsl:if test="@description and not(description[@xml:lang='en'])"><description xml:lang="none"><xsl:value-of select="@description"/></description></xsl:if>
      </xsl:copy>
    </xsl:template>
</xsl:stylesheet>