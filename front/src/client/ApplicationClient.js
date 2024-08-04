import BaseClient from "src/client/BaseClient";

class ApplicationClient extends BaseClient {
    constructor(client) {
        super();
        this.client = client;
        this.base_url = `${this.client.base_url}/applications`;
    }

    async getApplications(limit = null, page = null) {
        try {
            const url = this.constructor.addPagination(`${this.base_url}/`, limit, page);
            const response = await this.client.client.get(url);
            return response.data;
        } catch (error) {
            console.error('Error getting applications:', error);
            throw error;
        }
    }

    async getApplicationById(applicationId) {
        try {
            const response = await this.client.client.get(`${this.base_url}/${applicationId}`);
            return response.data;
        } catch (error) {
            console.error('Error getting application by ID:', error);
            throw error;
        }
    }

    async createApplication(data) {
        try {
            const response = await this.client.client.post(`${this.base_url}/`, data);
            return response.data;
        } catch (error) {
            console.error('Error creating application:', error);
            throw error;
        }
    }

    async updateApplication(data, applicationId) {
        try {
            const response = await this.client.client.put(`${this.base_url}/${applicationId}`, data);
            return response.data;
        } catch (error) {
            console.error('Error updating application:', error);
            throw error;
        }
    }

    async deleteApplication(applicationId) {
        try {
            await this.client.client.delete(`${this.base_url}/${applicationId}`);
        } catch (error) {
            console.error('Error deleting application:', error);
            throw error;
        }
    }

    getApplyLink(searchId) {
      return `${this.base_url}/apply/${searchId}`;
    }
}

export default ApplicationClient;
