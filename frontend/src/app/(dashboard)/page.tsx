"use client"

import { useQuery } from "@tanstack/react-query"
import Link from "next/link"
import { Plus, Clock, ExternalLink } from "lucide-react"

import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface Investigation {
  id: number
  title: string
  status: string
  created_at: string
}

export default function DashboardPage() {
  const { data: investigations, isLoading, isError } = useQuery<Investigation[]>({
    queryKey: ["investigations"],
    queryFn: async () => {
      const res = await api.get("/investigations/")
      return res.data
    },
  })

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Recent Investigations</h2>
          <p className="text-muted-foreground">Manage and track your OSINT resolutions here.</p>
        </div>
        <Link href="/investigations/new">
          <Button>
            <Plus className="mr-2 h-4 w-4" /> New Investigation
          </Button>
        </Link>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {isLoading && <p>Loading investigations...</p>}
        {isError && <p className="text-destructive">Failed to load investigations.</p>}
        
        {investigations?.length === 0 && (
          <div className="col-span-full py-12 text-center">
            <h3 className="text-lg font-medium">No investigations yet</h3>
            <p className="text-sm text-muted-foreground mt-1">Start tracking a new digital footprint to see results here.</p>
          </div>
        )}

        {investigations?.map((inv) => (
          <Card key={inv.id} className="hover:border-primary/50 transition-colors">
            <CardHeader className="pb-3">
              <div className="flex justify-between items-start">
                <CardTitle className="text-xl line-clamp-1">{inv.title}</CardTitle>
                <div className="text-xs capitalize px-2 py-1 bg-muted rounded-full">
                  {inv.status}
                </div>
              </div>
              <CardDescription className="flex items-center gap-1">
                <Clock className="h-3 w-3" />
                {new Date(inv.created_at).toLocaleDateString()}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="secondary" className="w-full mt-2" disabled>
                View Details <ExternalLink className="ml-2 h-3 w-3" />
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
