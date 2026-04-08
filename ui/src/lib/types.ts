export interface ActSummary {
    slug: string;
    name: string;
    stage: string;
    date: string; // "YYYY-MM-DD"
    start: string; // "HH:MM"
    end: string; // "HH:MM"
    genre: string;
}

export interface ActDetail extends ActSummary {
    about: string;
    about_source: string;
    websites: string[];
}

export interface StageInfo {
    name: string;
    lat: number;
    lng: number;
    order: number;
}

export interface StageListResponse {
    stages: StageInfo[];
    count: number;
}

export interface ActListResponse {
    acts: ActSummary[];
    count: number;
}

export interface ShareRef {
    share_id: string;
    name: string;
}

export interface ScheduleResponse {
    token: string;
    name: string;
    picks: string[];
    acts: ActSummary[];
    shares: ShareRef[];
    share_id: string;
}

export interface ScheduleUpdate {
    picks: string[];
    name?: string;
}

export interface TokenResponse {
    token: string;
}

export interface FuzzyLookupResponse {
    token: string;
    corrected: boolean;
    suggestion: string;
    name: string;
    found: boolean;
}

export interface ShareResponse {
    share_id: string;
    share_url: string;
}

export interface SharedScheduleResponse {
    name: string;
    picks: string[];
    acts: ActSummary[];
    has_back_share?: boolean | null;
}

export interface SharedSchedule {
    share_id: string;
    name: string;
    picks: string[];
    acts: ActSummary[];
    shared_back?: boolean;
}

export interface ShareBackResponse {
    already_shared: boolean;
}

export type ConflictLevel = 'none' | 'yellow' | 'red';

export type ViewMode = 'all-acts' | 'my-schedule' | 'share' | 'map';

export type MobileSortMode = 'by-time' | 'by-stage';

export const FESTIVAL_DATES = ['2026-04-16', '2026-04-17', '2026-04-18', '2026-04-19'] as const;

export const DAY_LABELS: Record<string, string> = {
    '2026-04-16': 'Thu 16',
    '2026-04-17': 'Fri 17',
    '2026-04-18': 'Sat 18',
    '2026-04-19': 'Sun 19'
};

export const IDENTITY_STORAGE_KEY = 'fqf_identity';
export const FINGERPRINT_COUNTER_KEY = 'fqf_fingerprint_counter';
export const PICKS_STORAGE_KEY = 'fqf_picks';
export const ACTS_STORAGE_PREFIX = 'fqf_acts_';
export const STAGES_STORAGE_KEY = 'fqf_stage_locations';
// 24-hour TTL for act/stage caches (data is static for the festival run)
export const ACTS_CACHE_TTL_MS = 24 * 60 * 60 * 1000;
