import { md5 } from 'js-md5';
import dotenv from 'dotenv';
dotenv.config();

export const tokenVerifyErrors = (req) => {
  const token = req.header('Authorization');

  if (!token) {
    return('not exists');
  }

  const [hash, expired] = token.replace(/^\w+\s+/, '').split('.');

  if (!hash || !expired) {
    return('no hash or expired');
  }

  const now = Date.now();

  if (now > expired) {
    return 'is expired or not in ms';
  }

  const secret = process.env.SECRET;
  const hashed = md5(`${expired}.${secret}`);
  const passed = hash === hashed;

  if (!passed) {
    return 'is incorrect';
  }

  return;
};
