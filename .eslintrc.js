module.exports = {
    "env": {
        "browser": true,
        "es2021": true,
        "jest": true,
	"node": true,
	"es6": true
    },
    "extends": [
        "eslint:recommended",
        "plugin:react/recommended"
    ],
    "overrides": [
        {
            "env": {
                "node": true
            },
            "files": [
                ".eslintrc.{js,cjs}"
            ],
            "parserOptions": {
                "sourceType": "script"
            }
        }
    ],
    "parserOptions": {
        "ecmaVersion": "2018",
        "sourceType": "module"
    },
    "plugins": [
	"react"
    ],
    "rules": {
    },
    "settings": {
	"react": { "version": "17.0.1" }
    },
    "parser": "babel-eslint"
};

