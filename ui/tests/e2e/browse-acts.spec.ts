/**
 * E2E: Browse acts
 *
 * Verifies the act grid loads, day tabs work, and acts are filtered by day.
 */
import { test, expect } from '@playwright/test';
import { mockAllApiRoutes, seedIdentity, MOCK_ACTS } from './fixtures';

test.describe('Browse acts', () => {
    test.beforeEach(async ({ page }) => {
        await seedIdentity(page);
        await mockAllApiRoutes(page);
    });

    test('act grid loads with acts visible', async ({ page }) => {
        await page.goto('/fq2026');

        // Wait for an act name to appear — confirms the grid rendered
        const thursdayAct = MOCK_ACTS.find((a) => a.date === '2026-04-16')!;
        await expect(page.getByText(thursdayAct.name)).toBeVisible({ timeout: 10_000 });
    });

    test('day tabs are present for all four festival days', async ({ page }) => {
        await page.goto('/fq2026');

        await expect(page.getByRole('button', { name: 'Thu 16' })).toBeVisible();
        await expect(page.getByRole('button', { name: 'Fri 17' })).toBeVisible();
        await expect(page.getByRole('button', { name: 'Sat 18' })).toBeVisible();
        await expect(page.getByRole('button', { name: 'Sun 19' })).toBeVisible();
    });

    test('switching day tabs shows acts for that day', async ({ page }) => {
        await page.goto('/fq2026');

        // Wait for Thursday tab to load
        const thuAct = MOCK_ACTS.find((a) => a.date === '2026-04-16')!;
        await expect(page.getByText(thuAct.name)).toBeVisible({ timeout: 10_000 });

        // Switch to Friday
        await page.getByRole('button', { name: 'Fri 17' }).click();

        // Friday act should appear
        const friAct = MOCK_ACTS.find((a) => a.date === '2026-04-17')!;
        await expect(page.getByText(friAct.name)).toBeVisible({ timeout: 10_000 });

        // Thursday-only acts should no longer be visible
        // (trombone-shorty is Thu only in mock data)
        const thuOnlyAct = MOCK_ACTS.find(
            (a) => a.date === '2026-04-16' && a.slug === 'trombone-shorty'
        )!;
        await expect(page.getByText(thuOnlyAct.name)).not.toBeVisible();
    });
});
