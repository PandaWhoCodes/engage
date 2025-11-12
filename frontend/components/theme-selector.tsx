"use client"

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

const THEMES = [
  { value: "random", label: "Random" },
  { value: "meme/internet culture", label: "Meme / Internet Culture" },
  { value: "sports/competition", label: "Sports / Competition" },
  { value: "music/arts", label: "Music / Arts" },
  { value: "gaming/tech", label: "Gaming / Tech" },
  { value: "real talk/deep thoughts", label: "Real Talk / Deep Thoughts" },
  { value: "goals/ambitions", label: "Goals / Ambitions" },
  { value: "funny/lighthearted", label: "Funny / Lighthearted" },
  { value: "challenges/support", label: "Challenges / Support" },
]

interface ThemeSelectorProps {
  value: string
  onChange: (value: string) => void
}

export function ThemeSelector({ value, onChange }: ThemeSelectorProps) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
        Select Theme
      </label>
      <Select value={value} onValueChange={onChange}>
        <SelectTrigger className="w-full">
          <SelectValue placeholder="Choose a theme" />
        </SelectTrigger>
        <SelectContent>
          {THEMES.map((theme) => (
            <SelectItem key={theme.value} value={theme.value}>
              {theme.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )
}
