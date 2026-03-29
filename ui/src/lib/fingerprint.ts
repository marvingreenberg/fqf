/**
 * Generate a device fingerprint by drawing on a hidden canvas and hashing the result.
 * Returns a hex SHA-256 hash, or null if canvas fingerprinting is unstable (Brave, Tor).
 */

const CANVAS_WIDTH = 200;
const CANVAS_HEIGHT = 50;
const FINGERPRINT_TEXT = 'FQF2026 \uD83C\uDFBA';
const RECT_X = 125;
const RECT_Y = 1;
const RECT_W = 62;
const RECT_H = 20;
const TEXT_Y_PRIMARY = 15;
const TEXT_Y_SECONDARY = 17;
const FONT_SPEC = '14px Arial';
const COLOR_ORANGE = '#f60';
const COLOR_BLUE = '#069';
const COLOR_GREEN_ALPHA = 'rgba(102, 204, 0, 0.7)';

function drawFingerprint(ctx: CanvasRenderingContext2D): void {
    ctx.textBaseline = 'top';
    ctx.font = FONT_SPEC;
    ctx.fillStyle = COLOR_ORANGE;
    ctx.fillRect(RECT_X, RECT_Y, RECT_W, RECT_H);
    ctx.fillStyle = COLOR_BLUE;
    ctx.fillText(FINGERPRINT_TEXT, 2, TEXT_Y_PRIMARY);
    ctx.fillStyle = COLOR_GREEN_ALPHA;
    ctx.fillText(FINGERPRINT_TEXT, 4, TEXT_Y_SECONDARY);
}

export async function getFingerprint(): Promise<string | null> {
    const canvas = document.createElement('canvas');
    canvas.width = CANVAS_WIDTH;
    canvas.height = CANVAS_HEIGHT;
    const ctx = canvas.getContext('2d');
    if (!ctx) return null;

    drawFingerprint(ctx);
    const dataUrl1 = canvas.toDataURL();

    // Stability check: draw again and compare — Brave/Tor randomize canvas output
    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    drawFingerprint(ctx);
    const dataUrl2 = canvas.toDataURL();

    if (dataUrl1 !== dataUrl2) return null;

    const encoder = new TextEncoder();
    const data = encoder.encode(dataUrl1);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, '0')).join('');
}
