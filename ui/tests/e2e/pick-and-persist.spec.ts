/**
 * E2E: Pick and persist
 *
 * Verifies that picking an act updates the pick indicator, and that the pick
 * survives a page reload (via localStorage cache).
 */
import { test, expect } from '@playwright/test';
import { mockAllApiRoutes, seedIdentity, MOCK_ACTS } from './fixtures';

test.describe('Pick and persist', () => {
    test.beforeEach(async ({ page }) => {
        await seedIdentity(page);
        await mockAllApiRoutes(page);
    });

    test('clicking the fleur button picks an act', async ({ page }) => {
        await page.goto('/fq2026');

        const targetAct = MOCK_ACTS.find((a) => a.date === '2026-04-16')!;

        // Wait for the act to be visible
        await expect(page.getByText(targetAct.name)).toBeVisible({ timeout: 10_000 });

        // Find the exact fleur button (exact: true avoids matching the act block div
        // which also has role="button" and a label containing this text as a substring)
        const pickBtn = page.getByRole('button', {
            name: `Add ${targetAct.name} to picks`,
            exact: true
        });
        await expect(pickBtn).toBeVisible();

        await pickBtn.click();

        // After picking, the aria-label should switch to "Remove ... from picks"
        await expect(
            page.getByRole('button', { name: `Remove ${targetAct.name} from picks`, exact: true })
        ).toBeVisible();
    });

    test('pick persists after page reload via localStorage', async ({ page }) => {
        await page.goto('/fq2026');

        const targetAct = MOCK_ACTS.find((a) => a.date === '2026-04-16')!;

        // Wait for act to appear and pick it
        await expect(page.getByText(targetAct.name)).toBeVisible({ timeout: 10_000 });
        await page
            .getByRole('button', { name: `Add ${targetAct.name} to picks`, exact: true })
            .click();

        // Confirm pick indicator changed
        await expect(
            page.getByRole('button', {
                name: `Remove ${targetAct.name} from picks`,
                exact: true
            })
        ).toBeVisible();

        // Seed picks in localStorage so they persist through the reload
        await page.evaluate(
            ({ slug }) => {
                localStorage.setItem('fqf_picks', JSON.stringify([slug]));
            },
            { slug: targetAct.slug }
        );

        // Override the schedule API to return the pick on reload
        await page.route('**/api/v1/schedule**', async (route) => {
            const method = route.request().method();
            if (method === 'GET') {
                await route.fulfill({
                    json: {
                        token: 'river-stone-moon',
                        name: 'TestUser',
                        picks: [targetAct.slug],
                        acts: MOCK_ACTS,
                        shares: [],
                        share_id: 'zz99myshare'
                    }
                });
            } else {
                await route.continue();
            }
        });

        await page.reload();

        await expect(page.getByText(targetAct.name)).toBeVisible({ timeout: 10_000 });
        await expect(
            page.getByRole('button', {
                name: `Remove ${targetAct.name} from picks`,
                exact: true
            })
        ).toBeVisible();
    });

    test('clicking maybe button marks act as maybe', async ({ page }) => {
        await page.goto('/fq2026');

        const targetAct = MOCK_ACTS.find((a) => a.date === '2026-04-16')!;
        await expect(page.getByText(targetAct.name)).toBeVisible({ timeout: 10_000 });

        const maybeBtn = page.getByRole('button', {
            name: `Mark ${targetAct.name} as maybe`,
            exact: true
        });
        await expect(maybeBtn).toBeVisible();
        await maybeBtn.click();

        await expect(
            page.getByRole('button', { name: `Remove ${targetAct.name} from maybes`, exact: true })
        ).toBeVisible();
    });
});
