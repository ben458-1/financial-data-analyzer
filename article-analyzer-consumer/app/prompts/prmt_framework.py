from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class Author_Designation(BaseModel):
    current_designation: str = Field(
        ..., 
        description="Extract the author's current designation if mentioned. If currently they are not a full-time journalist, extract their actual job title. If not provided, return 'NA'."
    )
    past_designation: str = Field(
        ..., 
        description="Extract the past designation of the author, if not mentioned return as NA "
    )


class Author_Details(BaseModel):
    name: str = Field(
        ...,
        description = "Extract the name of the article's author/reporter"
    )
    comments: List[str] = Field(
        ...,
        description = "Extract only the author's commentary from the financial article. Retain their interpretation, criticism, praise, personal stance, predictions, contextual background, causal relationships, recommendations, synthesis, and ethical insights. Focus solely on the author's analysis, observations, and conclusions. Exclude all spokesperson quotes, source and third-party opinions."
    )
    
    designation: Author_Designation = Field(
        ...,
        description = "Designation of the author" 
    )
    organization: str


class People_Info(BaseModel):
    name: str = Field(
        ...,
        description = "Extract the full name of the person"
    )
    designation: str = Field(
        ...,
        description = "Extract the designation of the person"
    )
    company: str = Field(
        ...,
        description = "Extract the company of the person"
    )
    people_summary: str = Field(
        ...,
        description = "Brief individual summary of the person mentioned, explaining their role and context within the article."
    )


class Article_Details(BaseModel):
    article_keywords: List[str] = Field(
        ...,
        description = "Extract the main keywords in the article, that denote the topic of discussion."
    )
    people_info: List[People_Info] = Field(
        ...,
        description = "List of all the people mentioned in the article"
    )
    article_summary: str = Field(
        ...,
        description = "Summary of the article, capturing all essential information, key points, and context without omitting important details"
    )


class Comment_Date_Details(BaseModel):
    date: str = Field(
        ...,
        description = "Find the exact date the spokesperson/source has told the comment, if the date of the comment is not mentioned use NA. If the date is also abstract and not a proper date use NA"
    )
    abstract: str = Field(
        ...,
        description = "If the exact date is not present and abstract sentence is mentioned regarding the time of the comment, extract the abstract sentence for the time of the comment"
    )


class Spokesperson_Past(BaseModel):
    designation: str = Field(
        ...,
        description = """Past designation of the spokesperson"""
    )
    organization: str = Field(
        ...,
        description = """past organization of the spokesperson"""
    )
    no_of_years: int = Field(
        ...,
        description = """No of years the spokesperson has been in the previous organization"""
    )
    timeperiod: str = Field(
        ...,
        description="""The time-period from start to end the spokesperson worked on the previous organization, if it is not mentioned in the article use 0"""
    )
    location: str = Field(
        ...,
        description ="""The location of the previous organization"""
    )
    country: str = Field(
        ...,
        description = """The country in which the previous organization belonged to"""
    )


class Competitors_Mentioned(BaseModel):
    name: str = Field(
        ...,
        description = """Name of the competitors mentioned in the comment"""
    )
    conf_score: float = Field(
        description = """The confidence score of the competitor, give a value on how confident the name in the comment is a competitor"""
    )


class Spokesperson_Place(BaseModel):
    location: str = Field(
        ...,
        description="Extract the exact location mentioned in the article. This can be a city, region, landmark, or any specific place explicitly stated. If not mentioned, use 'NA'."
    )
    state: str = Field(
        ...,
        description="Extract the state or province explicitly mentioned in the article. If not mentioned, use 'NA'."
    )
    country: str = Field(
        ...,
        description="Extract the country name explicitly stated in the article.If not mentioned, use 'NA'."
    )


