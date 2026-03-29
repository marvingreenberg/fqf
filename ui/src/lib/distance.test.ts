import { describe, it, expect } from 'vitest';
import {
    haversineMeters,
    walkingDistanceMeters,
    formatDistance,
    distanceStyle,
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
    it('converts meters to feet rounded to nearest 100', () => {
        // 100m * 3.28084 = 328ft → rounds to 300
        expect(formatDistance(100)).toBe('300 ft');
    });

    it('rounds up to nearest 100', () => {
        // 200m * 3.28084 = 656ft → rounds to 700
        expect(formatDistance(200)).toBe('700 ft');
    });

    it('handles large distances', () => {
        // 1000m * 3.28084 = 3281ft → rounds to 3300
        expect(formatDistance(1000)).toBe('3300 ft');
    });

    it('enforces minimum of 100 ft for very short distances', () => {
        // 10m * 3.28084 = 33ft → rounds to 0 → clamped to 100
        expect(formatDistance(10)).toBe('100 ft');
    });
});

describe('distanceStyle', () => {
    it('returns green style for close distances', () => {
        // 100m = 328ft < 600
        expect(distanceStyle(100)).toContain('#1a7a4a');
    });

    it('returns orange style for medium distances', () => {
        // 250m = 820ft, between 600 and 1200
        expect(distanceStyle(250)).toContain('#d97706');
    });

    it('returns dark red bold style for far distances', () => {
        // 400m = 1312ft >= 1200
        const style = distanceStyle(400);
        expect(style).toContain('#991b1b');
        expect(style).toContain('font-weight: 700');
    });

    it('returns green for distances right at zero', () => {
        // 0m = 0ft < 600
        expect(distanceStyle(0)).toContain('#1a7a4a');
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
