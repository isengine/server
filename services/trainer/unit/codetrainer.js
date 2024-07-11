const axios = require('axios');

const compile = async (data) => {
    const inputJson = data.input?.split(/[\r\n]+/) || [];
    const api = 'http://localhost:3999/run';
    try {
        console.log('+++')
        const res = await axios.post(api, {
            command: data.command,
            stdin: inputJson,
            files: [
                {
                    name: data.name,
                    content: data.code,
                },
            ],
        });
        console.log('res', res);
        if (!res?.data || res?.data?.stderr) {
            let message = '';
            if (res?.data?.stdout) {
                message += res.data.stdout;
            }
            if (res?.data?.stderr) {
                message += message ? '\n\n' : '';
                message += res.data.stderr;
            }
            return {
                error: true,
                message,
                result: undefined,
            };
        }
        return {
            error: false,
            message: undefined,
            result: res?.data?.stdout,
        };
    } catch (e) {
        return {
            error: true,
            message: `${e}`,
            result: undefined,
        };
    }
}

const equalCode = (customCode, originalCode) => {
    const customCodeResult = ` ${customCode}`
        .replaceAll(/(^|\r|\n)\s*#.+?($|\r|\n)/gi, '')
        .replaceAll(/[\n\r,;:{}]+/gi, ' ')
        .replaceAll('"', "'")
        .replaceAll(/\s[a-zA-Z0-9]+\s*=/gi, ' =')
        .replaceAll(/=\s*[a-zA-Z0-9]+\s/gi, '= ')
        .replaceAll(/\(\s*[a-zA-Z0-9]+\s*\)+/gi, '()')
        .replaceAll(/\[.*?\]/gi, '[]')
        .replaceAll(/'.*?'/gi, '')
        .replaceAll(/'\s+'/gi, ' ');
    const originalCodeResult = ` ${originalCode}`
        .replaceAll(/(^|\r|\n)\s*#.+?($|\r|\n)/gi, '')
        .replaceAll(/[\n\r,;:{}]+/gi, ' ')
        .replaceAll('"', "'")
        .replaceAll(/\s[a-zA-Z0-9]+\s*=/gi, ' =')
        .replaceAll(/=\s*[a-zA-Z0-9]+\s/gi, '= ')
        .replaceAll(/\(\s*[a-zA-Z0-9]+\s*\)+/gi, '()')
        .replaceAll(/\[.*?\]/gi, '[]')
        .replaceAll(/'.*?'/gi, '')
        .replaceAll(/'\s+'/gi, ' ');
    console.log('customCodeResult', customCodeResult);
    console.log('originalCodeResult', originalCodeResult);
    return customCodeResult === originalCodeResult;
}

const keywordsCode = (code, keywords) => {
    const keywordsList = keywords?.replaceAll('"', "'").replaceAll(/[\s,]+/gi, ' ').split(' ');
    let result = true;
    keywordsList?.forEach(i => {
        if (code.indexOf(i) < 0) {
            result = false;
        }
    });
    return result;
}

const clearCode = (code) => {
    return code?.replaceAll(/[\n\r\s]+/gu, '').replaceAll('\n', '').trim();
}

const testPython = async (code, input = undefined, libraries = undefined) => {
    let command = '';
    if (libraries && libraries.trim()) {
        command = `pip install ${libraries.replace(/[\s\n,]+/iug, ' ')} && `;
    }
    command += 'python main.py';
    return compile({
        command,
        input,
        name: 'main.py',
        code,
        libraries,
    });
}

const testCpp = async (code, input = undefined, libraries = undefined) => {
    return compile({
        command: 'g++ -pipe -O2 -static -o main main.cpp && ./main',
        input,
        name: 'main.cpp',
        code,
        libraries,
    });
}

const testJs = async (code, input = undefined, libraries = undefined) => {
    let command = '';
    if (libraries && libraries.trim()) {
        command = `npm i ${libraries.replace(/[\s\n,]+/iug, ' ')} && `;
    }
    command += 'node ./index.js';
    return compile({
        command,
        input,
        name: 'index.js',
        code,
        libraries,
    });
}

module.exports.compile = compile;
module.exports.equalCode = equalCode;
module.exports.keywordsCode = keywordsCode;
module.exports.clearCode = clearCode;
module.exports.testPython = testPython;
module.exports.testCpp = testCpp;
module.exports.testJs = testJs;
