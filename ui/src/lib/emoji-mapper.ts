const MERGE_EMOJIS = ['🐊', '🎺', '🦞', '⚜️', '🎭', '🌶️', '🥁', '🦜'] as const;

export function assignEmojis(tokens: string[]): Record<string, string> {
    const sorted = [...tokens].sort();
    const result: Record<string, string> = {};
    for (let i = 0; i < sorted.length; i++) {
        result[sorted[i]] = MERGE_EMOJIS[i % MERGE_EMOJIS.length];
    }
    return result;
}
