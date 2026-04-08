import type {
    ActListResponse,
    ActDetail,
    FuzzyLookupResponse,
    ScheduleResponse,
    ScheduleUpdate,
    TokenResponse,
    StageListResponse,
    ShareResponse,
    SharedScheduleResponse,
    ShareRef,
    ShareBackResponse
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

export async function createSchedule(
    name: string,
    fingerprintHash?: string,
    counter?: number
): Promise<TokenResponse> {
    const body = JSON.stringify({
        name,
        ...(fingerprintHash !== undefined ? { fingerprint_hash: fingerprintHash } : {}),
        ...(counter !== undefined ? { counter } : {})
    });
    return fetchJson<TokenResponse>(`${BASE}/schedule`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body
    });
}

export async function fuzzyLookup(rawTriple: string): Promise<FuzzyLookupResponse> {
    // Backend returns { token, suggestion } — we enrich to the full FuzzyLookupResponse shape
    const raw = await fetchJson<{ token: string; suggestion: string | null }>(
        `${BASE}/schedule/fuzzy-lookup`,
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ raw_triple: rawTriple })
        }
    );
    const schedule = await fetchJson<ScheduleResponse>(`${BASE}/schedule/${raw.token}`);
    return {
        token: raw.token,
        found: true,
        corrected: raw.suggestion !== null,
        suggestion: raw.suggestion ?? '',
        name: schedule.name
    };
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

export async function loadSharedSchedule(
    shareId: string,
    checkShareId?: string
): Promise<SharedScheduleResponse> {
    const params = checkShareId ? `?check_share_id=${encodeURIComponent(checkShareId)}` : '';
    return fetchJson<SharedScheduleResponse>(`${BASE}/schedule/by-share/${shareId}${params}`);
}

export async function shareBack(
    targetShareId: string,
    ourShareId: string,
    ourName: string
): Promise<ShareBackResponse> {
    return fetchJson<ShareBackResponse>(`${BASE}/schedule/by-share/${targetShareId}/share-back`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ our_share_id: ourShareId, our_name: ourName })
    });
}

export async function addShareToSchedule(
    token: string,
    shareRef: ShareRef
): Promise<ScheduleResponse> {
    return fetchJson<ScheduleResponse>(`${BASE}/schedule/${token}/add-share`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(shareRef)
    });
}

export async function removeShareFromSchedule(
    token: string,
    shareId: string
): Promise<ScheduleResponse> {
    return fetchJson<ScheduleResponse>(`${BASE}/schedule/${token}/remove-share/${shareId}`, {
        method: 'DELETE'
    });
}

export async function deleteSchedule(token: string): Promise<void> {
    const resp = await fetch(`${BASE}/schedule/${token}`, { method: 'DELETE' });
    if (!resp.ok) {
        throw new Error(`API error: ${resp.status} ${resp.statusText}`);
    }
}

export async function listStages(): Promise<StageListResponse> {
    return fetchJson<StageListResponse>(`${BASE}/stages`);
}