class Comment_Details(BaseModel):
    comment: str = Field(
        ...,
        description = """Extract only the FULL and EXACT comment (quote or opinion or statement) made by a spokesperson (named individuals like CEOs) or attributed to a source (analysts, managers, trusted individuals, "people with knowledge," etc.). Extract comments and statements of both direct and indirect speech. Do not include surrounding context, background information, or factual descriptions. Be brief and to the point."""
    )
    reasoning: str = Field(
        ...,
        description="""Explain your reasoning for extracting this specific comment and attributing it to this particular spokesperson or source. Why is this considered a direct comment/opinion? What words or phrases in the article led you to this conclusion?"""
    )
    reference_type: Literal['direct', 'indirect', 'NA'] = Field(
        description = """The reference type is an entity where in an article the spokesperson/source has quoted something in an old interview/press which is mentioned in this article, quoting it, if the old interview report/press release is relevant to the current context, the reference type is - direct, if the reference is not related to the current context then it is indirect reference. If there are no references in the article the value of reference type should be NA.
        Rules for Categorization of Reference Type
          Direct Reference:
 
          A past statement (from an interview, report, or event) is quoted and directly relevant to the article’s main discussion.
          The statement remains strategically important to the current context.
          Example: If an article discusses a company's innovation strategy and includes a past quote on innovation, it's a direct reference.
 
          Indirect Reference:
          
          A past statement is mentioned but does not directly support the article’s main discussion.
          Used for background or historical context, not influencing the current topic.
          Example: If an article discusses market expansion but includes an old quote about security, it's an indirect reference.
 
          NA (No Reference):
          A new statement made in the current press release, interview, or event.
          No mention of past reports, studies, or interviews.
          Example: A CEO announces a recent market growth in a new press conference.
        """
    )
    from_to: List[str] = Field(
        ...,
        description = """For this parameter, you will have to extract from and to. from- it is the person who is speaking. to- it is the target of the person, the person who is listening to.['from_person','to_person'] - follow this order. If there is no 'to' assume it to be author/reporter"""
    )
    comment_keywords: List[str] = Field(
        ...,
        description = """Keywords in a comment, Extract the key words from the comment. Keywords are the most repeating/important word. Generally keywords should denote the comment content."""
    )
    stakeholders_in_comment: List[str] = Field(
        ...,
        description = """Stakeholders mentioned in the comment. For every comment, list the stakeholders involved. Be specific to comment. Be very specific in extracting the stakeholders, there may be many stakeholders involved, extract the most relevant stakeholders alone, be more subjective."""
    )


class Extraction_Details(BaseModel):
    attribution: str = Field(
        ...,
        description="""Identify WHO is making the comment. If it's a named individual, use their FULL NAME from the article. If it's an unnamed source, use the phrase that indicates the source."""
    )
    attribution_type: Literal['spokesperson', 'source'] = Field(
        ...,
        description = """From the extracted comment classify wheter the comment is **from** a spokesperson or attributed source. In most cases only if the attribution is a name is, it will come under spokesperson. Note: any organization or company will come under attributed source"""
    )
    designation: str = Field(
        ...,
        description = """The current designation of the spokesperson or the source. Extract the present designation. If no designation is present, the designation value is NA any past or previous designations will be handled in another parameter spokesperson_past, in that case also use NA"""
    )
    organization: str = Field(
        ...,
        description = """The organization, company or group where the source or the spokesperson belongs to or works on"""
    )
    comment_details: List[Comment_Details]
    spokesperson_place: Spokesperson_Place = Field(
        ...,
        description = """The place of the spokesperson or the source"""
    )
    people_in_comment: List[str] = Field(
        ...,
        description = "Extract all people involved from the comment. If no people is mentioned use NA"
    )
    competitors_mentioned: List[Competitors_Mentioned] = Field(
        ...,
        description = "List of competitors mentioned in the comment"
    )
    spokesperson_past: Spokesperson_Past = Field(
        description = "Past details of the spokesperson"
    )
    spokesperson_summary: str = Field(
        ...,
        description = """For every spokesperson, extract the summary of all his comments. Make sure the context is understandable with alone the summary, if the summary is very abstract, add a little of context of the article which supports the comment."""
    )
    comment_date: Comment_Date_Details


class Comment_Extraction(BaseModel):
    extraction_details: List[Extraction_Details]
    article_details: Article_Details= Field(
        ...,
        description="""Details and metadata about the article."""
    )
    author_details: Author_Details = Field(
        ...,
        description="""Details about the article's author."""
    )
