module.exports = {
    roots: [
	'<rootDir>/',
	'<rootDir>/..'
    ],
    moduleDirectories: [
	'node_modules',
	'<rootDir>/tests/node_modules',
	'<rootDir>/../tests/node_modules',
	'<rootDir>/../../tests/node_modules',
	'<rootDir>/../../../tests/node_modules'
    ],
    //testEnvironment: 'jest-environment-jsdom',
    testEnvironment: 'jsdom',
    setupFilesAfterEnv: ['./jest.setupTests.js'],
    verbose: true
};

