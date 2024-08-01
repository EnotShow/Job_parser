const BaseDTO = require("src/client/BaseDTO");

class UserRegisterDTO extends BaseDTO {
    constructor(email, password, language_code, refer_id) {
        super();
        this.email = email;
        this.password = password;
        this.language_code = language_code;
        this.refer_id = refer_id;
    }
}

export default UserRegisterDTO
