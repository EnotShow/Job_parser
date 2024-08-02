class BaseDTO {
    toJSON() {
        return Object.assign({}, this);
    }
}

export default BaseDTO
