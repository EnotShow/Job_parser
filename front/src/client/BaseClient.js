class BaseClient {
    static addPagination(url, limit, page) {
    const params = [];

    if (typeof limit === 'number' || typeof limit === 'string') {
        params.push(`limit=${encodeURIComponent(limit)}`);
    }
    if (typeof page === 'number' || typeof page === 'string') {
        params.push(`page=${encodeURIComponent(page)}`);
    }

    if (params.length > 0) {
        const separator = url.includes('?') ? '&' : '?';
        const resultString = params.join('&');

        return url + separator + resultString;
    } else {
        return url;
    }
  }
}

export default BaseClient
