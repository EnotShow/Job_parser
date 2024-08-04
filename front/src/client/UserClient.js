import BaseClient from "src/client/BaseClient";

class UserClient extends BaseClient {
    constructor(client) {
        super();
        this.client = client;
        this.base_url = `${this.client.base_url}/users`;
    }

    async getMe() {
        try {
            const response = await this.client.client.get(`${this.base_url}/me`);
            return response.data;
        } catch (error) {
            console.error('Error getting user data:', error);
            throw error;
        }
    }

    async updateMe(data) {
        try {
            const response = await this.client.client.put(`${this.base_url}/me`, data);
            return response.data;
        } catch (error) {
            console.error('Error updating user data:', error);
            throw error;
        }
    }

    async getSettings() {
        try {
            const response = await this.client.client.get(`${this.base_url}/me/settings`);
            return response.data;
        } catch (error) {
            console.error('Error getting user settings:', error);
            throw error;
        }
    }

    async getUserSettingsById(userId) {
        try {
            const response = await this.client.client.get(`${this.base_url}/settings/${userId}`);
            return response.data;
        } catch (error) {
            console.error('Error getting user settings by ID:', error);
            throw error;
        }
    }
}

export default UserClient
