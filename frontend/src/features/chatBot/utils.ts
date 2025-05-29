export function extractUsedIndices(answer: string): number[] {
  const matches = [...answer.matchAll(/\[(\d+)\]/g)]
  const rawIndices = matches.map((m) => parseInt(m[1]))
  return Array.from(new Set(rawIndices)).sort((a, b) => a - b)
}

export function remapAnswer(answer: string, usedIndices: number[]): string {
  const indexMap = new Map<number, number>()
  usedIndices.forEach((original, i) => {
    indexMap.set(original, i + 1)
  })

  return answer.replace(/\[(\d+)\]/g, (_, p1) => {
    const mapped = indexMap.get(parseInt(p1))
    return mapped ? `[${mapped}]` : `[${p1}]`
  })
}

export function getUsedSources<T = any>(sources: T[], usedIndices: number[]): T[] {
  return usedIndices.map((i) => sources[i - 1]).filter(Boolean)
}
