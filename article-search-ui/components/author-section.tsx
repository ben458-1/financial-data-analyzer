import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Separator } from "@/components/ui/separator"
import { User, Briefcase, Building, MessageSquare, History } from "lucide-react"

// Mock data for demonstration
const mockData = {
  name: "Alex Thompson",
  comments: [
    "The technological landscape is rapidly evolving, with companies racing to adapt to new market demands.",
    "While Tech Solutions Inc. leads in innovation, questions remain about the long-term sustainability of their approach.",
    "Industry analysts suggest that the next quarter will be crucial for determining market leaders in this space.",
  ],
  designation: {
    current_designation: "Senior Technology Reporter",
    past_designation: "Technology Correspondent",
  },
  organization: "Global Tech News",
}

export function AuthorSection() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Author Details</CardTitle>
          <CardDescription>Information about the article's author</CardDescription>
        </CardHeader>
      </Card>

      <Card>
        <CardHeader className="bg-gray-100 dark:bg-gray-800">
          <div className="flex items-center gap-2">
            <User className="h-5 w-5 text-primary" />
            <CardTitle>{mockData.name}</CardTitle>
          </div>
          <div className="flex items-center gap-2 mt-2 text-sm text-gray-500 dark:text-gray-400">
            <span className="flex items-center gap-1">
              <Briefcase className="h-4 w-4" /> {mockData.designation.current_designation}
            </span>
            <span className="flex items-center gap-1">
              <Building className="h-4 w-4" /> {mockData.organization}
            </span>
          </div>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium mb-2 flex items-center gap-2">
                <History className="h-4 w-4 text-primary" /> Career History
              </h3>
              <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-md">
                <div className="flex flex-col sm:flex-row gap-4">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Current Position</p>
                    <p className="text-gray-700 dark:text-gray-300">{mockData.designation.current_designation}</p>
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Previous Position</p>
                    <p className="text-gray-700 dark:text-gray-300">{mockData.designation.past_designation}</p>
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Organization</p>
                    <p className="text-gray-700 dark:text-gray-300">{mockData.organization}</p>
                  </div>
                </div>
              </div>
            </div>

            <Separator />

            <div>
              <h3 className="text-lg font-medium mb-2 flex items-center gap-2">
                <MessageSquare className="h-4 w-4 text-primary" /> Author Comments
              </h3>
              <Accordion type="single" collapsible className="w-full">
                {mockData.comments.map((comment, index) => (
                  <AccordionItem key={index} value={`comment-${index}`}>
                    <AccordionTrigger className="text-left">
                      <div className="truncate max-w-[600px]">{comment.substring(0, 60)}...</div>
                    </AccordionTrigger>
                    <AccordionContent>
                      <p className="text-gray-700 dark:text-gray-300 p-2">{comment}</p>
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
