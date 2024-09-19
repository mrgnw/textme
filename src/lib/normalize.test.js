import { describe, it, expect } from 'vitest';
import { normalize } from './normalize.js';

describe('normalize', () => {
	it('converts word digits to numeric digits', () => {
		const input = 'SEIS-CERO-SIETE';
		const output = normalize(input);
		expect(output).toBe('+1607');
	});

	it('handles numbers with country code', () => {
		const input = '+54 9 11 1234 5678';
		const output = normalize(input);
		expect(output).toBe('+5491112345678');
	});

	it('defaults to country code "1" if none provided', () => {
		const input = '1234567890';
		const output = normalize(input);
		expect(output).toBe('+11234567890');
	});

});