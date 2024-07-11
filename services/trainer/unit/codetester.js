const {
    testPython,
    testCpp,
    testJs,
    keywordsCode,
} = require('./codetrainer.js');

class CodeTester {
    lang;

    checkList;

    input;

    code;

    libraries;

    error;

    message;

    result;

    setLang (lang) {
        this.lang = lang;
    }

    setLibraries (libraries) {
        this.libraries = libraries;
    }

    addLibraries (libraries) {
        this.libraries += ` ${libraries}`;
    }

    clearLibraries () {
        this.libraries = '';
    }

    setCode (code) {
        this.code = code;
    }

    addCode (code) {
        this.code += code;
    }

    clearCode () {
        this.code = '';
    }

    setInput (input) {
        if (typeof input === 'object') {
            input = input.join('\n');
        }
        this.input = input;
    }

    addInput (input) {
        this.input += `${input}\n`;
    }

    clearInput () {
        this.input = '';
    }

    // checkList

    clear () {
        this.checkList = [];
    }

    print (message, value) {
        const icon = value ? '✅' : '❌';
        this.checkList.push(`${icon} ${message}`);
    }

    // running

    async run () {
        if (this.lang === 'python') {
            const { error, message, result } = await testPython(this.code, this.input, this.libraries);
            this.error = error;
            this.message = message;
            this.result = result;
        } else if (this.lang === 'cpp') {
            const { error, message, result } = await testCpp(this.code, this.input, this.libraries);
            this.error = error;
            this.message = message;
            this.result = result;
        } else if (this.lang === 'javascript') {
            const { error, message, result } = await testJs(this.code, this.input, this.libraries);
            this.error = error;
            this.message = message;
            this.result = result;
        }
        return this.result;
    }

    async runInput (...args) {
        if (args && args.length) {
            this.setInput(args);
        }
        console.log('+-')
        return this.run();
    }

    async runCode (code, ...args) {
        if (args && args.length) {
            this.setInput(args);
        }
        this.addCode(code);
        return this.run();
    }

    // генераторы

    // eslint-disable-next-line class-methods-use-this
    random (min, max, step = 1) {
        const mmax = max;
        const koeff = 1 / step;
        max *= koeff;
        const rand = min + Math.random() * (max + 1 - min);
        let result = Math.floor(rand) / koeff;
        if (result > mmax) {
            result -= step;
        }
        if (result < min) {
            result += step;
        }
        return result;
    }

    // eslint-disable-next-line class-methods-use-this
    randomString (min, max, string = '') {
        if (min !== max) {
            max = this.random(min, max);
        }
        let result = '';

        if (!string) {
            string = ['ru', 'RU', 'en', 'EN'];
        }

        if (typeof string === 'object') {
            const strings = {
                ru: 'абвгдеёжзийклмнопрстуфхцчшщъыьюя',
                RU: 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЮЯ',
                en: 'abcdefghijklmnopqrstuvwxyz',
                EN: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                num: '0123456789',
                sym: '!@#$%^&*()_+-=/{}:;",.?<> ',
            };
            let str = '';
            string.forEach(i => {
                str += strings[i];
            });
            string = str;
        }

        const { length } = string;
        // eslint-disable-next-line no-plusplus
        for (let i = 0; i < max; i++) {
            result += string.charAt(Math.floor(Math.random() * length));
        }
        return result;
    }

    // проверка

    isEqual (string) {
        return !this.error && String(this.result).trim().toLowerCase() === String(string).trim().toLowerCase();
    }

    isContains (string) {
        return !this.error && String(this.result).trim().indexOf(String(string).trim());
    }

    isMatch (regexp, params = 'ui') {
        const r = new RegExp(regexp, params);
        return !this.error && !!String(this.result).trim().match(r)?.length;
    }

    isKeywords (keywords) {
        return keywordsCode(this.code, keywords);
    }
}

const tester = new CodeTester();

module.exports = tester;
