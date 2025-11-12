"use client"

import { useState } from "react"
import { toast } from "sonner"
import { ThemeSelector } from "@/components/theme-selector"
import { GenerateButton } from "@/components/generate-button"
import { OutputDisplay } from "@/components/output-display"

export default function Home() {
  const [theme, setTheme] = useState("random")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<{
    content: string
    themeUsed: string
  } | null>(null)

  const handleGenerate = async () => {
    setLoading(true)
    setResult(null)

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ theme }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || "Failed to generate message")
      }

      const data = await response.json()
      setResult({
        content: data.content,
        themeUsed: data.theme_used,
      })
      toast.success("Message generated successfully!")
    } catch (error) {
      console.error("Error:", error)
      toast.error(
        error instanceof Error ? error.message : "Failed to generate message"
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="container max-w-2xl mx-auto px-4 py-8 md:py-16">
        <div className="space-y-8">
          {/* Header */}
          <div className="text-center space-y-2">
            <h1 className="text-4xl font-bold tracking-tight">
              Engagement Message Generator
            </h1>
            <p className="text-muted-foreground">
              Generate creative prompts for Gen Z teens
            </p>
          </div>

          {/* Input Section */}
          <div className="space-y-6">
            <ThemeSelector value={theme} onChange={setTheme} />
            <GenerateButton
              onClick={handleGenerate}
              loading={loading}
              disabled={loading}
            />
          </div>

          {/* Output Section */}
          {result && (
            <OutputDisplay content={result.content} themeUsed={result.themeUsed} />
          )}
        </div>
      </div>
    </main>
  )
}
