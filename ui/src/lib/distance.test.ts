import { describe, it, expect } from 'vitest';
import {
    haversineMeters,
    walkingDistanceMeters,
    formatDistance,
    shortenStageName
} from '$lib/distance';

describe('haversineMeters', () => {
    it('returns 0 for identical points', () => {
        expect(haversineMeters(29.95, -90.06, 29.95, -90.06)).toBe(0);
    });

    it('returns reasonable distance for Fish Fry to Entergy', () => {
        // Fish Fry (29.95107, -90.06280) to Entergy (29.96145, -90.05825)
        const dist = haversineMeters(29.95107, -90.0628, 29.96145, -90.05825);
        // Roughly 1.2 km straight line
        expect(dist).toBeGreaterThan(1000);
        expect(dist).toBeLessThan(1500);
    });

    it('returns short distance for adjacent stages', () => {
        // Cafe Beignet (29.95582, -90.06843) to Jazz Playhouse (29.95582, -90.06850)
        const dist = haversineMeters(29.95582, -90.06843, 29.95582, -90.0685);
        expect(dist).toBeLessThan(10);
    });
});

describe('walkingDistanceMeters', () => {
    it('is 1.25x haversine', () => {
        const haversine = haversineMeters(29.95107, -90.0628, 29.96145, -90.05825);
        const walking = walkingDistanceMeters(29.95107, -90.0628, 29.96145, -90.05825);
        expect(walking).toBeCloseTo(haversine * 1.25, 0);
    });
});

describe('formatDistance', () => {
    it('formats meters below 1km', () => {
        expect(formatDistance(350)).toBe('350m');
    });

    it('formats kilometers', () => {
        expect(formatDistance(1200)).toBe('1.2km');
    });

    it('rounds meters', () => {
        expect(formatDistance(349.7)).toBe('350m');
    });

    it('formats exactly 1km', () => {
        expect(formatDistance(1000)).toBe('1.0km');
    });
});

describe('shortenStageName', () => {
    it('strips " Stage" suffix', () => {
        expect(shortenStageName('Abita Beer Stage')).toBe('Abita Beer');
    });

    it('truncates long names with ellipsis', () => {
        expect(shortenStageName("Jack Daniel's Stage")).toBe('Jack Dani\u2026');
    });

    it('truncates long names after removing Stage suffix', () => {
        // "KREWE Eyewear" = 13 chars → slice(0,9) + "…"
        expect(shortenStageName('KREWE Eyewear Stage')).toBe('KREWE Eye\u2026');
    });

    it('handles names without Stage suffix', () => {
        // "Jazz Playhouse at the Royal Sonesta" = 35 chars → slice(0,9) + "…"
        expect(shortenStageName('Jazz Playhouse at the Royal Sonesta')).toBe('Jazz Play\u2026');
    });

    it('keeps names at exactly 10 chars', () => {
        expect(shortenStageName('Abita Beer')).toBe('Abita Beer');
    });
});
