import js from '@eslint/js';
import parser from '@typescript-eslint/parser';

export default [
  js.configs.recommended,
  { ignores: ['dist/**'] },
  { files: ['src/**/*.{ts,tsx}'], languageOptions: { parser, parserOptions: { ecmaVersion: 'latest', sourceType: 'module', ecmaFeatures: { jsx: true } }, globals: { window: 'readonly', confirm: 'readonly', fetch: 'readonly', WebSocket: 'readonly', HTMLVideoElement: 'readonly' } }, rules: { 'no-undef': 'off', 'no-unused-vars': 'off' } },
];
