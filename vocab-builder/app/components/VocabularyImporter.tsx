"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { generateVocabulary } from "../actions/generateVocabulary"

export default function VocabularyImporter() {
  const [category, setCategory] = useState("")
  const [result, setResult] = useState("")
  const [isLoading, setIsLoading] = useState(false)


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      const data = await generateVocabulary(category)
      setResult(JSON.stringify(data, null, 2))
    } catch (error) {
      console.error("Error generating vocabulary:", error)
      setResult("Error generating vocabulary. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(result).then(() => {
      alert("Copied to clipboard!")
    })
  }

  const handleReset = () => {
    setCategory("");
    setResult("");
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit}>
        <Input
          type="text"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          placeholder="Enter thematic category"
          required
        />
        <div className="flex space-x-4">
          <Button type="submit" disabled={isLoading}>
            {isLoading ? "Generating..." : "Generate Vocabulary"}
          </Button>
          <Button type="reset" onClick={handleReset} disabled={isLoading}>
            {isLoading ? "Resetting..." : "Reset"}
          </Button>
        </div>
      </form>
      {result !== "" && (
        <div className="space-y-4">
          <Textarea value={result} readOnly />
          <Button onClick={handleCopy}>Copy to Clipboard</Button>
        </div>
      )}

    </div>
  )
}