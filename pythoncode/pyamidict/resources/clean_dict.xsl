<xsl:stylesheet xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>

<!-- root -->
    <xsl:template match="/">
            <xsl:apply-templates/>
    </xsl:template>

    <!-- identity , copyn everything -->
    <xsl:template match="node()|@*">
        <xsl:junk/>
      <xsl:copy>
        <xsl:apply-templates select="node()|@*"/>
      </xsl:copy>
    </xsl:template>

    <!-- 'desc' obsolete; transform to 'metadata' -->
    <xsl:template match="desc">
      <xsl:copy>
        <xsl:apply-templates select="node()|@*[not(name()='description')]"/>
        <xsl:if test="@description and not(description[@xml:lang='en'])"><description xml:lang="en"><xsl:value-of select="@description"/></description></xsl:if>
      </xsl:copy>
    </xsl:template>

    <!-- entry 
     transform @description to en-child
     attributes treated separately
     -->
    <xsl:template match="entry">
        <xsl:junk/>
      <xsl:copy>
        <!-- transfer @description to child with language attribute -->
<!--        <xsl:apply-templates select="@*[not(name()='description')]"/> -->
        <xsl:if test="@description and not(description[@xml:lang='en'])"><description xml:lang="en"><xsl:value-of select="@description"/></description></xsl:if>
          <!-- terms in languages -->
        <xsl:if test="@French"><synonym xml:lang="fr"><xsl:value-of select="@French"/></synonym></xsl:if>
        <xsl:if test="@German"><synonym xml:lang="de"><xsl:value-of select="@Germa"/></synonym></xsl:if>
        <xsl:if test="@Hausa"><synonym xml:lang="ha"><xsl:value-of select="@Hausa"/></synonym></xsl:if>
        <xsl:if test="@Hindi"><synonym xml:lang="hi"><xsl:value-of select="@Hindi"/></synonym></xsl:if>
        <xsl:if test="@Sanskrit"><synonym xml:lang="sa"><xsl:value-of select="@Sanskrit"/></synonym></xsl:if>
        <xsl:if test="@Spanish"><synonym xml:lang="es"><xsl:value-of select="@Spanish"/></synonym></xsl:if>
        <xsl:if test="@Tamil"><synonym xml:lang="ta"><xsl:value-of select="@Tamil"/></synonym></xsl:if>
        <xsl:if test="@Urdu"><synonym xml:lang="ur"><xsl:value-of select="@Urdu"/></synonym></xsl:if>

                    <!-- terms in languages -->
        <xsl:if test="@French_description"><description xml:lang="fr"><xsl:value-of select="@French"/></description></xsl:if>
        <xsl:if test="@German_description"><description xml:lang="de"><xsl:value-of select="@Germa"/></description></xsl:if>
        <xsl:if test="@Hausa_description"><description xml:lang="ha"><xsl:value-of select="@Hausa"/></description></xsl:if>
        <xsl:if test="@Hindi_description"><description xml:lang="hi"><xsl:value-of select="@Hindi"/></description></xsl:if>
        <xsl:if test="@Sanskrit_description"><description xml:lang="sa"><xsl:value-of select="@Sanskrit"/></description></xsl:if>
        <xsl:if test="@Spanish_description"><description xml:lang="es"><xsl:value-of select="@Spanish"/></description></xsl:if>
        <xsl:if test="@Tamil_description"><description xml:lang="ta"><xsl:value-of select="@Tamil"/></description></xsl:if>
        <xsl:if test="@Urdu_description"><description xml:lang="ur"><xsl:value-of select="@Urdu"/></description></xsl:if>

        <xsl:apply-templates select="node()"/>
      </xsl:copy>
    </xsl:template>

    <!--
    'Sanskrit', 'Hindi', 'Hausa', 'Hindi_description', 'Spanish_description', 'Tamil_description', 'German_description',
    'Tamil', 'formulae', 'Urdu', 'Urdu_description', 'altNames', 'picture', 'Spanish', 'Portuguese', 'German',
    'Portuguese_description'
    -->
    <xsl:template match="entry/@*">
        <xsl:junk/>
        <xsl:choose>
            <xsl:when test="name()='id'"><xsl:attribute name="id"><xsl:value-of select="."/></xsl:attribute></xsl:when>
            <xsl:when test="name()='wikipedia'"><xsl:attribute name="wikipediaURL"><xsl:value-of select="."/></xsl:attribute></xsl:when>
            <xsl:when test="name()='wikidata'"><xsl:attribute name="wikidataID"><xsl:value-of select="."/></xsl:attribute></xsl:when>
            <xsl:when test="starts-with(name(),'_p') or  starts-with(name(),'_q')"><xsl:value-of select="."/></xsl:when>
            <!-- obsolete  -->

            <xsl:when test="
                   false()
                or name()='altNames'
                or name()='formulae'
                or name()='picture'
                or name()='wikipediaPage'
            ">DELETE</xsl:when>
            <!-- move to children; see template for 'entry'-->
            <xsl:when test="
                   name()='French_description'
                or name()='German_description'
                or name()='Hausa_description'
                or name()='Hindi_description'
                or name()='Portuguese_description'
                or name()='Sanskrit_description'
                or name()='Spanish_description'
                or name()='Tamil_description'
                or name()='Urdu_description'
                "><!--DELETE--></xsl:when>
            <xsl:when test="
                   false()
                or name()='French'
                or name()='German'
                or name()='Hausa'
                or name()='Hindi'
                or name()='Portuguese'
                or name()='Sanskrit'
                or name()='Spanish'
                or name()='Tamil'
                or name()='Urdu'
                ">DELETE</xsl:when>
            <xsl:otherwise><xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute>
<!--                <xsl:message>UNKNOWN<xsl:value-of select="name()"/></xsl:message>-->
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="junk">
        <xsl:junk/>
    </xsl:template>

</xsl:stylesheet>