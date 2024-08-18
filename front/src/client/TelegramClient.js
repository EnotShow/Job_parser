import BaseClient from "src/client/BaseClient";

class TelegramClient extends BaseClient {
    constructor(client) {
        super();
        this.client = client;
        this.base_url = `${this.client.base_url}/telegram`;
    }

    async generatePayload(data) {
        try {
            const response = await this.client.client.post(`${this.base_url}/generate_payload`, data);

            return response.data;
        } catch (error) {
            console.error('Error generating payload:', error);
            throw error;
        }
    }
}

export default TelegramClient