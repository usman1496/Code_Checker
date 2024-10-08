module.exports = {
    env: {
      browser: true,
      es2021: true,
    },
    extends: [
      'eslint:recommended',
      'plugin:@typescript-eslint/recommended',
    ],
    parser: '@typescript-eslint/parser',
    parserOptions: {
      ecmaVersion: 12,
      sourceType: 'module',
    },
    "plugins": [
    "@typescript-eslint"
  ],
    
    rules: {
      'semi': ['error', 'always'], // Ensure this rule is included
      'no-unused-vars': 'warn',
      'no-undef': 'error',
      'quotes': ['error', 'single'],
      'no-console': 'off',
    },
  };
  