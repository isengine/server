import { readFile } from 'fs/promises';
import { join } from 'path';
import puppeteer from 'puppeteer';
import * as ejs from 'ejs';

export const createPdf = async (
  template = '',
  data = {},
  options = {},
) => {
  template = template.replace(/[^\w_-]+/igu, '');
  const filePath = join(process.cwd(), 'views', `${template}.ejs`);

  const browser = await puppeteer.launch({
      executablePath: '/usr/bin/google-chrome',
      args: ['--headless', '--no-sandbox', '--disable-gpu', '--no-zygote'],
  })
    .catch(e => {
      console.log('e --1', e);
      return;
    });

  try {
    const page = await browser.newPage();
    
    const html = await readFile(filePath, { encoding: 'utf8' });
    const content = ejs.render(html, data);

    await page.setContent(content);

    options = {
      path: undefined,
      format: 'A4',
      printBackground: true,
      displayHeaderFooter: false,
      landscape: false,
      margin: {
        left: '0mm',
        top: '0mm',
        right: '0mm',
        bottom: '0mm',
      },
      ...options,
    };

    const buffer = await page.pdf(options)
      .catch(e => {
        console.log('e', e);
      });
    await browser.close();
    return buffer;
  } catch (e) {
    await browser.close();
    console.log(e);
  }
};
