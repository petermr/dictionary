### PMR's summary of 20210703's meeting
Shweata and PMR had a long session yesterday - initially looking at automatically extracting entities AND their context from boilerplate, of the form:
<ACTION> by <ORGANIZATION> [with <QUALIFICATIONS>]
If we are looking at the 1-2 sentence ethics statements, especially where they are cut and paste for a group, this will probably work quite well. We wanted to get away from solely Frontiers so we had a brief look at PLOSOne , with "stem cells AND clinical trials". This showed that many ethics statements were included in "Study Design" which is a 2-3 paragraph section.  

These Study Designs will be richer in content and much more similar to the ChemicalTagger that Lezan Hawizy and I developed 10 years ago. That will be a significant amount of work - at least weeks - even with modern tools. So we need to define a tightly-specified set of goals.

It comes back to the fundamental fact that we have to do human document analysis - hopefully machine-assisted - to scope our problem.

PMR's suggestions:
* we hypothesize that a study design is made up of boilerplate sentences and specific details. 
* We hypothesize that the boilerplate is restricted to individual sentences. 
* We only analyze the boilerplate.
* we hypothesize that we three can create a smallish semantic-ontological framework for the boilerplate. 
* we classify sentences according to this ontology and build a classifier. This may either be trained by ML or depend on rules, including entity recognition (I'd prefer this as it adds more value and is more understandable)
* we decide on a small number of classes which are (a) interesting (b) easily tractable.
* we will have discovered the set of tools which will help us. This will include annotation, which will be a major means of outreach.

So here's an example - which we should really do on a wiki. It's randomly taken as the first non-review article that PLOSOne gives for "stem cells AND clinical trials. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0120474. I'll break it up by sentences:

```
This research was approved by the University of Southern California Health Sciences Institutional Review Board. This was a nested retrospective study within the Pediatric AIDS Clinical Trials Group (PACTG) Protocol 366 (ACTG 366). ACTG 366 enrollment occurred between May 1998 and January 2000 at 50 participating sites in the US and Puerto Rico. Written informed consents from the next of kin, caretakers, or guardians were obtained on behalf of the minors and children enrolled in the study, including written assent according to local institutional review board guidelines. Patient records and information were anonymized and de-identified prior to analysis. ACTG 366 is registered with ClinicalTrials.gov under the following registration number: NCT00000902.

ACTG 366 enrolled PHIV+ ART-experienced participants 6 months to 21 years old with severe disease defined as having HIV-1 plasma viral load (VL) >50,000 copies/mL; CD4+ count <200 cells/mm3, CD4% <15, or a 50% reduction in CD4% within 24 weeks of the start of the current ART regimen; growth failure; or CNS disease. Participants started a new cART regimen according to a pre-defined algorithm as previously described [11]. HIV VL and CD4/CD8 cell counts were measured at baseline, monthly for the first six months and bimonthly thereafter. Advanced T-cell phenotyping and CMV cell-mediated immunity (CMI) assays were performed at baseline and weeks 12, 20 and 40. All assays were performed at PACTG-certified laboratories.

Our analysis included participants older than one year; who had baseline plasma samples available for CMV testing; and had baseline data available for at least one of the T-cell phenotypes of interest. Virology and immunology testing was performed in National Institutes of Health, Division of AIDS (DAIDS) approved laboratories that participated in viral and immunology quality assurance programs.
```

Now the analysis split at sentence level, or subsentence 
```
This research was approved by the University of Southern California Health Sciences Institutional Review Board.
```

 APPROVALBY <body>
```
This was a nested retrospective study within the Pediatric AIDS Clinical Trials Group (PACTG) Protocol 366 (ACTG 366).
```
STUDYTYPE <studygroup> <protocol> 
```
ACTG 366 enrollment occurred between May 1998 and January 2000 at 50 participating sites in the US and Puerto Rico.
```
ENROLMENT <enrol-id> <date-range> <sites> <countries> 
```
Written informed consents from the next of kin, caretakers, or guardians were obtained on behalf of the minors and children enrolled in the study, including written assent according to local institutional review board guidelines.
```

INFORMED_CONSENT <consenters> <consentees> CONSENT_TYPE written REGULATION <regulations>
```
 Patient records and information were anonymized and de-identified prior to analysis.
```
ANONYMTY <information_type> <procedure> < times>
```
ACTG 366 is registered with ClinicalTrials.gov under the following registration number: NCT00000902.
```

REGISTRATION <group> <authority> <id>

PARA
```
ACTG 366 enrolled PHIV+ ART-experienced participants 6 months to 21 years old with severe disease defined as having HIV-1 plasma viral load (VL) >50,000 copies/mL; CD4+ count <200 cells/mm3, CD4% <15, or a 50% reduction in CD4% within 24 weeks of the start of the current ART regimen; growth failure; or CNS disease.
```
<EXPT_PARAMS >
```
Participants started a new cART regimen according to a pre-defined algorithm as previously described [11].
```
 <EXPT_PARAMS>
``` 
HIV VL and CD4/CD8 cell counts were measured at baseline, monthly for the first six months and bimonthly thereafter. Advanced T-cell phenotyping and CMV cell-mediated immunity (CMI) assays were performed at baseline and weeks 12, 20 and 40.
```
<EXPT_DATA>
``` 
All assays were performed at PACTG-certified laboratories.
```
PROTOCOL <authorization>
 
PARA 
```
Our analysis included participants older than one year; who had baseline plasma samples available for CMV testing; and had baseline data available for at least one of the T-cell phenotypes of interest.
```
EXPT_PARAMS
``` 
Virology and immunology testing was performed in National Institutes of Health, Division of AIDS (DAIDS) approved laboratories that participated in viral and immunology quality assurance programs.
```
PROTOCOL <authorization>
  
The last two paras are either too complex or subsidiary to the main goal. So here we have 6 sentences. Daniel should suggest which are critical. I'll assume all to start with.

So the goal would be to split into sentences and classify their type and devise an ontology/template structure. My guess is that there will be about 10 categories of sentences. 

APPROVAL_BY <body>
STUDY_TYPE <studygroup> <protocol> 
ENROLMENT <enrol-id> <date-range> <sites> <countries> 
INFORMED_CONSENT <consenters> <consentees> 
CONSENT_TYPE written REGULATION <regulations>
ANONYMITY <information_type> <procedure> < times>
REGISTRATION <group> <authority> <id>

 The main challenge is deciding on the analysis. We probably need to go to PRISMA or other authorities to see how they specify the boilerplate

The immediate questions are:
* which of the extracted statements are critical?
* what entities/data do we wish to extract?
* how many different sources do we need to examine?

This is do-able but certainly not trivial. When we have decided what we want to do we should examine the toolset. 

