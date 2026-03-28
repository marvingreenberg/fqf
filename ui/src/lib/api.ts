import type {
    ActListResponse,
    ActDetail,
    ScheduleResponse,
    ScheduleUpdate,
    TokenResponse,
    MergeResponse,
    StageListResponse,
    ShareResponse,
    SharedScheduleResponse
} from '$lib/types';

const BASE = '/api/v1';

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
    const resp = await fetch(url, init);
    if (!resp.ok) {
        throw new Error(`API error: ${resp.status} ${resp.statusText}`);
    }
    return resp.json() as Promise<T>;
}

export async function listActs(params?: {
    date?: string;
    stage?: string;
    q?: string;
}): Promise<ActListResponse> {
    const query = new URLSearchParams();
    if (params?.date) query.set('date', params.date);
    if (params?.stage) query.set('stage', params.stage);
    if (params?.q) query.set('q', params.q);
    const qs = query.toString();
    return fetchJson<ActListResponse>(`${BASE}/acts${qs ? `?${qs}` : ''}`);
}

export async function getAct(slug: string): Promise<ActDetail> {
    return fetchJson<ActDetail>(`${BASE}/acts/${slug}`);
}

export async function createSchedule(name?: string): Promise<TokenResponse> {
    const body = name ? JSON.stringify({ name }) : undefined;
    return fetchJson<TokenResponse>(`${BASE}/schedule`, {
        method: 'POST',
        headers: body ? { 'Content-Type': 'application/json' } : undefined,
        body
    });
}

export async function loadSchedule(token: string): Promise<ScheduleResponse> {
    return fetchJson<ScheduleResponse>(`${BASE}/schedule/${token}`);
}

export async function savePicks(
    token: string,
    picks: string[],
    name?: string
): Promise<ScheduleResponse> {
    const body: ScheduleUpdate = { picks, ...(name !== undefined ? { name } : {}) };
    return fetchJson<ScheduleResponse>(`${BASE}/schedule/${token}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
}

export async function createShare(token: string): Promise<ShareResponse> {
    return fetchJson<ShareResponse>(`${BASE}/schedule/${token}/share`, { method: 'POST' });
}

export async function loadSharedSchedule(shareId: string): Promise<SharedScheduleResponse> {
    return fetchJson<SharedScheduleResponse>(`${BASE}/schedule/by-share/${shareId}`);
}

export async function mergeSchedules(tokens: string[]): Promise<MergeResponse> {
    return fetchJson<MergeResponse>(`${BASE}/schedule/merge?tokens=${tokens.join(',')}`);
}

export async function listStages(): Promise<StageListResponse> {
    return fetchJson<StageListResponse>(`${BASE}/stages`);
}
