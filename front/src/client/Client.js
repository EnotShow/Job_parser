import axios from 'axios';
import AppSettings from "src/AppSettings";
import {getCookies} from "src/helpers/_auth";
import UserClient from "src/client/UserClient";
import ApplicationClient from "src/client/ApplicationClient";
import SearchClient from "src/client/SearchClient";
import BaseClient from "src/client/BaseClient";

class JobParserClient extends BaseClient {
    constructor(base_url) {
        super();
        this.base_url = base_url;
        this.client = axios.create({
            baseURL: base_url,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        this.refreshToken = getCookies().refreshToken;

        this.users = new UserClient(this);
        this.applications = new ApplicationClient(this);
        this.searches = new SearchClient(this);
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

let jobParserClient = new JobParserClient(
    AppSettings.base_url
);

export default jobParserClient;
