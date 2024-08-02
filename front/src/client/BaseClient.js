const axios = require('axios');
const { settings } = require('./core/config/proj_settings');
const { UserRegisterDTO, UserLoginDTO } = require('./src/api/auth/auth_dto');

class JobParserClient {
    constructor(baseUrl = settings.base_url) {
        this.baseUrl = baseUrl;
        this.client = axios.create({
            baseURL: baseUrl,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        this.refreshToken = null;
    }

    async authAsUser(data) {
        try {
            const response = await this.client.post('/auth/login', data);
            if (response.status !== 200) {
                throw new Error('Authentication failed');
            }

            const { access_token, refresh_token } = response.data;
            this.client.defaults.headers['Authorization'] = `Bearer ${access_token}`;
            this.refreshToken = refresh_token;

            return response.data;
        } catch (error) {
            console.error('Error authenticating user:', error);
            throw error;
        }
    }

    async refreshAccessToken() {
        try {
            const response = await this.client.post('/auth/refresh', {
                refresh_token: this.refreshToken
            });
            if (response.status !== 200) {
                throw new Error('Token refresh failed');
            }

            const { access_token } = response.data;
            this.client.defaults.headers['Authorization'] = `Bearer ${access_token}`;
            this.refreshToken = access_token;

            console.log(response.data);
            return response.data;
        } catch (error) {
            console.error('Error refreshing access token:', error);
            throw error;
        }
    }

    async verifyToken() {
        try {
            const response = await this.client.get('/auth/verify_token');
            return response.status === 200;
        } catch (error) {
            console.error('Error verifying token:', error);
            throw error;
        }
    }

    async register(data) {
        try {
            const response = await this.client.post('/auth/register', data);
            if (response.status !== 200) {
                throw new Error('Registration failed');
            }

            return response.data;
        } catch (error) {
            console.error('Error registering user:', error);
            throw error;
        }
    }
}

export default JobParserClient;
