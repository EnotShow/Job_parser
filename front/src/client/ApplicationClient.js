class ApplicationClient {
    constructor(client) {
        this.client = client;
        this.base_url = `${this.client.base_url}/applications`;
    }

    async getAllApplications() {
        try {
            const response = await this.client.client.get(`${this.base_url}/`);
            return response.data;
        } catch (error) {
            console.error('Error getting all applications:', error);
            throw error;
        }
    }

    async getApplication(applicationId) {
        try {
            const response = await this.client.client.get(`${this.base_url}/${applicationId}`);
            return response.data;
        } catch (error) {
            console.error('Error getting application by ID:', error);
            throw error;
        }
    }

    async getAppliedApplications(userId) {
        try {
            const response = await this.client.client.get(`${this.base_url}/applied`, {
                params: { user_id: userId }
            });
            return response.data;
        } catch (error) {
            console.error('Error getting applied applications:', error);
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
}

export default ApplicationClient;
