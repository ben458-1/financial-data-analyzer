import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { User, Briefcase, MapPin, Calendar, MessageSquare, History } from "lucide-react"

// Mock data for demonstration - only spokespersons
const mockData = {
  extraction_details: [
    {
      attribution: "John Doe",
      attribution_type: "spokesperson",
      designation: "Chief Marketing Officer",
      organization: "Tech Solutions Inc.",
      comment_details: [
        {
          comment: "We are excited to announce our new product line that will revolutionize the industry.",
          reasoning: "Promoting new product launch",
          reference_type: "direct",
          from_to: ["press release", "media"],
          comment_keywords: ["product launch", "innovation", "industry"],
          stakeholders_in_comment: ["customers", "investors"],
        },
        {
          comment: "The company has seen a 30% growth in the last quarter.",
          reasoning: "Sharing company performance",
          reference_type: "direct",
          from_to: ["interview", "public"],
          comment_keywords: ["growth", "performance", "quarter"],
          stakeholders_in_comment: ["investors", "analysts"],
        },
      ],
      spokesperson_place: {
        location: "Silicon Valley",
        state: "California",
        country: "USA",
      },
      people_in_comment: ["CEO Jane Smith", "CTO Mike Johnson"],
      spokesperson_past: {
        designation: "Marketing Director",
        organization: "Digital Innovations",
        no_of_years: 5,
        timeperiod: "2015-2020",
        location: "Boston",
        country: "USA",
      },
      spokesperson_summary: "John Doe is an experienced marketing executive with over 10 years in the tech industry.",
      comment_date: {
        date: "2023-05-15",
        abstract: "During the quarterly earnings call",
      },
    },
    {
      attribution: "Jane Smith",
      attribution_type: "spokesperson",
      designation: "Chief Executive Officer",
      organization: "Tech Solutions Inc.",
      comment_details: [
        {
          comment: "Our vision is to lead the industry in innovation and sustainable practices.",
          reasoning: "Company vision statement",
          reference_type: "direct",
          from_to: ["interview", "media"],
          comment_keywords: ["vision", "innovation", "sustainability"],
          stakeholders_in_comment: ["employees", "investors", "customers"],
        },
      ],
      spokesperson_place: {
        location: "Silicon Valley",
        state: "California",
        country: "USA",
      },
      people_in_comment: ["CTO Mike Johnson", "Board Members"],
      spokesperson_past: {
        designation: "COO",
        organization: "Tech Innovations Ltd",
        no_of_years: 7,
        timeperiod: "2010-2017",
        location: "New York",
        country: "USA",
      },
      spokesperson_summary: "Jane Smith is the visionary CEO who has led Tech Solutions Inc. to record growth.",
      comment_date: {
        date: "2023-06-10",
        abstract: "At the annual shareholders meeting",
      },
    },
  ],
}

export function SpokespersonSection() {
  // Filter to only show spokespersons
  const spokespersons = mockData.extraction_details

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Spokesperson Details</CardTitle>
          <CardDescription>Information about spokespersons mentioned in the article</CardDescription>
        </CardHeader>
      </Card>

      {spokespersons.map((detail, index) => (
        <Card key={index} className="overflow-hidden">
          <CardHeader className="bg-gray-100 dark:bg-gray-800">
            <div className="flex items-center gap-2">
              <User className="h-5 w-5 text-primary" />
              <CardTitle>{detail.attribution}</CardTitle>
            </div>
            <div className="flex items-center gap-2 mt-2">
              <Badge variant="default">{detail.attribution_type}</Badge>
              <span className="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1">
                <Briefcase className="h-4 w-4" /> {detail.designation} at {detail.organization}
              </span>
            </div>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-medium mb-2">Summary</h3>
                <p className="text-gray-700 dark:text-gray-300">{detail.spokesperson_summary}</p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <div className="flex-1">
                  <h3 className="text-lg font-medium mb-2 flex items-center gap-2">
                    <MapPin className="h-4 w-4 text-primary" /> Location
                  </h3>
                  <p className="text-gray-700 dark:text-gray-300">
                    {detail.spokesperson_place.location}, {detail.spokesperson_place.state},{" "}
                    {detail.spokesperson_place.country}
                  </p>
                </div>

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
                  <History className="h-4 w-4 text-primary" /> Past Experience
                </h3>
                <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded-md">
                  <div className="flex flex-col sm:flex-row gap-4">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Previous Role</p>
                      <p className="text-gray-700 dark:text-gray-300">
                        {detail.spokesperson_past.designation} at {detail.spokesperson_past.organization}
                      </p>
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Duration</p>
                      <p className="text-gray-700 dark:text-gray-300">
                        {detail.spokesperson_past.no_of_years} years ({detail.spokesperson_past.timeperiod})
                      </p>
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Location</p>
                      <p className="text-gray-700 dark:text-gray-300">
                        {detail.spokesperson_past.location}, {detail.spokesperson_past.country}
                      </p>
                    </div>
                  </div>
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
                          </div>
                        </div>
                      </AccordionContent>
                    </AccordionItem>
                  ))}
                </Accordion>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
