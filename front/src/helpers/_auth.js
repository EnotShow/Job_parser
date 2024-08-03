import jobParserClient from 'src/client/BaseClient';

function setCookie(name, value, days) {
  let expires = '';
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = '; expires=' + date.toUTCString();
  }
  document.cookie = name + '=' + encodeURIComponent(value) + expires + '; path=/';
}

function getCookies() {
  const cookies = document.cookie;
  const cookieObject = {};
  cookies.split(';').forEach(cookie => {
    const [name, ...rest] = cookie.split('=');
    const value = rest.join('=').trim();
    if (name) {
      cookieObject[name.trim()] = decodeURIComponent(value);
    }
  });
  return cookieObject;
}

async function verifyToken() {
  const cookies = getCookies();
  if (!cookies || !cookies.accessToken) {
    return false;
  } else {
    jobParserClient.client.defaults.headers['Authorization'] = `Bearer ${cookies.accessToken}`;
    try {
      const tokenVerified = await jobParserClient.verifyToken();
      if (!tokenVerified) {
        console.log("Trying to refresh token...");
        await jobParserClient.refreshAccessToken();
        return true;
      }
      return true;
    } catch (error) {
      console.error('Token verification failed:', error);
    }
    return false;
  }
}

export { setCookie, getCookies, verifyToken };
