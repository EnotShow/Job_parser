function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + encodeURIComponent(value) + expires + "; path=/";
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

function verifyToken(cookie) {
  const cookies = getCookies();
  if (!cookies) {
    return false;
  }

}


export { setCookie, getCookies };
