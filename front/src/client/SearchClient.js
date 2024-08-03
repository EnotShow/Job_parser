class SearchClient {
    constructor(client) {
        this.client = client;
        this.base_url = `${this.client.base_url}/searches`;
    }

    async getSearches() {
        try {
            const response = await this.client.client.get(`${this.base_url}/`);
            return response.data;
        } catch (error) {
            console.error('Error getting searches:', error);
            throw error;
        }
    }

    async getSearchById(searchId) {
        try {
            const response = await this.client.client.get(`${this.base_url}/${searchId}`);
            return response.data;
        } catch (error) {
            console.error('Error getting search by ID:', error);
            throw error;
        }
    }

    async createSearch(data) {
        try {
            const response = await this.client.client.post(`${this.base_url}/`, data);
            return response.data;
        } catch (error) {
            console.error('Error creating search:', error);
            throw error;
        }
    }

    // async updateSearch(data, searchId) {
    //     try {
    //         const response = await this.client.client.put(`${this.base_url}/${searchId}`, data);
    //         return response.data;
    //     } catch (error) {
    //         console.error('Error updating search:', error);
    //         throw error;
    //     }
    // }

    async deleteSearch(searchId) {
        try {
            await this.client.client.delete(`${this.base_url}/${searchId}`);
        } catch (error) {
            console.error('Error deleting search:', error);
            throw error;
        }
    }
}

export default SearchClient
