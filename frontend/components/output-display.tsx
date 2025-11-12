"use client"

import { useState } from "react"
import { Copy, Check } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"

interface OutputDisplayProps {
  content: string
  themeUsed: string
}

export function OutputDisplay({ content, themeUsed }: OutputDisplayProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error("Failed to copy:", err)
    }
  }

  if (!content) {
    return null
  }

  return (
    <div className="animate-in fade-in-50 duration-500">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Generated Message</CardTitle>
              <p className="text-sm text-muted-foreground mt-1">
                Theme: {themeUsed}
              </p>
            </div>
            <Button
              variant="outline"
              size="icon"
              onClick={handleCopy}
              title="Copy to clipboard"
            >
              {copied ? (
                <Check className="h-4 w-4 text-green-500" />
              ) : (
                <Copy className="h-4 w-4" />
              )}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <Textarea
            value={content}
            readOnly
            className="min-h-[150px] resize-none"
          />
        </CardContent>
      </Card>
    </div>
  )
}
