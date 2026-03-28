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

export interface ScheduleResponse {
    token: string;
    name: string;
    picks: string[];
    acts: ActSummary[];
}

export interface ScheduleUpdate {
    picks: string[];
    name?: string;
}

export interface TokenResponse {
    token: string;
}

export interface ShareResponse {
    share_id: string;
    share_url: string;
}

export interface SharedScheduleResponse {
    name: string;
    picks: string[];
    acts: ActSummary[];
}

export interface MergeEntry {
    token: string;
    picks: string[];
}

export interface MergeResponse {
    schedules: MergeEntry[];
    acts: ActSummary[];
}

export interface SharedSchedule {
    share_id: string;
    name: string;
    picks: string[];
    acts: ActSummary[];
}

export type ConflictLevel = 'none' | 'yellow' | 'red';

export type ViewMode = 'grid' | 'mobile' | 'my-schedule' | 'share';

export type MobileSortMode = 'by-time' | 'by-stage';

export const FESTIVAL_DATES = ['2026-04-16', '2026-04-17', '2026-04-18', '2026-04-19'] as const;

export const DAY_LABELS: Record<string, string> = {
    '2026-04-16': 'Thu 16',
    '2026-04-17': 'Fri 17',
    '2026-04-18': 'Sat 18',
    '2026-04-19': 'Sun 19'
};

export const IDENTITY_STORAGE_KEY = 'fqf_identity';
