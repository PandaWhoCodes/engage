"use client"

import { Loader2, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"

interface GenerateButtonProps {
  onClick: () => void
  loading: boolean
  disabled?: boolean
}

export function GenerateButton({
  onClick,
  loading,
  disabled = false,
}: GenerateButtonProps) {
  return (
    <Button
      onClick={onClick}
      disabled={loading || disabled}
      size="lg"
      className="w-full"
    >
      {loading ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Generating...
        </>
      ) : (
        <>
          <Sparkles className="mr-2 h-4 w-4" />
          Generate Message
        </>
      )}
    </Button>
  )
}
