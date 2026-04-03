/**
 * E2E: Share flow
 *
 * Verifies that:
 * 1. Opening the AvatarMenu shows a share option.
 * 2. Generating a share link produces a URL.
 * 3. Navigating to a share URL loads the shared schedule view.
 */
import { test, expect } from '@playwright/test';
import {
    mockAllApiRoutes,
    seedIdentity,
    MOCK_ACTS,
    MOCK_SHARE_ID,
    MOCK_OWN_SHARE_ID,
    MOCK_SHARED_SCHEDULE
} from './fixtures';

test.describe('Share flow', () => {
    test.beforeEach(async ({ page }) => {
        await seedIdentity(page);
        await mockAllApiRoutes(page);
    });

    test('avatar menu is visible after identity confirmed', async ({ page }) => {
        await page.goto('/fq2026');
        // Wait for acts to load as a proxy for "confirmed" state
        await expect(page.getByText(MOCK_ACTS[0].name)).toBeVisible({ timeout: 10_000 });

        // Avatar button has aria-label="Identity menu"
        await expect(page.getByRole('button', { name: 'Identity menu' })).toBeVisible();
    });

    test('generate share link produces a URL containing share=', async ({ page }) => {
        await page.goto('/fq2026');
        await expect(page.getByText(MOCK_ACTS[0].name)).toBeVisible({ timeout: 10_000 });

        // Open avatar menu
        await page.getByRole('button', { name: 'Identity menu' }).click();

        // Click the "Share my schedule" button inside the menu
        await page.getByRole('button', { name: 'Share my schedule' }).click();

        // After generating, the share URL containing the user's own share_id should appear
        await expect(page.getByText(new RegExp(MOCK_OWN_SHARE_ID))).toBeVisible({ timeout: 5_000 });
    });

    test('navigating to a share URL shows the owner name', async ({ page }) => {
        // The shared schedule route renders at /fq2026/<share_id>
        // It shows a ShareLoginPane with an h2 heading "{ownerName}'s Schedule"
        await page.goto(`/fq2026/${MOCK_SHARE_ID}`);

        // Use heading role to target the h2 specifically (avoids matching other text)
        await expect(
            page.getByRole('heading', { name: `${MOCK_SHARED_SCHEDULE.name}'s Schedule` })
        ).toBeVisible({ timeout: 10_000 });
    });

    test('dismissing share login pane reveals the shared act grid', async ({ page }) => {
        await page.goto(`/fq2026/${MOCK_SHARE_ID}`);

        // Wait for the share pane to appear, then dismiss it
        const seeBtn = page.getByRole('button', {
            name: `See ${MOCK_SHARED_SCHEDULE.name}'s schedule`
        });
        await expect(seeBtn).toBeVisible({ timeout: 10_000 });
        await seeBtn.click();

        // After dismissing, the ScheduleShell renders with the shared acts
        await expect(page.getByText(MOCK_ACTS[0].name)).toBeVisible({ timeout: 10_000 });
    });

    test('opening share link on main page switches to share view', async ({ page }) => {
        // Navigating with ?share=<id> and a confirmed identity should:
        // 1. Confirm the user (token in localStorage)
        // 2. Load the share via the by-share API
        // 3. Add it to sharedSchedules and switch to share view
        // We verify the view switches away from 'All Acts' to the share-related view.
        await page.goto(`/fq2026?share=${MOCK_SHARE_ID}&name=${MOCK_SHARED_SCHEDULE.name}`);

        // After identity confirmation and share processing, the Share tab should show (1).
        // Use a longer timeout since this involves two async operations (confirm + loadShare).
        await expect(page.getByRole('button', { name: /Share \(1\)/i })).toBeVisible({
            timeout: 15_000
        });
    });
});
