import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { User, Briefcase, Calendar, MessageSquare, Tag, Users } from "lucide-react"

// Mock data for demonstration - only sources
const mockData = {
  extraction_details: [
    {
      designation: "Industry Analyst",
      organization: "Market Research Group",
      comment_details: [
        {
          comment: "The new developments in this sector indicate a shift towards more sustainable practices.",
          reasoning: "Analysis of industry trends",
          reference_type: "indirect",
          from_to: ["research report", "public"],
          comment_keywords: ["sustainability", "industry trends", "development"],
          stakeholders_in_comment: ["industry players", "regulators"],
        },
      ],
      people_in_comment: ["Environmental Minister", "Industry Leaders"],
      competitors_mentioned: [],
      comment_date: {
        date: "2023-06-02",
        abstract: "In a published industry report",
      },
    },
    {
      designation: "Sustainability Director",
      organization: "Green Tech Alliance",
      comment_details: [
        {
          comment:
            "Companies that adopt sustainable practices now will have a competitive advantage in the future market.",
          reasoning: "Expert opinion on sustainability",
          reference_type: "direct",
          from_to: ["interview", "media"],
          comment_keywords: ["sustainability", "competitive advantage", "future market"],
          stakeholders_in_comment: ["companies", "investors", "consumers"],
        },
      ],
      people_in_comment: ["Industry Leaders", "Policy Makers"],
      competitors_mentioned: [
        {
          name: "Eco Solutions",
          conf_score: 0.78,
        },
        {
          name: "Green Innovations",
          conf_score: 0.65,
        },
      ],
      comment_date: {
        date: "2023-05-28",
        abstract: "During a panel discussion on sustainability",
      },
    },
  ],
}

export function SourceSection() {
  // Filter to only show sources
  const sources = mockData.extraction_details

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Source Details</CardTitle>
          <CardDescription>Information about sources mentioned in the article</CardDescription>
        </CardHeader>
      </Card>

      {sources.map((detail, index) => (
        <Card key={index} className="overflow-hidden">
          <CardHeader className="bg-gray-100 dark:bg-gray-800">
            <div className="flex items-center gap-2">
              <User className="h-5 w-5 text-primary" />
              <CardTitle>{detail.designation}</CardTitle>
            </div>
            <div className="flex items-center gap-2 mt-2">
              <span className="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1">
                <Briefcase className="h-4 w-4" /> {detail.organization}
              </span>
            </div>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="flex-1">
                  <h3 className="text-lg font-medium mb-2 flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-primary" /> Comment Date
                  </h3>
                  <p className="text-gray-700 dark:text-gray-300">{detail.comment_date.date}</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">{detail.comment_date.abstract}</p>
                </div>
              </div>

              <Separator />

              <div>
                <h3 className="text-lg font-medium mb-2 flex items-center gap-2">
                  <MessageSquare className="h-4 w-4 text-primary" /> Comments
                </h3>
                <Accordion type="single" collapsible className="w-full">
                  {detail.comment_details.map((comment, commentIndex) => (
                    <AccordionItem key={commentIndex} value={`comment-${commentIndex}`}>
                      <AccordionTrigger className="text-left">
                        <div className="truncate max-w-[600px]">{comment.comment.substring(0, 60)}...</div>
                      </AccordionTrigger>
                      <AccordionContent>
                        <div className="space-y-3 p-2">
                          <p className="text-gray-700 dark:text-gray-300">{comment.comment}</p>

                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                            <div>
                              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Reference Type</p>
                              <Badge variant="outline">{comment.reference_type}</Badge>
                            </div>
                            <div>
                              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">From/To</p>
                              <div className="flex flex-wrap gap-2 mt-1">
                                {comment.from_to.map((item, i) => (
                                  <Badge key={i} variant="secondary">
                                    {item}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                            <div>
                              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Keywords</p>
                              <div className="flex flex-wrap gap-2 mt-1">
                                {comment.comment_keywords.map((keyword, i) => (
                                  <Badge key={i} variant="outline" className="bg-gray-100 dark:bg-gray-800">
                                    <Tag className="h-3 w-3 mr-1" /> {keyword}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                            <div>
                              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Stakeholders</p>
                              <div className="flex flex-wrap gap-2 mt-1">
                                {comment.stakeholders_in_comment.map((stakeholder, i) => (
                                  <Badge key={i} variant="outline" className="bg-gray-100 dark:bg-gray-800">
                                    <Users className="h-3 w-3 mr-1" /> {stakeholder}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>
                      </AccordionContent>
                    </AccordionItem>
                  ))}
                </Accordion>
              </div>

              {detail.people_in_comment.length > 0 && (
                <>
                  <Separator />
                  <div>
                    <h3 className="text-lg font-medium mb-2 flex items-center gap-2">
                      <Users className="h-4 w-4 text-primary" /> People Mentioned in Comments
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {detail.people_in_comment.map((person, i) => (
                        <Badge key={i} variant="secondary">
                          {person}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </>
              )}

              {detail.competitors_mentioned && detail.competitors_mentioned.length > 0 && (
                <>
                  <Separator />
                  <div>
                    <h3 className="text-lg font-medium mb-2">Competitors Mentioned</h3>
                    <div className="space-y-2">
                      {detail.competitors_mentioned.map((competitor, i) => (
                        <div key={i} className="flex items-center justify-between">
                          <span>{competitor.name}</span>
                          <Badge variant="outline">Confidence: {(competitor.conf_score * 100).toFixed(0)}%</Badge>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
