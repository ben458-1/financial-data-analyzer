import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { User, Briefcase, Building } from "lucide-react"

// Mock data for demonstration
const mockData = {
  people_info: [
    {
      name: "Jane Smith",
      summary: "CEO of Tech Solutions Inc. with over 20 years of experience in the technology sector.",
      designation: "Chief Executive Officer",
      company: "Tech Solutions Inc.",
    },
    {
      name: "Mike Johnson",
      summary: "CTO responsible for leading the company's technological innovations and strategic direction.",
      designation: "Chief Technology Officer",
      company: "Tech Solutions Inc.",
    },
    {
      name: "Environmental Minister",
      summary: "Government official overseeing environmental regulations and sustainability initiatives.",
      designation: "Minister",
      company: "Department of Environmental Affairs",
    },
    {
      name: "Industry Leaders",
      summary: "Collective reference to executives and decision-makers across the technology sector.",
      designation: "Various",
      company: "Multiple Organizations",
    },
    {
      name: "Policy Makers",
      summary: "Government officials and regulators responsible for creating industry policies and regulations.",
      designation: "Various",
      company: "Government Agencies",
    },
  ],
}

export function PeopleInfoSection() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">People Information</CardTitle>
          <CardDescription>Details about people mentioned in the article</CardDescription>
        </CardHeader>
      </Card>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <User className="h-5 w-5 text-primary" />
            <CardTitle>People Mentioned</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {mockData.people_info.map((person, index) => (
              <div key={index} className="space-y-3">
                {index > 0 && <Separator />}
                <div className="pt-3">
                  <h3 className="text-lg font-medium">{person.name}</h3>
                  <div className="flex items-center gap-2 mt-1 text-sm text-gray-500 dark:text-gray-400">
                    <span className="flex items-center gap-1">
                      <Briefcase className="h-4 w-4" /> {person.designation}
                    </span>
                    <span className="flex items-center gap-1">
                      <Building className="h-4 w-4" /> {person.company}
                    </span>
                  </div>
                  <p className="mt-2 text-gray-700 dark:text-gray-300">{person.summary}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
