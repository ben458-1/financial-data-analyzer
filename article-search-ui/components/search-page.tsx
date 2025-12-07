"use client"

import type React from "react"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { SearchResults } from "@/components/search-results"
import { Search } from "lucide-react"

// Mock data for search results
const mockSearchResults = [
  {
    id: "1",
    header: "Tech Solutions Inc. Announces Revolutionary Product Line",
    spokespersons: [
      {
        name: "John Doe",
        designation: "Chief Marketing Officer",
        organization: "Tech Solutions Inc.",
      },
    ],
    author: "Alex Thompson",
    people_mentioned: ["Jane Smith", "Mike Johnson", "Environmental Minister"],
    articleUrl: "https://example.com/tech-solutions-product-line",
  },
  {
    id: "2",
    header: "Market Analysis: Sustainability Trends in Technology Sector",
    spokespersons: [
      {
        name: "Sarah Johnson",
        designation: "Industry Analyst",
        organization: "Market Research Group",
      },
      {
        name: "Robert Chen",
        designation: "Sustainability Director",
        organization: "Green Tech Alliance",
      },
    ],
    author: "Maria Rodriguez",
    people_mentioned: ["Environmental Minister", "Industry Leaders", "Policy Makers"],
    articleUrl: "https://example.com/sustainability-trends",
  },
  {
    id: "3",
    header: "Quarterly Earnings Report Shows 30% Growth for Tech Solutions",
    spokespersons: [
      {
        name: "Jane Smith",
        designation: "Chief Executive Officer",
        organization: "Tech Solutions Inc.",
      },
      {
        name: "David Wilson",
        designation: "Chief Financial Officer",
        organization: "Tech Solutions Inc.",
      },
    ],
    author: "Alex Thompson",
    people_mentioned: ["Board Members", "Investors", "Market Analysts"],
    articleUrl: "https://example.com/quarterly-earnings",
  },
  {
    id: "4",
    header: "Industry Leaders Gather for Annual Tech Summit",
    spokespersons: [
      {
        name: "Mike Johnson",
        designation: "Chief Technology Officer",
        organization: "Tech Solutions Inc.",
      },
      {
        name: "Lisa Wong",
        designation: "Innovation Director",
        organization: "Future Technologies",
      },
    ],
    author: "James Peterson",
    people_mentioned: ["Tech Executives", "Startup Founders", "Venture Capitalists"],
    articleUrl: "https://example.com/tech-summit",
  },
  {
    id: "5",
    header: "New Regulations to Impact Technology Manufacturing",
    spokespersons: [
      {
        name: "Environmental Minister",
        designation: "Minister",
        organization: "Department of Environmental Affairs",
      },
      {
        name: "Industry Association Spokesperson",
        designation: "Communications Director",
        organization: "Tech Industry Association",
      },
    ],
    author: "Sophia Chen",
    people_mentioned: ["Regulatory Officials", "Manufacturing Executives", "Environmental Experts"],
    articleUrl: "https://example.com/new-regulations",
  },
]

export function SearchPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [results, setResults] = useState<typeof mockSearchResults | null>(null)
  const [isSearching, setIsSearching] = useState(false)

  const handleSearch = () => {
    if (!searchQuery.trim()) return

    setIsSearching(true)

    // Simulate API call with setTimeout
    setTimeout(() => {
      setResults(mockSearchResults)
      setIsSearching(false)
    }, 500)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSearch()
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col items-center justify-center">
      <div className="container mx-auto px-4 max-w-4xl">
        <Card className="shadow-lg border-0">
          <CardContent className="pt-6 pb-6">
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                <Input
                  placeholder="Search for spokesperson, organization, or person..."
                  className="pl-10 h-12 text-lg"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={handleKeyDown}
                />
              </div>
              <Button className="h-12 px-6" onClick={handleSearch} disabled={isSearching || !searchQuery.trim()}>
                {isSearching ? "Searching..." : "Search"}
              </Button>
            </div>
          </CardContent>
        </Card>

        {results && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-100">
              Top Results for "{searchQuery}"
            </h2>
            <SearchResults results={results} />
          </div>
        )}
      </div>
    </main>
  )
}
