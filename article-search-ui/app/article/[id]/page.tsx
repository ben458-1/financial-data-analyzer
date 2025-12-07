import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { SpokespersonSection } from "@/components/spokesperson-section"
import { SourceSection } from "@/components/source-section"
import { ArticleSection } from "@/components/article-section"
import { AuthorSection } from "@/components/author-section"
import { PeopleInfoSection } from "@/components/people-info-section"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Button } from "@/components/ui/button"
import { ArrowLeft } from "lucide-react"
import Link from "next/link"

export default function ArticleParserPage({ params }: { params: { id: string } }) {
  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="container mx-auto py-8 px-4">
        <div className="mb-6">
          <Link href="/">
            <Button variant="ghost" className="flex items-center gap-2 mb-4">
              <ArrowLeft className="h-4 w-4" /> Back to Search
            </Button>
          </Link>
          <h1 className="text-3xl font-bold text-center mb-2 text-gray-800 dark:text-gray-100">Article Parser</h1>
          <p className="text-center text-gray-500 dark:text-gray-400">Viewing article ID: {params.id}</p>
        </div>

        <Tabs defaultValue="spokesperson" className="w-full">
          <TabsList className="grid w-full grid-cols-5 mb-8">
            <TabsTrigger value="spokesperson">Spokesperson Details</TabsTrigger>
            <TabsTrigger value="source">Source Details</TabsTrigger>
            <TabsTrigger value="article">Article Details</TabsTrigger>
            <TabsTrigger value="author">Author Details</TabsTrigger>
            <TabsTrigger value="people">People Information</TabsTrigger>
          </TabsList>

          <ScrollArea className="h-[calc(100vh-200px)] rounded-md border">
            <TabsContent value="spokesperson" className="p-4">
              <SpokespersonSection />
            </TabsContent>

            <TabsContent value="source" className="p-4">
              <SourceSection />
            </TabsContent>

            <TabsContent value="article" className="p-4">
              <ArticleSection />
            </TabsContent>

            <TabsContent value="author" className="p-4">
              <AuthorSection />
            </TabsContent>

            <TabsContent value="people" className="p-4">
              <PeopleInfoSection />
            </TabsContent>
          </ScrollArea>
        </Tabs>
      </div>
    </main>
  )
}
