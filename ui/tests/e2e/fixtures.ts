/**
 * Shared test fixtures and API mock data for E2E tests.
 *
 * All tests intercept /api/v1/* routes so the backend does not need to be running.
 */
import type { Page, Route } from '@playwright/test';

// ---------------------------------------------------------------------------
// Mock data
// ---------------------------------------------------------------------------

export const MOCK_TOKEN = 'river-stone-moon';
export const MOCK_SHARE_ID = 'abc123share';
export const MOCK_OWN_SHARE_ID = 'zz99myshare'; // distinct from MOCK_SHARE_ID — used as ownShareId
export const MOCK_NAME = 'TestUser';

export const MOCK_ACTS = [
    {
        slug: 'trombone-shorty',
        name: 'Trombone Shorty & Orleans Avenue',
        stage: 'Abita Beer Stage',
        date: '2026-04-16',
        start: '17:00',
        end: '18:30',
        genre: 'Funk'
    },
    {
        slug: 'banu-gibson',
        name: 'Banu Gibson',
        stage: 'French Market Traditional Jazz Stage',
        date: '2026-04-16',
        start: '14:00',
        end: '15:30',
        genre: 'Jazz (Traditional)'
    },
    {
        slug: 'fri-act-one',
        name: 'Friday Act One',
        stage: 'Abita Beer Stage',
        date: '2026-04-17',
        start: '13:00',
        end: '14:30',
        genre: 'Blues'
    }
];

export const MOCK_SCHEDULE_RESPONSE = {
    token: MOCK_TOKEN,
    name: MOCK_NAME,
    picks: [],
    acts: MOCK_ACTS,
    shares: [],
    share_id: MOCK_OWN_SHARE_ID // user's own share_id — distinct from the friend's share
};

export const MOCK_SHARE_RESPONSE = {
    share_id: MOCK_OWN_SHARE_ID,
    share_url: `/fq2026?share=${MOCK_OWN_SHARE_ID}`
};

export const MOCK_SHARED_SCHEDULE = {
    name: 'Friend Schedule',
    picks: ['trombone-shorty'],
    acts: MOCK_ACTS
};

// ---------------------------------------------------------------------------
// Route interceptors
// ---------------------------------------------------------------------------

/** Intercept all /api/v1 routes with standard mocks. */
export async function mockAllApiRoutes(page: Page): Promise<void> {
    // Acts list — filter by date param if provided
    await page.route('**/api/v1/acts**', async (route: Route) => {
        const url = new URL(route.request().url());
        const date = url.searchParams.get('date');
        const acts = date ? MOCK_ACTS.filter((a) => a.date === date) : MOCK_ACTS;
        await route.fulfill({ json: { acts, count: acts.length } });
    });

    // All /api/v1/schedule/** requests — dispatch by path and method
    // Note: use '**/api/v1/schedule**' (double-star suffix) to match across slashes
    await page.route('**/api/v1/schedule**', async (route: Route) => {
        const url = new URL(route.request().url());
        const path = url.pathname;
        const method = route.request().method();

        // POST /api/v1/schedule  — create
        if (method === 'POST' && path === '/api/v1/schedule') {
            await route.fulfill({ json: { token: MOCK_TOKEN } });
            return;
        }

        // GET|PUT /api/v1/schedule/<token>  — load/update
        if (path === `/api/v1/schedule/${MOCK_TOKEN}`) {
            if (method === 'GET') {
                await route.fulfill({ json: MOCK_SCHEDULE_RESPONSE });
            } else if (method === 'PUT') {
                const body = JSON.parse(route.request().postData() ?? '{}');
                await route.fulfill({
                    json: { ...MOCK_SCHEDULE_RESPONSE, picks: body.picks ?? [] }
                });
            } else {
                await route.fulfill({ status: 204, body: '' });
            }
            return;
        }

        // POST /api/v1/schedule/<token>/share
        if (method === 'POST' && path === `/api/v1/schedule/${MOCK_TOKEN}/share`) {
            await route.fulfill({ json: MOCK_SHARE_RESPONSE });
            return;
        }

        // POST /api/v1/schedule/<token>/add-share
        if (method === 'POST' && path === `/api/v1/schedule/${MOCK_TOKEN}/add-share`) {
            await route.fulfill({ json: MOCK_SCHEDULE_RESPONSE });
            return;
        }

        // DELETE /api/v1/schedule/<token>/remove-share/<id>
        if (method === 'DELETE' && path.startsWith(`/api/v1/schedule/${MOCK_TOKEN}/remove-share`)) {
            await route.fulfill({ json: MOCK_SCHEDULE_RESPONSE });
            return;
        }

        // GET /api/v1/schedule/by-share/<shareId>
        if (method === 'GET' && path.startsWith('/api/v1/schedule/by-share/')) {
            await route.fulfill({ json: MOCK_SHARED_SCHEDULE });
            return;
        }

        // GET /api/v1/schedule/fuzzy-lookup — not needed in most tests
        await route.fulfill({ status: 404, body: 'Not found in mock' });
    });

    // Stages
    await page.route('**/api/v1/stages**', async (route: Route) => {
        await route.fulfill({ json: { stages: [], count: 0 } });
    });
}

/** Seed localStorage with a confirmed identity so the IdentityGate is skipped. */
export async function seedIdentity(page: Page): Promise<void> {
    await page.addInitScript(
        ({ token, name }) => {
            localStorage.setItem('fqf_identity', JSON.stringify({ token, name, counter: 1 }));
            localStorage.setItem('fqf_fingerprint_counter', '1');
        },
        { token: MOCK_TOKEN, name: MOCK_NAME }
    );
}

/** Seed localStorage with pre-existing picks. */
export async function seedPicks(page: Page, picks: string[]): Promise<void> {
    await page.addInitScript((p) => {
        localStorage.setItem('fqf_picks', JSON.stringify(p));
    }, picks);
}
