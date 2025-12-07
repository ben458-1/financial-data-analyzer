import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { FileText, User, Users, Building, ExternalLink } from "lucide-react"
import Link from "next/link"

type SearchResult = {
  id: string
  header: string
  spokespersons: {
    name: string
    designation: string
    organization: string
  }[]
  author: string
  people_mentioned: string[]
  articleUrl: string
}

interface SearchResultsProps {
  results: SearchResult[]
}

export function SearchResults({ results }: SearchResultsProps) {
  return (
    <div className="space-y-4">
      {results.map((result) => (
        <Card key={result.id} className="overflow-hidden hover:shadow-md transition-shadow">
          <CardContent className="p-0">
            <Link href={`/article/${result.id}`} className="block">
              <div className="bg-gray-100 dark:bg-gray-800 p-4 cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
                <div className="flex items-center gap-2 mb-1">
                  <FileText className="h-5 w-5 text-primary" />
                  <h3 className="text-lg font-medium text-gray-800 dark:text-gray-100">{result.header}</h3>
                </div>
              </div>
            </Link>

            <div className="p-4 space-y-4">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <User className="h-4 w-4 text-primary" />
                  <h4 className="font-medium text-gray-700 dark:text-gray-300">Spokespersons</h4>
                </div>
                <div className="space-y-2">
                  {result.spokespersons.map((spokesperson, index) => (
                    <div key={index} className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-3">
                      <span className="text-gray-800 dark:text-gray-200">{spokesperson.name}</span>
                      <div className="flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400">
                        <span>{spokesperson.designation}</span>
                        <span>•</span>
                        <span className="flex items-center gap-1">
                          <Building className="h-3 w-3" /> {spokesperson.organization}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <Separator />

              <div className="flex flex-col sm:flex-row gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <User className="h-4 w-4 text-primary" />
                    <h4 className="font-medium text-gray-700 dark:text-gray-300">Author</h4>
                  </div>
                  <p className="text-gray-800 dark:text-gray-200">{result.author}</p>
                </div>

                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <Users className="h-4 w-4 text-primary" />
                    <h4 className="font-medium text-gray-700 dark:text-gray-300">People Mentioned</h4>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {result.people_mentioned.map((person, index) => (
                      <Badge key={index} variant="secondary">
                        {person}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>

              <Separator />

              <div>
                <a
                  href={result.articleUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 text-primary hover:underline"
                >
                  <ExternalLink className="h-4 w-4" />
                  <span>View Original Article</span>
                </a>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
