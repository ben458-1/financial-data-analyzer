import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { FileText, Tag } from "lucide-react"

// Mock data for demonstration
const mockData = {
  article_keywords: [
    "technology",
    "innovation",
    "market growth",
    "sustainability",
    "digital transformation",
    "industry trends",
  ],
  article_summary:
    "This article discusses the recent technological innovations in the industry and how companies are adapting to new market demands. It highlights the growth of Tech Solutions Inc. and their new product line, while also touching on sustainability practices being adopted across the sector. The piece includes insights from key executives and industry analysts about future trends and challenges.",
}

export function ArticleSection() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Article Details</CardTitle>
          <CardDescription>Summary and key information extracted from the article</CardDescription>
        </CardHeader>
      </Card>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <FileText className="h-5 w-5 text-primary" />
            <CardTitle>Article Summary</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">{mockData.article_summary}</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Tag className="h-5 w-5 text-primary" />
            <CardTitle>Keywords</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {mockData.article_keywords.map((keyword, index) => (
              <Badge key={index} variant="secondary">
                {keyword}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
