export const error = (res, message) => {
  message = JSON.stringify({ error: message });
  res.set({
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': message.length,
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    Pragma: 'no-cache',
    Expires: 0,
  });
  res.send(message);
  return true;
};
