import dotenv from 'dotenv';
dotenv.config();

import cors from 'cors';
import express from 'express';
import http from 'http';
import { v4 } from 'uuid';
import { createPdf } from './src/pdf.handler.js';
import { tokenVerifyErrors } from './src/token.handler.js';
import { error } from './src/error.handler.js';

const app = express();

app
    .use(cors())
    .use(express.json())
    .use(express.static('./static'));

const server = http.createServer(app);

app.get('/base', async (req, res) => {
    console.log('-- get');
    res.set({
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        Pragma: 'no-cache',
        Expires: 0,
    });
    res.send('<h1>Hello World!</h1>');
});

app.post('/pdf/:template', async (req, res) => {
    const tokenError = tokenVerifyErrors(req);
    if (tokenError) {
        return error(res, `Not valid token: ${tokenError}`);
    }

    const { template } = req.params;
    const { data, options } = req.body;

    const buffer = await createPdf(template, data, options);
    if (!buffer) {
        return error(res, 'No result');
    }

    res.set({
        'Content-Type': 'application/pdf',
        'Content-Disposition': `inline; filename=${v4()}.pdf`,
        'Content-Length': buffer.length,
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        Pragma: 'no-cache',
        Expires: 0,
    });
    res.end(buffer);
});

const port = 3000;

await new Promise(() => server.listen(port, console.log(`Example app listening on port ${port}`)))
        .then(async () => {
    })
    .catch(async (e) => {
        console.error('--e', e);
        process.exit(1);
    });
