"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { useMutation } from "@tanstack/react-query"
import { Search } from "lucide-react"

import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"

export default function NewInvestigationPage() {
  const router = useRouter()
  const [title, setTitle] = useState("")
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [username, setUsername] = useState("")

  const createMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post("/investigations/", data)
      return response.data
    },
    onSuccess: () => {
      router.push("/")
    },
    onError: (err) => {
      console.error(err)
      alert("Failed to create investigation")
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    // Clean up empty fields
    const targetData: Record<string, string> = {}
    if (email) targetData.email = email
    if (phone) targetData.phone = phone
    if (username) targetData.username = username

    createMutation.mutate({
      title,
      target_data: targetData
    })
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">New Investigation</h2>
        <p className="text-muted-foreground">Input known intelligence to begin tracking a digital footprint.</p>
      </div>

      <Card>
        <form onSubmit={handleSubmit}>
          <CardHeader>
            <CardTitle>Subject Details</CardTitle>
            <CardDescription>Provide any known identifiers. The more you provide, the better the resolution.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="title">Investigation Name *</Label>
              <Input 
                id="title" 
                placeholder="e.g. John Doe OSINT" 
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required 
              />
            </div>
            
            <div className="pt-4 border-t">
              <h4 className="text-sm font-medium mb-4">Initial Intelligence</h4>
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="email">Email Address</Label>
                  <Input 
                    id="email" 
                    type="email" 
                    placeholder="john@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="phone">Phone Number</Label>
                  <Input 
                    id="phone" 
                    placeholder="+1 555 123 4567"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="username">Known Username</Label>
                  <Input 
                    id="username" 
                    placeholder="johndoe1999"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                  />
                </div>
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex justify-end gap-2">
            <Button variant="outline" type="button" onClick={() => router.back()}>Cancel</Button>
            <Button type="submit" disabled={createMutation.isPending || !title}>
              <Search className="mr-2 h-4 w-4" /> 
              {createMutation.isPending ? "Starting..." : "Start Investigation"}
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
